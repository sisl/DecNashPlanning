function vehicle_paths(x_coefs::Vector{N}, y_coefs::Vector{N}, 
        s_max::AbstractVector; T=Float64) where {N <: AbstractVector}
    """
    Take in path coefficients as they are passed from python and convert to a list of VehiclePaths.
    """
    
    @assert length(x_coefs) == length(y_coefs) == length(s_max) "nplayers path mismatch"
    @assert length(x_coefs[1]) == length(y_coefs[1]) "ncoefs path mismatch"
    
    P = length(x_coefs)
    D = length(x_coefs[1])
    paths = [VehiclePath(SVector{D,T}(x_coefs[i]), SVector{D}(y_coefs[i]), s_max[i]) for i = 1:P]
    return paths
end

function vehicle_paths(x_coefs::AbstractMatrix, y_coefs::AbstractMatrix, 
        s_max::AbstractVector; T=Float64)
    """
    Take in path coefficients as they are passed from python and convert to a list of VehiclePaths.
    """
    
    @assert size(x_coefs)[1] == size(y_coefs)[1] == length(s_max) "nplayers path mismatch"
    @assert size(x_coefs)[2] == size(y_coefs)[2] "ncoefs path mismatch"
    
    P,D = size(x_coefs)
    paths = [VehiclePath(SVector{D,T}(x_coefs[i,:]), SVector{D}(y_coefs[i,:]), s_max[i]) for i = 1:P]
    return paths
end

function initial_state(paths::Vector{VehiclePath{M}}, s_sdot::Vector{N}) where {N <: AbstractVector, M}
    """
    Take in initial s and sdot as they are passed from python and convert to an initial state
    """
    @assert length(paths) == length(s_sdot) "nplayers initial state mismatch"
    P = length(paths)
    T = eltype(paths[1].s_max)
    
    s = SVector{P,T}([s_sdot[i][1] for i=1:P])
    v = SVector{P,T}([s_sdot[i][2] for i=1:P])
    xs = SVector{P,T}([powerseries(paths[i].x_coefs, s[i]) for i=1:P]) 
    ys = SVector{P,T}([powerseries(paths[i].y_coefs, s[i]) for i=1:P])
    return SVector{4P,T}(xs..., ys..., s..., v...)
end

function initial_state(paths::Vector{VehiclePath{M}}, s_sdot::AbstractMatrix) where {M}
    """
    Take in initial s and sdot as they are passed from python and convert to an initial state
    """
    @assert length(paths) == size(s_sdot)[1] "nplayers initial state mismatch"
    P = length(paths)
    T = eltype(paths[1].s_max)
    
    s = SVector{P,T}([s_sdot[i,1] for i=1:P])
    v = SVector{P,T}([s_sdot[i,2] for i=1:P])
    xs = SVector{P,T}([powerseries(paths[i].x_coefs, s[i]) for i=1:P]) 
    ys = SVector{P,T}([powerseries(paths[i].y_coefs, s[i]) for i=1:P])
    return SVector{4P,T}(xs..., ys..., s..., v...)
end

function final_state(paths::Vector{VehiclePath{M}}) where {M}
    """
    Generate final state as s=paths.smax and v=0 
    """
    P = length(paths)
    T = eltype(paths[1].s_max)
    s = SVector{P}([path.s_max for path in paths])
    v = zeros(SVector{P,T})
    
    
    xf = [SVector{4,T}(powerseries(paths[i].x_coefs, paths[i].s_max),
            powerseries(paths[i].y_coefs, paths[i].s_max), 
            paths[i].s_max, 0.) for i = 1:P]
    return xf
end

function setup_problem(ssdot, xpoly, ypoly, smax, uc::Int; N::Int=20, 
        dt::AbstractFloat=0.1, q::AbstractFloat=10., r::AbstractFloat=0.1,
        a_lower::AbstractFloat=-4.5, a_upper::AbstractFloat=1.5, radius::AbstractFloat = 4.,
        vel_control::Bool=false, vel_des::AbstractFloat=Inf,
        solver_opts::Options=Options(inner_print=false,outer_print=false))
    """
    Generate roundabout problem
    """
    
    # Set Up RoundaboutGame
    T = Float64
    paths = vehicle_paths(xpoly, ypoly, 1.0*smax; T=T)
    x0 = initial_state(paths, ssdot)

    model = RoundaboutGame(paths, uc)
    p, n, m = model.p, model.n, model.m

    # Define Problem Size
    probsize = ProblemSize(N, model)

    # Define the objective of each player
    # We use a LQR cost
    
    # State Cost
    if vel_control # velocity target
        @assert 0. <= vel_des < Inf "desired velocity invalid"
        xf = [SVector{4,T}(0., 0., 0., vel_des) for i=1:p]
        Q = [Diagonal(q*SVector{model.ni[i],T}(0,0,0,1)) for i=1:p] # Quadratic state cost
    else # final state target
        xf = [SVector{4,T}(0., 0., paths[i].s_max, 0.) for i=1:p]
        Q = [Diagonal(q*SVector{model.ni[i],T}(0,0,1,0)) for i=1:p] # Quadratic state cost
    end
    
    # Control Cost
    uf = [zeros(SVector{model.mi[i],T}) for i=1:p]
    R = [Diagonal(r*ones(SVector{model.mi[i],T})) for i=1:p] # Quadratic control cost

    # Objectives of the game
    game_obj = GameObjective(Q,R,xf,uf,N,model)

    # Define the constraints that each player must respect
    game_con = GameConstraintValues(probsize)

    # Add collision avoidance
    add_collision_avoidance!(game_con, radius)

    # Add control bounds
    u_max = [a_upper*ones(SVector{m-model.uc,T}); zeros(SVector{model.uc,T})]
    u_min = [a_lower*ones(SVector{m-model.uc,T}); zeros(SVector{model.uc,T})]

    add_control_bound!(game_con, u_max, u_min)

    # Add velocity bounds ## TODO

    # Add control constraint on final $uc players ## TODO (currently doing with u_max=u_min=0)

    # Define the game problem
    prob = GameProblem(N,dt,x0,model,solver_opts,game_obj,game_con);
    return prob
end
