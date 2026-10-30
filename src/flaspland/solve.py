"""
Solve a Flatland environment with ASP encodings and simulate the plan.

Run as `flaspland solve ENV ENCODING [ENCODING ...]`; see `flaspland solve -h`.
"""

# standard packages
import sys
import warnings
import os
import time
import pickle
import tempfile
from argparse import ArgumentParser, Namespace
from pathlib import Path

# custom modules
from .modules.api import FlatlandPlan
from .modules.convert import convert_malfunctions_to_clingo, convert_formers_to_clingo, convert_futures_to_clingo

# clingo
from clingo.application import clingo_main

# rendering visualizations
from flatland.envs.rail_env import RailEnvActions
from flatland.utils.rendertools import RenderTool
import imageio.v2 as imageio
from PIL import Image, ImageDraw, ImageFont

FONT = Path(__file__).resolve().parent / "modules" / "LiberationMono-Regular.ttf"


class MalfunctionManager():
    def __init__(self, num_agents):
        self.num_agents = num_agents
        self.malfunctions = []

    def get(self) -> list:
        """ get the list of malfunctions """
        return(self.malfunctions)

    def deduct(self) -> None:
        """ decrease the duration of each malfunction by one and delete expired malfunctions """
        malfunctions_to_remove = []
        for i, malf in enumerate(self.malfunctions):
            self.malfunctions[i] = (self.malfunctions[i][0], self.malfunctions[i][1] - 1)
            if self.malfunctions[i][1] == 0:
                malfunctions_to_remove.append(i)
        
        # delete expired malfunctions
        for i in sorted(malfunctions_to_remove, reverse=True):
            del self.malfunctions[i]

    def check(self, info) -> set:
        """ check current state of the env for new malfunctions """
        malfunctioning_info = info['malfunction']
        malfunctioning_trains = {train for train, duration in malfunctioning_info.items() if duration > 0}
        existing = {malf[0] for malf in self.malfunctions}
        new = malfunctioning_trains.difference(existing)

        # add new ones to malfunctions
        for train in new:
            self.malfunctions.append((train, malfunctioning_info[train]))

        return(new)


def check_plan(action_list, when) -> list:
    """ stop with a clear message if clingo did not produce a plan """
    if action_list is None:
        raise SystemExit(f"No plan found {when}: see the clingo output above (e.g. UNSATISFIABLE, or an error in an encoding).")
    return(action_list)


class SimulationManager():
    def __init__(self,env,encodings,clingo_args=()):
        self.env = env
        self.encodings = encodings
        self.clingo_args = list(clingo_args)

    def build_actions(self) -> list:
        """ create initial list of actions """
        # pass env, encodings
        app = FlatlandPlan(self.env, None)
        clingo_main(app, self.encodings + self.clingo_args)
        return(check_plan(app.action_list, "for the initial plan"))

    def provide_context(self, actions, timestep, malfunctions) -> str:
        """ provide additional facts when updating list """
        # actions that have already been executed
        # wait actions that are enforced because of malfunctions
        # future actions that were previously planned
        past = convert_formers_to_clingo(actions[:timestep])
        present = convert_malfunctions_to_clingo(malfunctions, timestep)
        future = convert_futures_to_clingo(actions[timestep:])
        return(past + present + future)

    def update_actions(self, context) -> list:
        """ update list of actions following malfunction """
        # pass env, encodings, context
        app = FlatlandPlan(self.env, context)
        clingo_main(app, self.encodings + self.clingo_args)
        return(check_plan(app.action_list, "while replanning after a malfunction"))


class OutputLogManager():
    def __init__(self) -> None:
        self.logs = []

    def add(self,info) -> None:
        """ add info from a timestep to the log """
        self.logs.append(info)

    def save(self,directory) -> None:
        """ save output log to local drive """
        with open(os.path.join(directory, "paths.csv"), "w") as f:
            f.write("agent;timestep;position;direction;status;given_command\n")
            for log in self.logs:
                f.write(log)

def get_position_and_direction(agent) -> tuple:
    """ get an agent's position and direction; position is None while the agent is off the map """
    if agent.current_configuration is not None:
        return(agent.current_configuration)
    # off the map: use the arrival direction if done, otherwise the starting direction
    if agent.target_configuration is not None:
        return(None, agent.target_configuration[1])
    return(None, agent.initial_configuration[1])


