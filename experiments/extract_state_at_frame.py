# experiment.py
import sys, os
sys.path.append('./')
import pickle
import pandas as pd
from src.datautils import *
from src import RoundaboutSimulator


LOCATIONS = ['DR_USA_Roundabout_FT',
             'DR_CHN_Roundabout_LN',
             'DR_DEU_Roundabout_OF',
             'DR_USA_Roundabout_EP',
             'DR_USA_Roundabout_SR']

def main(locnum, track, setting, frames, animate):
    
    name=LOCATIONS[locnum]
    
    # load a trackfile
    df = pd.read_csv('datasets/trackfiles/'+name+'/vehicle_tracks_%03i.csv'%(track))
    stv = df_to_stackedvehicletraj(df)
    sim = RoundaboutSimulator(stv)

    states = []
    s,_ = sim.reset()
    s = s.reshape(-1,5)
    states.append(s)
    
    
    if setting=='decnash':
        from src.policies.decnash import DecNash
        from src.graphs.conevisibility import ConeVisibilityGraph
        graph = ConeVisibilityGraph(r=20, half_angle=120)
        policy = DecNash(graph,*sim.path_coefs,sim.smax,
                         stv.lengths,idm_intermediate=False)
    elif setting=='cnash':
        from src.policies.decnash import DecNash
        from src.graphs.conevisibility import ConeVisibilityGraph
        graph = ConeVisibilityGraph(r=1000, half_angle=180)
        policy = DecNash(graph,*sim.path_coefs,sim.smax,
                         stv.lengths,idm_intermediate=False)
    elif setting=='idm':
        from src.policies.idm import IDM
        from src.graphs.closestobstacle import ClosestObstacleGraph
        graph = ClosestObstacleGraph(half_angle=20)
        policy = IDM(stv.lengths)
    else:
        raise('Setting %s not implemented'%(setting))
    
    
    graph_list = []
    
    for i in range(frames):
        print("Frame %04d" %(i))
        v = s[:,2:3]
        nni = ~torch.isnan(v)
        
        # update graph
        graph.update_graph(s.reshape(-1))
        graph_list.append(graph.edges)
        
        if i == 43:          
            torch.set_printoptions(precision=10)
            import ipdb
            ipdb.set_trace()
        
        # compute action
        if 'nash' in setting:
            p = sim.state[:,0:1]
            full_state = torch.cat((s,p),-1)
            a = policy.compute_action_from_full_state(full_state)
        else:
            a = policy(s.reshape(-1))
            
        if torch.any(torch.isnan(a[nni])):
            raise('Improper Acceleration')
        
        # simulate step
        s, _ = sim.step(a)
        s = s.reshape(-1,5)
        states.append(s)
    
    # append final state/graph
    graph.update_graph(s.reshape(-1))
    graph_list.append(graph.edges)
    states = torch.stack(states).reshape(frames+1,-1)


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
    parser.add_argument('--ani', type=bool, default=True,
                       help='Whether to save animation')
    args = parser.parse_args()
    main(args.loc, args.track, args.exp, args.frames, args.ani)
