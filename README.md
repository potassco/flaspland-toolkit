# flaspland

Welcome to the `flaspland-toolkit`!

## Installation

> [!TIP]
> We recommend first forking [`flaspland-encodings`](https://github.com/potassco/flaspland-encodings/fork) to form the basis of your project folder.
> Name it something that fits for your project.
> Doing so will give you access to encodings that define the environment, translate grid structures into graphs, and find paths for trains.
> In these instructions, we cite the command `cd my-project`, where you would instead insert the name of your project folder.

Install the toolkit once; the `flaspland` command then works in any folder.

```bash
git clone https://github.com/potassco/flaspland-toolkit.git && cd flaspland-toolkit
conda env create -f environment.yml 
```

From there you are free to start using `flaspland` with your project.

## Usage

After installing the project, activate the newly-created environment and navigate to your project folder. 
Once inside, initialize the flaspland tool for that repository.

```bash
conda activate flaspland
cd my-project
flaspland init                       # create config.toml with the build settings
```

### Building
The toolkit can be used to build environments.
You can specify the parameters of the environment by using arguments
(see `flaspland build --help` for more info),
or you can directly edit the `config.toml` file that came with the toolkit.

```bash
flaspland build 5 --agents 3         # generate environments into envs/
```

### Solving
The toolkit can be used to run your encodings.
To convert to Flatland, you need to use the `.pkl` version of the environment.
In order to keep your commands short,
we recommend creating a single encoding file and using `#include` to select the files you want to use.
See [an example encoding](https://github.com/potassco/flaspland-encodings/blob/main/setting-sub.lp).

```bash
flaspland solve envs/pkl/env_001--3_2.pkl encodings/main.lp
```

Results are saved to `output/<date>_<time>/` as `animation.gif` and
`paths.csv`. Run `flaspland <command> -h` for all options.


### Example
The repository `flaspland-encodings` includes an example [environment and solution](https://github.com/potassco/flaspland-encodings/tree/main/example).
This comes automatically if you fork the repository, as suggested at the top of this document.
Users can refer to `example/solution.lp` as an example of expected output for a proper encoding on the environment `example-env.pkl`,
which may help during development and debugging.

```bash
cd my-project/examples
flaspland solve example/example-env.pkl example/solution.lp
```

## Documentation

The documentation covers installation, examples, the input and output format
of encodings, and troubleshooting. To view it locally:

```bash
pip install -e ".[doc]"
mkdocs serve -o
```

Instructions for running the tests and code checks can be found in
[DEVELOPMENT.md](./DEVELOPMENT.md).
