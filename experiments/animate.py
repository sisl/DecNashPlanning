# experiment.py
import torch
import pickle
import intersim.datautils as utils
from intersim import RoundaboutSimulator
import os
import matplotlib.animation as animation
from intersim.viz.animatedviz import AnimatedViz
import matplotlib.pyplot as plt

LOCATIONS = ['DR_USA_Roundabout_FT',
             'DR_CHN_Roundabout_LN',
             'DR_DEU_Roundabout_OF',
             'DR_USA_Roundabout_EP',
             'DR_USA_Roundabout_SR']

def animate(locnum, track, setting, frames):
    name=LOCATIONS[locnum]

    fullname = name+'_track%03i_%s_frames%04i'%(track,setting,frames)
    outdir = './experiments/results/'

    # load states
    states = torch.load(outdir+fullname+'_states.pt')

    # load graphs
    graph_list = pickle.load(open(outdir+fullname+'_graphs.pkl', 'rb'))

    # load lengths, widths
    lengths = torch.load(outdir+fullname+'_lengths.pt')
    widths = torch.load(outdir+fullname+'_widths.pt')

    # save animation
    Writer = animation.writers['ffmpeg']
    writer = Writer(fps=15, bitrate=1800)
    fig = plt.figure()
    ax = fig.gca()
    osm = f'{utils.DATASET_DIR}/maps/'+name+'.osm'
    av = AnimatedViz(ax, osm, states, lengths, widths, graphs=graph_list)
    ani = animation.FuncAnimation(fig, av.animate, frames=len(states),
                    interval=20, blit=True, init_func=av.initfun,
                    repeat=False)
    ani.save(outdir+fullname+'_ani_manual.mp4', writer)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Run Roundabout Experiment.')
    parser.add_argument('--loc', default=0, type=int,
                       help='location (default 0)')
    parser.add_argument('--track', default=0, type=int,
                       help='track number (default 0)')
    parser.add_argument('--frames', default=1000, type=int,
                       help='number of frames (default 1000)')
    parser.add_argument('--exp', choices=['decnash', 'cnash', 'idm'],
                        default='decnash', help='experiment')
    args = parser.parse_args()
    animate(args.loc, args.track, args.exp, args.frames)



