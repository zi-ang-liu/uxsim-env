import optuna
from opt_sim.get_problem import get_problem
from plotly.io import show

# test small case
# problem = get_problem("N4S1")
problem = get_problem("N12S4")
n_var = problem.n_var


def objective(trial):
    x = []
    for i in range(1, n_var + 1):
        vars()["x" + str(i)] = trial.suggest_float("x" + str(i), 10, 70)
        x.append(vars()["x" + str(i)])
    res = problem.evaluate(x)
    return res


sampler = optuna.samplers.GPSampler()
study = optuna.create_study(sampler=sampler)
study.optimize(objective, n_trials=50)

study.best_params

x_opt = [study.best_params["x" + str(i)] for i in range(1, n_var + 1)]
res_opt = problem.evaluate(x_opt)


fig = optuna.visualization.plot_optimization_history(study)
show(fig)

problem.analyze(x_opt)
