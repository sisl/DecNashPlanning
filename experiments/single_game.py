import numpy as np
import matplotlib.pyplot as plt

from julia.api import Julia
jl = Julia(compiled_modules=False)
from julia import Main
from julia import Pkg
Pkg.activate('.')
Pkg.instantiate()
jl.eval('include("./src/julia/AlgamesRoundabout.jl")')
jl.using('.AlgamesRoundabout')



#include("../src/julia/AlgamesRoundabout.jl")
#using .AlgamesRoundabout
#using Plots

# game settings
Main.uc = 1
Main.xp = [[ 9.92483328e+02,  1.00992169e+00, -1.06373371e-02,
         5.44482755e-03, -1.56124376e-03,  2.96003128e-04,
        -3.97313295e-05,  3.90312145e-06, -2.85274315e-07,
         1.56024980e-08, -6.35690001e-10,  1.89076217e-11,
        -3.87873308e-13,  4.48568557e-15,  1.04254642e-17,
        -1.56423667e-18,  3.29567455e-20, -3.92492131e-22,
         2.88391940e-24, -1.22655411e-26,  2.32697067e-29],
       [ 1.06021128e+03, -3.94695552e-01, -2.65480724e-01,
         7.72331895e-02, -1.28764151e-02,  1.35288108e-03,
        -9.63032818e-05,  4.88162591e-06, -1.81700838e-07,
         5.04535619e-09, -1.04705323e-10,  1.59722674e-12,
        -1.69571241e-14,  1.03019971e-16,  9.91898387e-20,
        -9.43413842e-21,  1.05428864e-22, -6.63261341e-25,
         2.57206072e-27, -5.76876538e-30,  5.76518416e-33],
       [ 1.03956886e+03, -6.66404535e-01,  1.68722243e-01,
        -9.61339363e-02,  2.85736090e-02, -4.98160515e-03,
         5.74110190e-04, -4.64814345e-05,  2.72600951e-06,
        -1.17131710e-07,  3.66123146e-09, -8.02534848e-11,
         1.09485575e-12, -4.37048296e-15, -1.60842484e-16,
         3.75509773e-18, -3.66648589e-20,  1.13749036e-22,
         1.09091124e-24, -1.18463934e-26,  3.49468666e-29],
       [ 1.04368180e+03, -1.00002693e+00,  1.62315284e-02,
        -3.67536866e-03,  5.53573396e-04, -6.29877665e-05,
         5.78415323e-06, -4.25140558e-07,  2.40307950e-08,
        -1.01864918e-09,  3.20099297e-11, -7.33625975e-13,
         1.17000629e-14, -1.09904618e-16,  1.15040614e-20,
         1.78120874e-20, -3.04212971e-22,  2.83825404e-24,
        -1.61941073e-26,  5.32615567e-29, -7.79110941e-32]]

Main.yp = [[ 9.85056258e+02, -7.33797447e-03, -1.60582416e-02,
         7.69597502e-03, -2.24558622e-03,  4.25337577e-04,
        -5.54541321e-05,  5.15766542e-06, -3.50257135e-07,
         1.75989111e-08, -6.54629343e-10,  1.76918782e-11,
        -3.26218029e-13,  3.19403241e-15,  1.82888213e-17,
        -1.28191809e-18,  2.40451512e-20, -2.64439070e-22,
         1.81562474e-24, -7.25616139e-27,  1.29732722e-29],
       [ 9.72977375e+02,  1.68013496e-01,  2.62859673e-01,
        -8.19509164e-02,  1.45446629e-02, -1.62040306e-03,
         1.21181800e-04, -6.37599460e-06,  2.43629872e-07,
        -6.88482976e-09,  1.44532818e-10, -2.22237103e-12,
         2.37577213e-14, -1.45865218e-16, -1.22469420e-19,
         1.32130012e-20, -1.49434739e-22,  9.49787654e-25,
        -3.72296646e-27,  8.44740565e-30, -8.54771388e-33],
       [ 9.71432643e+02,  1.09644346e+00, -3.16524750e-01,
         2.00055092e-01, -6.62052012e-02,  1.33578100e-02,
        -1.79359783e-03,  1.69149381e-04, -1.15739527e-05,
         5.84432938e-07, -2.18342229e-08,  5.93275610e-10,
        -1.10412944e-11,  1.11264523e-13,  5.14067848e-16,
        -4.13379623e-17,  7.86212065e-19, -8.68704866e-21,
         5.97414273e-23, -2.38779614e-25,  4.26590812e-28],
       [ 1.00765571e+03,  1.40122934e-01,  4.66769186e-03,
        -9.84994942e-04,  3.54607296e-04, -5.61687052e-05,
         4.94425778e-06, -2.64201889e-07,  7.95049087e-09,
        -6.11160141e-11, -5.32885165e-12,  2.53520405e-13,
        -5.65667160e-15,  6.63090268e-17, -1.23853952e-19,
        -9.29126946e-21,  1.68471272e-22, -1.54367074e-24,
         8.34787712e-27, -2.53711116e-29,  3.35685250e-32]]

Main.sm = [ 59.51321215, 113.35577177,  58.70627679,  80.66267064]

Main.ssd = [[44.15017431,  9.94493352],
       [27.12617116,  7.74348089],
       [11.59016022,  6.5109571 ],
       [18.43266001,  8.3942871 ]]

Main.v0 = 11.17

Main.eval("prob = setup_problem(ssd, xp, yp, sm, uc; N=8, dt=0.2, radius=3., vel_control=true, vel_des = Main.v0)")
Main.eval("newton_solve!(prob)")


Main.eval("x, y, s, v = trajectory(prob.model, prob.pdtraj.pr)")
Np = Main.prob.model.p

import tikzplotlib

plt.figure()
for p in range(Np):
    plt.plot(Main.x[p], Main.y[p], marker='o')
plt.legend(["Vehicle %i"%(i) for i in range(1,Np+1)])
plt.xlim((1000, 1060))
plt.ylim((970, 1020))
#plt.savefig("./experiments/results/trajectory2.png")
tikzplotlib.save("./experiments/results/trajectory.tex")



plt.figure()
for p in range(Np):
    plt.plot(np.arange(0.0, 0.2*len(Main.v[p]), 0.2), Main.v[p], marker='o')
plt.xlabel("Time (s)")
plt.ylabel("Velocity (m/s)")
plt.legend(["Vehicle %i"%(i) for i in range(1,Np+1)])
plt.xlim((-.1, 1.6))
plt.ylim((5, 13))
#plt.savefig("./experiments/results/velocities2.png")
tikzplotlib.save("./experiments/results/velocities.tex")