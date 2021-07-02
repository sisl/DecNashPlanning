# Visualize the Results
function plot_trajectory!(plt, model::AbstractGameModel, traj::Algames.Traj)
    plot!(plt, legend=false, aspect_ratio=:equal)
    N = length(traj)
    for i = 1:model.p
        xi = [Algames.state(traj[k])[model.pz[i][1]] for k=1:N]
        yi = [Algames.state(traj[k])[model.pz[i][2]] for k=1:N]
        plot!(xi, yi, label=false)
        scatter!(xi, yi)
    end
    return nothing
end

# Return state information
function trajectory(model::AbstractGameModel, traj::Algames.Traj)
    N = length(traj)
    x = [[Algames.state(traj[k])[model.pz[i][1]] for k=1:N] for i = 1:model.p]
    y = [[Algames.state(traj[k])[model.pz[i][2]] for k=1:N] for i = 1:model.p]
    s = [[Algames.state(traj[k])[model.pz[i][3]] for k=1:N] for i = 1:model.p]
    v = [[Algames.state(traj[k])[model.pz[i][4]] for k=1:N] for i = 1:model.p]
    return x, y, s, v
end