def get_args(argv=None):
    """ capture command line inputs; everything after `--` is passed on to clingo """
    argv = sys.argv[1:] if argv is None else list(argv)
    clingo_args = []
    if '--' in argv:
        split = argv.index('--')
        argv, clingo_args = argv[:split], argv[split+1:]

    parser = ArgumentParser(
        prog='flaspland solve',
        description='Solve a Flatland environment with your encodings and simulate the plan. '
                    'Results are saved to output/<date>_<time>/ in the current folder.',
        epilog="Options after '--' are passed on to clingo, e.g. 'flaspland solve env.pkl main.lp -- -t 4'.")
    parser.add_argument('env', type=str, help='the Flatland environment, a .pkl file created by flaspland build')
    parser.add_argument('encodings', type=str, nargs='+', help='one or more encodings (.lp) to load into clingo, e.g. a single file of #include statements')
    parser.add_argument('--time-limit', type=int, metavar='SECONDS', help='stop each clingo call after SECONDS and use the best plan found so far')
    parser.add_argument('--no-render', action='store_true', help='if included, run the Flatland simulation but do not render a GIF')
    args = parser.parse_args(argv)

    if args.time_limit is not None:
        clingo_args.append(f'--time-limit={args.time_limit}')
    args.clingo_args = clingo_args
    return(args)


def create_output_dir() -> str:
    """ create a new folder output/<date>_<time> in the current folder """
    stamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    path = os.path.join("output", stamp)
    number = 1
    while os.path.exists(path):
        number += 1
        path = os.path.join("output", f"{stamp}_{number}")
    os.makedirs(path)
    return(path)


def main(argv=None) -> int:
    args: Namespace = get_args(argv)
    if not os.path.isfile(args.env):
        raise SystemExit(f"Environment not found: {args.env}")
    with open(args.env, "rb") as f:
        try:
            env = pickle.load(f)
        except (ModuleNotFoundError, AttributeError) as e:
            raise SystemExit(f"Could not load '{args.env}' ({e}). It was probably created with a different version of flatland; regenerate it with 'flaspland build'.")
    no_render = args.no_render

    # create manager objects
    mal = MalfunctionManager(env.get_num_agents())
    sim = SimulationManager(env, args.encodings, args.clingo_args)
    log = OutputLogManager()

    # envrionment rendering
    env_renderer = None
    if not no_render:
        env_renderer = RenderTool(env, gl="PILSVG")
        env_renderer.reset()
        images = []

    # temporary directory for the rendered frames
    frames = tempfile.TemporaryDirectory()
    action_map = {RailEnvActions.MOVE_LEFT:'move_left', RailEnvActions.MOVE_FORWARD:'move_forward', RailEnvActions.MOVE_RIGHT:'move_right', RailEnvActions.STOP_MOVING:'wait'}
    state_map = {0:'waiting', 1:'ready to depart', 2:'malfunction (off map)', 3:'moving', 4:'stopped', 5:'malfunction (on map)', 6:'done'}
    dir_map = {0:'n', 1:'e', 2:'s', 3:'w'}

    actions = sim.build_actions()

    timestep = 0
    while len(actions) > timestep:
        # add to the log
        for a in actions[timestep]:
            position, direction = get_position_and_direction(env.agents[a])
            log.add(f'{a};{timestep};{position};{dir_map[direction]};{state_map[env.agents[a].state]};{action_map[actions[timestep][a]]}\n')

        _, _, done, info = env.step(actions[timestep])

        # end if simulation is finished
        if done['__all__'] and timestep < len(actions)-1:
            warnings.warn('Simulation has reached its end before actions list has been exhausted.')
            break

        # check for new malfunctions
        new_malfs = mal.check(info)

        if len(new_malfs) > 0:
            context = sim.provide_context(actions, timestep, mal.get())
            actions = sim.update_actions(context)

        mal.deduct() #??? where in the loop should this go - before context?
        
        # render an image
        filename = os.path.join(frames.name, 'flatland_frame_{:04d}.png'.format(timestep))
        if env_renderer is not None:
            env_renderer.render_env(show=True, show_observations=False, show_predictions=False)
            env_renderer.gl.save_image(filename)
            env_renderer.reset()

            # add red numbers in the corner
            with Image.open(filename) as img:
                draw = ImageDraw.Draw(img)
                padding = 10
                font_size = int(min(img.width, img.height) * 0.10)
                try:
                    font = ImageFont.truetype(str(FONT), font_size)
                except IOError:
                    font = ImageFont.load_default()
                
                # prepare text
                text = f"{timestep}"
                size = font.getbbox(text)
                text_width = size[2]-size[0]
                text_position = (img.width - text_width - padding, padding)
                
                # draw text borders
                x, y = text_position
                border_color = "black"
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
                    draw.text((x + dx, y + dy), text, fill=border_color, font=font)
                
                # draw text
                draw.text(text_position, text, fill="red", font=font)
                img.save(filename)

            images.append(imageio.imread(filename))
        # images.append(imageio.imread(filename))

        timestep = timestep + 1

    frames.cleanup()

    # create a new folder for the gif and output log
    output_dir = create_output_dir()

    # combine images into gif
    if not no_render:
        imageio.mimsave(os.path.join(output_dir, "animation.gif"), images, format='GIF', loop=0, duration=240)

    # save output log
    log.save(output_dir)
    print(f"flaspland: results saved to {output_dir}")
    return(0)


if __name__ == "__main__":
    sys.exit(main())
