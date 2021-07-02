struct VehiclePath{N}
    x_coefs::AbstractVector
    y_coefs::AbstractVector
    s_max::AbstractFloat
    function VehiclePath(x_coefs::AbstractVector, y_coefs::AbstractVector, s_max::AbstractFloat)
        @assert length(x_coefs)==length(y_coefs) "Path length mismatch"
        N = length(x_coefs)
        new{N}(x_coefs, y_coefs, s_max)
    end
end

# Define the dynamics model of the model.
struct RoundaboutGame{N,M,P,SVu,SVx,SVz} <: AbstractGameModel
    n::Int  # Number of states
    m::Int  # Number of controls
    p::Int  # Number of players
    ni::Vector{Int}  # Number of states for each player
    mi::Vector{Int}  # Number of controls for each player
    pu::SVu # Indices of the each player's controls
    px::SVx # Indices of the each player's x and y positions
    pz::SVz # Indices of the each player's states
    
    paths::Vector{<:VehiclePath} # List of Path objects for each vehicle
    uc::Int # Number of uncontrolled players (default at the end of the player list) 
end

function RoundaboutGame(paths::Vector{VehiclePath{N}}, uc::Int) where {N}
    # p = number of players
    p = length(paths)
    n = 4p
    m = p
    pu = [SVector{1,Int}([i]) for i=1:p]
    px = [SVector{2,Int}([i + (j-1)*p for j=1:2]) for i=1:p]
    pz = [SVector{4,Int}([i + (j-1)*p for j=1:4]) for i=1:p]
    TYPE = typeof.((pu,px,pz))
    ni = 4*ones(Int,p)
    mi = 1*ones(Int,p)
    return RoundaboutGame{n,m,p,TYPE...}(n,m,p,ni,mi,pu,px,pz,paths,uc)
end

#@generated function RobotDynamics.dynamics(model::UnicycleGame{N,M,P}, x, u) where {N,M,P}
#    xd  = [:(cos(x[$i])*x[$i+P]) for i=M+1:M+P]
#    yd  = [:(sin(x[$i])*x[$i+P]) for i=M+1:M+P]
#    qdd = [:(u[$i]) for i=1:M]
#    return :(SVector{$N}($(xd...), $(yd...), $(qdd...)))
#end

function powerseries(coefs::AbstractVector, s)
    maxd = length(coefs)-1 
    ss = SVector{maxd+1}([s^i for i=0:maxd])
    return dot(coefs, ss)
end

function powerseriesd(coefs::AbstractVector, s, v)
    maxd = length(coefs)-1 
    ss = SVector{maxd+1}([i*s^(i-1) for i=0:maxd])
    return v*dot(coefs, ss)
end

function RobotDynamics.discrete_dynamics(::Type{PassThrough}, model::RoundaboutGame{N,M,P},
        x::StaticVector, u::StaticVector, t, dt) where {N,M,P}
    
    sidxs = SVector{P}([i for i=(2P+1):3P])
    st = x[sidxs]
    vt = x[sidxs.+P]
    
    vn = vt + u*dt
    sn = st + dt*(vt+vn)/2
    
    xn = SVector{P}([powerseries(model.paths[i].x_coefs, sn[i]) for i=1:P])
    yn = SVector{P}([powerseries(model.paths[i].y_coefs, sn[i]) for i=1:P])
    return SVector{N}(xn..., yn..., sn..., vn...)  
end

function RobotDynamics.dynamics(model::RoundaboutGame{N,M,P}, x, u) where {N,M,P}
    sidxs = SVector{P}([i for i=(2P+1):3P])
    st = x[sidxs]
    vt = x[sidxs.+P]
    
    vd = u
    sd = vt
    
    xd = SVector{P}([powerseriesd(model.paths[i].x_coefs, st[i], vt[i]) for i=1:P])
    yd = SVector{P}([powerseriesd(model.paths[i].y_coefs, st[i], vt[i]) for i=1:P])
    return SVector{N}(xd..., yd..., sd..., vd...)  
end

