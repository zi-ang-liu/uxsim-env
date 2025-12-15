from opt_sim.N4S1 import N4S1


def get_problem(name):

    if name == "N4S1":
        return N4S1()
    else:
        raise ValueError(f"Unknown problem name: {name}")
