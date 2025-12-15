from uxsim import *


class N4S1:

    def __init__(self):
        self.name = "N4S1"

    def evaluate(self, signals):

        # check signals length
        assert len(signals) == 2, "signals should contain two elements."

        # W.show_network(network_font_size=20, show_id=False)
        # simulation world
        self.W = World(
            name="N4S1",
            deltan=1,
            tmax=1200,
            print_mode=1,
            save_mode=1,
            show_mode=1,
            random_seed=0,
        )

        # scenario
        # merge network with signal
        self.W.addNode("orig1", 0, 0)
        self.W.addNode("orig2", 0, 2)
        # `signal` is a list of [duration of phase 0, duration of phase 1, ...]
        self.W.addNode("dest", 2, 1)
        self.W.addNode("merge", 1, 1, signal=signals)

        self.W.addLink("link1", "orig1", "merge", length=1000, signal_group=0)
        # if `signal_group` is 0, the exit of this link will be green at phase 0
        self.W.addLink("link2", "orig2", "merge", length=1000, signal_group=1)
        self.W.addLink("link3", "merge", "dest", length=1000)

        self.W.adddemand("orig1", "dest", 0, 1000, 0.2)
        self.W.adddemand("orig2", "dest", 500, 1000, 0.6)

        # execute simulation
        self.W.exec_simulation()

        # results
        result = self.W.analyzer.basic_to_pandas()
        average_delay = result["average_delay"][0]

        return average_delay

    def analyze(self, x_opt):
        self.W = World(
            name="N4S1",
            deltan=1,
            tmax=1200,
            print_mode=1,
            save_mode=1,
            show_mode=1,
            random_seed=0,
        )

        # scenario
        # merge network with signal
        self.W.addNode("orig1", 0, 0)
        self.W.addNode("orig2", 0, 2)
        # `signal` is a list of [duration of phase 0, duration of phase 1, ...]
        self.W.addNode("dest", 2, 1)
        self.W.addNode("merge", 1, 1, signal=x_opt)

        self.W.addLink("link1", "orig1", "merge", length=1000, signal_group=0)
        # if `signal_group` is 0, the exit of this link will be green at phase 0
        self.W.addLink("link2", "orig2", "merge", length=1000, signal_group=1)
        self.W.addLink("link3", "merge", "dest", length=1000)

        self.W.adddemand("orig1", "dest", 0, 1000, 0.2)
        self.W.adddemand("orig2", "dest", 500, 1000, 0.6)

        # execute simulation
        self.W.exec_simulation()

        self.W.analyzer.print_simple_stats()
        self.W.analyzer.time_space_diagram_traj_links(
            [["link1", "link3"], ["link2", "link3"]]
        )


if __name__ == "__main__":
    signals = [30, 60]  # duration of each phase in seconds
    res = N4S1.evaluate(signals)
    print(f"Average delay: {res} seconds")
