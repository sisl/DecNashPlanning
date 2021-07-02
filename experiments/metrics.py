import sys, os
sys.path.append('./')
import pickle
from src.datautils import *
from src.graph import InteractionGraph
from src.collisions import *
import torch

LOCATIONS = ['DR_USA_Roundabout_FT',
             'DR_CHN_Roundabout_LN',
             'DR_DEU_Roundabout_OF',
             'DR_USA_Roundabout_EP',
             'DR_USA_Roundabout_SR']

def add_edges(neighbor_dict,edges):
    for (i,j) in edges:
        if j not in neighbor_dict[i]:
            neighbor_dict[i].append(j)

def main(locnum, tracks, settings, frames):
     
    name = LOCATIONS[locnum]
    outdir = './experiments/results/'
    v_target = 11.17
    for setting in settings:
        print(setting)
        
        # collisions 
        
        # hand-counted
        # if setting == 'idm':
        #     collisions = torch.tensor([36., 23., 34., 21., 24.]) ## VERY WRONG - true = [99,30,47,54,49]
        # elif setting == 'cnash':
        #     collisions = torch.tensor([0., 5., 2., 12., 5.]) ## pretty close - true = [0,5,2,11,6]
        # elif setting == 'decnash':
        #     collisions = torch.tensor([0., 0., 0., 0., 1.]) ## right 
        
        # actual
        cs = []
        for track in tracks:
            fullname=name+'_track%03i_%s_frames%04i'%(track,setting,frames)
            s = torch.load(outdir+fullname+'_states.pt')
            l = torch.load(outdir+fullname+'_lengths.pt')
            w = torch.load(outdir+fullname+'_widths.pt')
            c = count_collisions(s, l, w)
            cs.append(c)
        collisions = torch.tensor(cs)
        print("Collisions: %7.4f \pm %7.4f" %(collisions.mean(), collisions.std()/(len(collisions)**.5)))
        
        # shortfall                         
        vs = []
        for track in tracks:
            fullname=name+'_track%03i_%s_frames%04i'%(track,setting,frames)
            filename=outdir+fullname+'_states.pt'
            s = torch.load(filename)
            s = s.reshape(s.shape[0], -1, 5)
            v = s[:,:,2]
            for i in range(v.shape[1]):
                nni = ~torch.isnan(v[:,i])
                v_car = v[nni,i]
                if len(v_car)>0:
                    vs.append(v_car.mean().item())
        vs = np.array(vs)
        print("Velocity Shortfall: %7.4f \pm %7.4f" %(v_target-vs.mean(), vs.std()/(len(vs)**.5)))                       
        # players
        ps = []
        if setting == 'idm':
            players = torch.tensor([1., 1.])
        else:
            for track in tracks:
                fullname=name+'_track%03i_%s_frames%04i'%(track,setting,frames)
                filename=outdir+fullname          
                graph_list=pickle.load(open(filename+'_graphs.pkl', 'rb'))
                
                states = torch.load(filename+'_states.pt')
                states_reshaped = states.reshape(states.shape[0], -1, 5)
                
                for i in range(1,len(graph_list)-1):
                    edges = graph_list[i]
                    state = states_reshaped[i]
                    v = state[:,2]
                    nni = ~torch.isnan(v)
                    neighbor_dict = {i:[] for i in range(len(v)) if nni[i]} 
                    add_edges(neighbor_dict, edges)
                    g = InteractionGraph(neighbor_dict)
                    sccs = g.strongly_connected_components
                    ps.append(max([0]+[len(scc[0]) for scc in sccs]))                    
                    
            players = torch.tensor(ps, dtype=torch.float)
        print("Players: %6.4f \pm %6.4f" %(players.mean(), players.std()))    
                
        # times
        ts = []
        for track in tracks:
            fullname=name+'_track%03i_%s_frames%04i'%(track,setting,frames)
            filename=outdir+fullname+'_times.csv'
            ts.append(np.loadtxt(filename)[1:])
        times = np.concatenate(ts)
        print("Times: %6.4f \pm %6.4f" %(times.mean(), times.std()))         
        print("")
        
if __name__ == "__main__":
    locnum = 0
    tracks = list(range(5))
    settings = ['idm','cnash','decnash']
    frames = 1000
    main(locnum, tracks, settings, frames)