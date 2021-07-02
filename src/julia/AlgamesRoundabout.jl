#__precompile__(false)

module AlgamesRoundabout

greet() = print("Hello World!")

using Algames
using StaticArrays
using LinearAlgebra
using RobotDynamics 
using Plots

# Dynamics
export
    VehiclePath,
    RoundaboutGame,
    dynamics
include("dynamics.jl")

# Game Problem Initialization
export
    setup_problem,
    Options
include("initialization.jl")

# Solver functions
export
    action,
    newton_solve!,
    controls, 
    state
include("solve.jl")

# Plotting
export
    plot_trajectory!,
    trajectory
include("plot.jl")

end