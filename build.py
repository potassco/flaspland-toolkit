from fractions import Fraction

from flatland.envs.rail_env import RailEnv
from flatland.envs.rail_env_action import RailEnvActions

from flatland.envs.rail_generators import sparse_rail_generator
from flatland.envs.line_generators import sparse_line_generator
from flatland.envs.timetable_generators import timetable_generator

from flatland.envs.malfunction_generators import ParamMalfunctionGen, MalfunctionParameters

from flatland.envs.observations import GlobalObsForRailEnv
from flatland.envs.step_utils.states import TrainState
from flatland.envs.persistence import RailEnvPersister

# INPUT ARGUMENTS


# RAIL GENERATOR
rail_gen = sparse_rail_generator(
    max_num_cities=4,
    grid_mode=False,
    max_rails_between_cities=2,
    max_rail_pairs_in_city=2,
    seed=42,
    p_level_free=0.3
)

# LINE GENERATOR
speed_ratio_map = {
    1.0:        0.25,
    1 / 2:      0.25,
    1 / 3:      0.25,
    1 / 4:      0.25
}

line_gen = sparse_line_generator(
    speed_ratio_map=speed_ratio_map,
    line_length=3 # one intermediate stop
)

# TIMETABLE GENERATOR
tt_gen = timetable_generator

# MALFUNCTION GENERATOR
malfunction_gen = ParamMalfunctionGen(
    parameters=MalfunctionParameters(
        malfunction_rate=1 / 50,
        min_duration=3,
        max_duration=10
    )
)

# OBSERVATION BUILDER
obs_builder = GlobalObsForRailEnv()

# ENVIRONMENT
env = RailEnv(
    width=30,
    height=30,
    number_of_agents=5,
    rail_generator=rail_gen,
    line_generator=line_gen,
    timetable_generator=tt_gen,
    acceleration_delta=1.0,
    braking_delta=-1.0,
    malfunction_generator=malfunction_gen,
    obs_builder_object=obs_builder,
    remove_agents_at_target=True,
    random_seed=42
)

env.reset()


# SAVE ENVIRONMENT
"""
First save the environment as a pickle file, which is the default format for Flatland environments.
"""
SAVE_PATH = "./tmp"
#RailEnvPersister.save(env, f"{SAVE_PATH}/flatland4_example.pkl")

"""
Next save the environment as an lp file, which can be used for debugging in clingo.

There are two components to the file:

Parameters
-----------
* global time horizon
* size of environment (height, width)
* number of agents (trains)
* train information
    * start
    * waypoints
    * end
    * speed
* acceleration and braking deltas


Layout
-----------
* cells (location and track type)
* level-free crossings (location)

"""
dirs = {0: "n", 1: "e", 2: "s", 3: "w"}
params_str = f"global({env._max_episode_steps}).\n\n"
layout_str = ""

for a in env.agents:
    params_str += f"train({a.handle}).\n"
    params_str += f"start({a.handle},{a.initial_position[::-1]},{dirs[a.initial_direction]},{a.earliest_departure}).\n".replace(" ", "")
    params_str += f"end({a.handle},{a.target},{a.latest_arrival}).\n".replace(" ", "")
    params_str += f"speed({a.handle},{1/(a.speed_counter.max_speed)}).\n".replace(" ", "")

    for idx, wp in enumerate(a.waypoints[1:-1]):
        params_str += f"waypoint({a.handle},{idx+1},{wp[0].position[::-1]}, {dirs[wp[0].direction]}, {a.waypoints_latest_arrival[idx+1]}, {a.waypoints_earliest_departure[idx+1]}).\n".replace(" ", "")
    
    params_str += "\n"

with open(f"{SAVE_PATH}/flatland4_example.lp", "w") as f:
    f.write(params_str + "\n" + layout_str)