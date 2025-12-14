import optuna
from opt_sim.N4S1 import evaluate_N4S1
from opt_sim.N12S4 import evaluate_N12S4

# test small case


def objective(trial):
    x1 = trial.suggest_float("x1", 10, 70)
    x2 = trial.suggest_float("x2", 10, 70)
    x = [x1, x2]
    res = evaluate_N4S1(x)
    return res


study = optuna.create_study()
study.optimize(objective, n_trials=10)

study.best_params


# test medium case


def objective(trial):
    x1 = trial.suggest_float("x1", 10, 70)
    x2 = trial.suggest_float("x2", 10, 70)
    x3 = trial.suggest_float("x3", 10, 70)
    x4 = trial.suggest_float("x4", 10, 70)
    x5 = trial.suggest_float("x5", 10, 70)
    x6 = trial.suggest_float("x6", 10, 70)
    x7 = trial.suggest_float("x7", 10, 70)
    x8 = trial.suggest_float("x8", 10, 70)
    x = [x1, x2, x3, x4, x5, x6, x7, x8]
    res = evaluate_N12S4(x)
    return res


study = optuna.create_study()
study.optimize(objective, n_trials=10)

study.best_params
