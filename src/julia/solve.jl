function action(prob::GameProblem; time=false)
    """
       Solve problem and return array of one-step actions
    """
    
    if time
        @time newton_solve!(prob)
    else
        newton_solve!(prob)
    end
    u = controls(prob.pdtraj.pr)
    return u[1]
end