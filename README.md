# DecNashPlanning
Decentralized game-theoretic planning using the [INTERACTION Dataset](https://interaction-dataset.com/)

Code for "Multi-Vehicle Control in Roundabouts using Decentralized Game-Theoretic Planning" at IJCAI 2021 AI4AD Workshop.

## Getting started

1. Clone the DecNashPlanning repository.
```
git clone https://github.com/sisl/DecNashPlanning.git
cd DecNashPlanning
```

2. This package uses [poetry](https://python-poetry.org/) for dependency management. Once you've [setup poetry](https://python-poetry.org/docs/#installation), you can install all dependencies by running in the `./install` script.

3. In order for the `InteractionSimulator` to work, you need to place your copy of the `INTERACTION Dataset` in the directory that the `INTERSIM_DATASET_DIR` environment variable points to.
    - the contents of `recorded_trackfiles` should be copied to `$INTERSIM_DATASET_DIR/trackfiles`
    - the contents of `maps` should be copied to `$INTERSIM_DATASET_DIR/maps`

If you want to avoid setting `INTERSIM_DATASET_DIR` environment variable manually every time, you can add it to the `.env` file at the repo root which will be automatically sources upon sourcing `activate`
```
# .env
export INTERSIM_DATASET_DIR=/path/to/INTERACTION/dataset/.../
```

## Running experiments

In order to run experiments, you need to activate the poetry environment. For this purpose run `source activate`.

You can run all experiments to generate trajectories and videos using `python experiments/exp_wrapper.py` (which makes successive calls to `experiments/experiment.py` with appropriate settings.

To calculate metrics from already generated trajectories, run `python experiments/metrics.py`.

To calculate metrics from already generated trajectories, run `python experiments/metrics.py`.

To generate plots used in paper for single game solution, run `python experiments/single_game.py`.

You can manually make animations from saved states, graphs, lengths, and widths (post-process) using `python experiments/animate.py`.

## Issues
For issues with `ffmpeg` when saving videos, if using conda to manage environments, use `conda install -c conda-forge ffmpeg`

## Citation

If you found this repository or the associated simulator useful, please cite this [paper](https://www.dropbox.com/s/kd19us8447fhabu/19.pdf?dl=0):

```
@inproeedings{jamgochian2021multivehicle,
  author  = {Arec Jamgochian and Kunal Menda and Mykel J. Kochenderfer},
  title   = {Multi-Vehicle Control in Roundabouts using Decentralized Game-Theoretic Planning}
}
```
