from uxsim import *
import random
import itertools


class N12S4:

    def __init__(self):
        self.name = "N12S4"
        self.n_var = 8  # number of variables

    def setup(self, signals):
        # check signals length
        assert len(signals) == 8, "signals length must be 8"

        tmax = 9000

        W = World(
            name="N12S4",
            deltan=5,
            tmax=tmax,
            print_mode=0,
            save_mode=0,
            show_mode=0,
            duo_update_time=600,
        )

        # network definition
        I1 = W.addNode("I1", 0, 0, signal=[signals[0], signals[1]])
        I2 = W.addNode("I2", 1, 0, signal=[signals[2], signals[3]])
        I3 = W.addNode("I3", 0, -1, signal=[signals[4], signals[5]])
        I4 = W.addNode("I4", 1, -1, signal=[signals[6], signals[7]])
        W1 = W.addNode("W1", -1, 0)
        W2 = W.addNode("W2", -1, -1)
        E1 = W.addNode("E1", 2, 0)
        E2 = W.addNode("E2", 2, -1)
        N1 = W.addNode("N1", 0, 1)
        N2 = W.addNode("N2", 1, 1)
        S1 = W.addNode("S1", 0, -2)
        S2 = W.addNode("S2", 1, -2)

        # E <-> W direction: signal group 0
        for n1, n2 in [[W1, I1], [I1, I2], [I2, E1], [W2, I3], [I3, I4], [I4, E2]]:
            W.addLink(n1.name + n2.name, n1, n2, length=500, signal_group=0)
            W.addLink(n2.name + n1.name, n2, n1, length=500, signal_group=0)
        # N <-> S direction: signal group 1
        for n1, n2 in [[N1, I1], [I1, I3], [I3, S1], [N2, I2], [I2, I4], [I4, S2]]:
            W.addLink(n1.name + n2.name, n1, n2, length=500, signal_group=1)
            W.addLink(n2.name + n1.name, n2, n1, length=500, signal_group=1)

        # W.show_network(network_font_size=15, show_id=False)

        # random demand definition
        dt = 30
        demand = 0.19
        for n1, n2 in itertools.permutations([W1, W2, E1, E2, N1, N2, S1, S2], 2):
            for t in range(0, tmax, dt):
                W.adddemand(n1, n2, t, t + dt, random.uniform(0, demand))

        return W

    def evaluate(self, x):

        W = self.setup(x)

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
        # W.analyzer.time_space_diagram_traj_links(
        #     [["link1", "link3"], ["link2", "link3"]]
        # )


if __name__ == "__main__":
    signals = [60, 60, 60, 60, 60, 60, 60, 60]
    problem = N12S4()
    avg_delay = problem.evaluate(signals)
    print(f"Average delay: {avg_delay} sec")
    problem.analyze(signals)
