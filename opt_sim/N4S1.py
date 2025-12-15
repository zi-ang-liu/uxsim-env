from uxsim import *
import random


class N4S1:

    def __init__(self):
        self.name = "N4S1"
        self.n_var = 2  # number of variables

    def setup(self, signals):
        # check signals length
        assert len(signals) == 2, "signals should contain two elements."

        tmax = 3600

        # W.show_network(network_font_size=20, show_id=False)
        # simulation world
        W = World(
            name="N4S1",
            deltan=1,
            tmax=tmax,
            print_mode=0,
            save_mode=0,
            show_mode=0,
            random_seed=0,
            duo_update_time=600,
        )

        # scenario
        # merge network with signal
        N1 = W.addNode("orig1", 0, 0)
        N2 = W.addNode("orig2", 0, 2)
        # `signal` is a list of [duration of phase 0, duration of phase 1, ...]
        N3 = W.addNode("dest", 2, 1)
        I1 = W.addNode("merge", 1, 1, signal=signals)

        W.addLink("link1", "orig1", "merge", length=1000, signal_group=0)
        # if `signal_group` is 0, the exit of this link will be green at phase 0
        W.addLink("link2", "orig2", "merge", length=1000, signal_group=1)
        W.addLink("link3", "merge", "dest", length=1000)

        # W.adddemand("orig1", "dest", 0, 1000, 0.2)
        # W.adddemand("orig2", "dest", 500, 1000, 0.6)

        # random demand definition
        dt = 30
        demand = 0.22
        for t in range(0, tmax, dt):
            W.adddemand(N1, N3, t, t + dt, random.uniform(0, demand))
            W.adddemand(N2, N3, t, t + dt, random.uniform(0, demand))

        return W

    def evaluate(self, signals):

        W = self.setup(signals)

        # execute simulation
        W.exec_simulation()

        # results
        result = W.analyzer.basic_to_pandas()
        average_delay = result["average_delay"][0]

        return average_delay

    def analyze(self, x_opt):

        W = self.setup(x_opt)

        # execute simulation
        W.exec_simulation()

        W.analyzer.print_simple_stats()
        W.analyzer.time_space_diagram_traj_links(
            [["link1", "link3"], ["link2", "link3"]]
        )


if __name__ == "__main__":
    signals = [30, 60]  # duration of each phase in seconds
    problem = N4S1()
    result = problem.evaluate(signals)
    print("Average delay:", result)
    problem.analyze(signals)
