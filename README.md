# DecNashPlanning
Decentralized game-theoretic planning using the [INTERACTION Dataset](https://interaction-dataset.com/)

Code for "Multi-Vehicle Control in Roundabouts using Decentralized Game-Theoretic Planning" at IJCAI 2021 AI4AD Workshop.

## Getting started
Clone InteractionSimulator and pip install the module.
```
git clone https://github.com/sisl/InteractionSimulator.git
cd InteractionSimulator
git checkout v0.0.2
pip install -e .
cd ..
export PYTHONPATH=$(pwd):$PYTHONPATH
```
Install additional requirements
```
pip install -r requirements.txt
```
Copy INTERACTION Dataset files:
The INTERACTION dataset contains a two folders which should be copied into a folder called `./InteractionSimulator/datasets`: 
  - the contents of `recorded_trackfiles` should be copied to `./InteractionSimulator/datasets/trackfiles`
  - the contents of `maps` should be copied to `./InteractionSimulator/datasets/maps`

## Running experiments
Can run all experiments to generate trajectories and videos using `python experiments/exp_wrapper.py` (which makes successive calls to `experiments/experiment.py` with appropriate settings.

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
