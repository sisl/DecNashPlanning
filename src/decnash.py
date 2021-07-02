# decnash.py

import torch
from torch import nn
from src.policy import Policy
import numpy as np
from src.datautils import powerseries
import time

## import julia files
#import julia
#j = julia.Julia()

from julia.api import Julia
jl = Julia(compiled_modules=False)
from julia import Main
jl.eval('include("./src/julia/AlgamesRoundabout.jl")')
jl.using('.AlgamesRoundabout')

class DecNash(Policy, nn.Module):

    def __init__(self, graph, xpoly, ypoly, smax, lengths, 
                 v0=11.17, s0=3., dth=5., amax=1.5, b=4., idm_intermediate=True):
        """
        Args:
            graph (InteractionGraph): interaction graph handle
            xpoly (torch.tensor): x position polynomial coefficients
            ypoly (torch.tensor): y position polynomial coefficients
            smax (torch.tensor): max path positions
            lengths (torch.tensor): vehicle_lengths
            v0 (float): desired velocity
            s0 (float): minimum spacing
            dth (float): desired time headway
            amax (float): max acceleration
            b (float): comfortable braking deceleration
            idm_intermediate (bool): if True, use idm policy when single car observes nodes
        """
        nn.Module.__init__(self)
        
        self._graph = graph
        self._xpoly = xpoly
        self._ypoly = ypoly
        self._smax = smax
        self._v0 = nn.Parameter(torch.tensor([v0]))
        self._s0 = nn.Parameter(torch.tensor([s0]))
        self._dth = nn.Parameter(torch.tensor([dth]))
        self._amax = nn.Parameter(torch.tensor([amax]))
        self._b = nn.Parameter(torch.tensor([b]))
        self._expdel = 4.
        self._lengths = lengths
        self._idm_intermediate = idm_intermediate
        self._times = []
        
    def compute_action_from_full_state(self, state):
        """
        Abstract policy computing accelerations for each vehicle.
        Args:
            state (torch.tensor): (*, nv, 6) (simulation state, s)
        Returns:
            a (torch.tensor): (*, nv, 1) actions
        """
        ndim = state.ndim
        lead_dims = state.shape[:-2]
        nv = state.shape[-2]
        lengths = self._lengths.reshape(*([1]*(ndim-2) + [-1, 1]))
        
        x = state[...,0:1]
        y = state[...,1:2]
        v = state[...,2:3]
        psi = state[...,3:4]
        psidot = state[...,4:5]
        s = state[...,5:6] # (*, nv, 1)
        
        # Set action as free action
        action = self._amax * (1. - (v / self._v0) ** self._expdel)
        
        if self._idm_intermediate:
            # generate idm policy
            dx = x.unsqueeze(-2) - x.unsqueeze(-3) 
            dy = y.unsqueeze(-2) - y.unsqueeze(-3)
            dr = (dx ** 2 + dy ** 2).sqrt()
            delpsi = self.to_circle(torch.atan2(dy,dx) - psi.unsqueeze(-3))
            dpsi = self.to_circle(psi.unsqueeze(-2) - psi.unsqueeze(-3))
            dcp = dpsi.cos()
            dsp = dpsi.sin()
            ndist = dr * delpsi.cos()
            ndisth = dr * delpsi.sin()
            vx = v * psi.cos()
            vy = v * psi.sin()
            
            follow_condition = (ndist > 0)
            ndist_ = torch.where(follow_condition, ndist, np.inf).detach()
        
        # add new maximal solve time
        self._times.append(0.)
        
        # compute sccs
        sccs = self._graph.strongly_connected_components
        for (control_nodes, observe_nodes) in sccs:
            
            scc_time = time.time()
            
            if len(control_nodes)==1 and len(observe_nodes)==0:
                # act freely according to IDM
                continue 
                
            elif self._idm_intermediate and len(control_nodes)==1:
                # follow idm to closest vehicle
                min_d, ind = torch.min(ndist_[observe_nodes, control_nodes[0], 0], dim=-1)
                car_ind = observe_nodes[ind]
                if min_d==np.inf:
                    # continue if no front vehicles
                    continue
                    
                min_d = dr[car_ind, control_nodes[0], 0]
                
                v_car = v[...,control_nodes[0],0]
                dvx = vx[car_ind,0] - vx[control_nodes[0],0]
                dvy = vy[car_ind,0] - vy[control_nodes[0],0]
                dv = (dvx ** 2 + dvy ** 2).sqrt()
                vdelpsi = self.to_circle(torch.atan2(dvy, dvx) - psi[control_nodes[0],0])        
                ndv = dv * vdelpsi.cos()
                
                sstar = self._s0 + v_car*self._dth + v_car*ndv / (2. * (self._amax * self._b).sqrt())
                sal = min_d
                action_int =  -self._amax*(sstar/sal)**2
                action[...,control_nodes[0],:] += action_int
            
            else:
                # call game solver
                combined = control_nodes+observe_nodes
                uc = len(observe_nodes)
                Main.v0 = self._v0.item()
                Main.uc = uc
                Main.xp = self._xpoly[combined].numpy()
                Main.yp = self._ypoly[combined].numpy()
                Main.sm = self._smax[combined].numpy()
                Main.ssd = torch.cat((s[...,combined,:],
                                      v[...,combined,:]),-1).detach().numpy() + 0.0001 # to avoid singularities
                
                
                try:
                    Main.eval("prob = setup_problem(ssd, xp, yp, sm, uc; N=20, dt=0.2, radius=3., vel_control=true, vel_des = Main.v0)")
                    Main.eval("u = action(prob;time=true)")
                    action[...,control_nodes,0] = torch.tensor(Main.u[:(len(Main.u)-uc)]) # exclude final uc actions
                except:
                    print('Solver failure')
            
            # add time
            scc_time = time.time() - scc_time
            if scc_time > self._times[-1]:
                self._times[-1] = scc_time
            
        return action

    @property
    def times(self):
        return self._times.copy()
    
    def to_circle(self, x):
        """
        Casts x (in rad) to [-pi, pi)
        
        Args:
            x (torch.tensor): (*) input angles (radians)
            
        Returns:
            y (torch.tensor): (*) x cast to [-pi, pi)
        """
        y = torch.remainder(x + np.pi, 2*np.pi) - np.pi
        return y
