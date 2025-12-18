import numpy as np
import matplotlib.pyplot as plt

from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.soo.nonconvex.de import DE
from pymoo.optimize import minimize
from pymoo.operators.sampling.lhs import LHS

from opt_sim.get_problem import get_problem


class uxsim_problem(ElementwiseProblem):
    def __init__(self, problem):
        n_var = problem.n_var
        xl = np.array([10.0] * n_var)
        xu = np.array([70.0] * n_var)
        super().__init__(n_var=n_var, n_obj=1, n_constr=0, xl=xl, xu=xu)
        self.problem = problem

    def _evaluate(self, x, out, *args, **kwargs):
        x = x.tolist()
        out["F"] = self.problem.evaluate(x)


if __name__ == "__main__":
    problem = get_problem("N4S1")
    # problem = get_problem("N12S4")
    problem = uxsim_problem(problem)

    algorithm = DE(
        pop_size=10,
        sampling=LHS(),
        variant="DE/rand/1/bin",
        CR=0.3,
        dither="vector",
        jitter=False,
    )

    res = minimize(
        problem,
        algorithm,
        seed=1,
        verbose=True,
        termination=("n_gen", 20),
        save_history=True,
    )

    print("Best solution found: \nX = %s\nF = %s" % (res.X, res.F))

    n_evals = np.array([e.evaluator.n_eval for e in res.history])
    opt = np.array([e.opt[0].F for e in res.history])

    plt.title("Convergence")
    plt.plot(n_evals, opt, "--")
    plt.show()
