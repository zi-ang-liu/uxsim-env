from uxsim import *


def evaluate_N4S1(signals):

    # check signals length
    assert len(signals) == 2, "signals should contain two elements."

    # simulation world
    W = World(
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
    W.addNode("orig1", 0, 0)
    W.addNode("orig2", 0, 2)
    W.addNode("merge", 1, 1, signal=signals)
    # `signal` is a list of [duration of phase 0, duration of phase 1, ...]
    W.addNode("dest", 2, 1)
    W.addLink("link1", "orig1", "merge", length=1000, signal_group=0)
    # if `signal_group` is 0, the exit of this link will be green at phase 0
    W.addLink("link2", "orig2", "merge", length=1000, signal_group=1)
    W.addLink("link3", "merge", "dest", length=1000)

    # W.show_network(network_font_size=20, show_id=False)

    W.adddemand("orig1", "dest", 0, 1000, 0.2)
    W.adddemand("orig2", "dest", 500, 1000, 0.6)

    # execute simulation
    W.exec_simulation()

    # results
    result = W.analyzer.basic_to_pandas()
    average_delay = result["average_delay"][0]

    return average_delay


if __name__ == "__main__":
    signals = [30, 60]  # duration of each phase in seconds
    delay = evaluate_N4S1(signals)
    print(f"Signals: {signals}, Average Delay: {delay}")
