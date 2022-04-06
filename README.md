# DecNashPlanning
Decentralized game-theoretic planning with v0.0.2 of the [Interaction Simulator](https://github.com/InteractionSimulator), which uses the [Interaction Dataset](https://interaction-dataset.com/) scenarios to determine vehicle paths and spawn times.

Code for "[Multi-Vehicle Control in Roundabouts using Decentralized Game-Theoretic Planning](https://www.dropbox.com/s/kd19us8447fhabu/19.pdf?dl=0)" at IJCAI 2021 AI4AD Workshop.

If you find this repository useful, please cite the paper:

```
@inproceedings{jamgochian2021multivehicle,
  author = {Arec Jamgochian and Kunal Menda and Mykel J. Kochenderfer},
  title = {Multi-Vehicle Control in Roundabouts using Decentralized Game-Theoretic Planning}
  series = {Artificial Intelligence for Autonomous Driving Workshop},
  booktitle = {International Joint Conference on Artificial Intelligence (IJCAI)},
  year = {2021}
}
```

## Getting started
Clone the DecNashPlanning repository
```
git clone https://github.com/sisl/DecNashPlanning.git
cd DecNashPlanning
```

Clone InteractionSimulator with the `decnash` tag and install requirements using `poetry`.
```
git clone --branch decnash https://github.com/sisl/InteractionSimulator.git
cd InteractionSimulator
poetry install
poetry shell
cd ..
export PYTHONPATH=$(pwd):$PYTHONPATH
```

Copy INTERACTION Dataset files:
The INTERACTION dataset contains a two folders which should be copied into a folder called `./InteractionSimulator/datasets`: 
  - the contents of `recorded_trackfiles` should be copied to `./InteractionSimulator/datasets/trackfiles`
  - the contents of `maps` should be copied to `./InteractionSimulator/datasets/maps`

Install additional requirements for `DecNashPlanning`:
```
pip install -r requirements.txt
```
Copy INTERACTION Dataset files:
The INTERACTION dataset contains a two folders which should be copied into a folder called `./InteractionSimulator/datasets`: 
  - the contents of `recorded_trackfiles` should be copied to `./InteractionSimulator/datasets/trackfiles`
  - the contents of `maps` should be copied to `./InteractionSimulator/datasets/maps`

Download and install [Julia](julialang.org) . We use version 1.5.3.

## Running experiments
You can run all experiments to generate trajectories and videos using `python experiments/exp_wrapper.py` (which makes successive calls to `experiments/experiment.py` with appropriate settings.

To calculate metrics from already generated trajectories, run `python experiments/metrics.py`.

To generate plots used in paper for single game solution, run `python experiments/single_game.py`.

You can manually make animations from saved states, graphs, lengths, and widths (post-process) using `python experiments/animate.py`.