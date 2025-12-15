from opt_sim.N4S1 import N4S1
from opt_sim.N12S4 import N12S4


def get_problem(name):

    if name == "N4S1":
        return N4S1()
    elif name == "N12S4":
        return N12S4()
    else:
        raise ValueError(f"Unknown problem name: {name}")
