from uxsim import *
import pandas as pd
import itertools
import random
import gymnasium as gym


class N4S1Env(gym.Env):
    def __init__(self):
        """
        traffic scenario: 1 signalized intersections as shown below:
                N1
                |
            W1--I1--E1

        Traffic demand is generated from each boundary node to all other boundary nodes.
        action: to determine which direction should have greenlight for every 10 seconds for single intersection. 2 actions.
            action 1: greenlight for I1: 0
            action 2: greenlight for I1: 1,
        state: number of waiting vehicles at each incoming link. 2 dimension.
        reward: negative of difference of total waiting vehicles
        """

        # action
        self.n_action = 2
        self.action_space = gym.spaces.Discrete(self.n_action)

        # state
        self.n_state = 2
        low = np.array([0 for i in range(self.n_state)])
        high = np.array([100 for i in range(self.n_state)])
        self.observation_space = gym.spaces.Box(low=low, high=high, dtype=np.int64)

        self.reset()

    def reset(self, seed=None, options=None):
        """
        reset the env
        """
        super().reset(seed=seed)

        W = World(
            name="",
            deltan=1,
            tmax=1200,
            print_mode=0,
            save_mode=0,
            show_mode=1,
            random_seed=seed,
            duo_update_time=600,
        )
        random.seed(seed)

        # network definition
        # scenario
        # merge network with signal
        N1 = W.addNode("orig1", 0, 0)
        N2 = W.addNode("orig2", 0, 2)
        I1 = W.addNode("merge", 1, 1, signal=[60, 60])
        # `signal` is a list of [duration of phase 0, duration of phase 1, ...]
        N3 = W.addNode("dest", 2, 1)
        W.addLink("link1", "orig1", "merge", length=1000, signal_group=0)
        # if `signal_group` is 0, the exit of this link will be green at phase 0
        W.addLink("link2", "orig2", "merge", length=1000, signal_group=1)
        W.addLink("link3", "merge", "dest", length=1000)

        # random demand definition
        dt = 30
        demand = 0.22
        for t in range(0, 3600, dt):
            W.adddemand(N1, N3, t, t + dt, random.uniform(0, demand))
            W.adddemand(N2, N3, t, t + dt, random.uniform(0, demand))

        # store UXsim object for later re-use
        self.W = W
        self.I1 = I1
        self.INLINKS = list(self.I1.inlinks.values())

        # initial observation
        observation = np.array([0 for i in range(self.n_state)])

        # log
        self.log_state = []
        self.log_reward = []

        # info
        info = {}

        return observation, info

    def comp_state(self):
        """
        compute the current state
        """
        vehicles_per_links = {}
        for l in self.INLINKS:
            vehicles_per_links[l] = (
                l.num_vehicles_queue
            )  # l.num_vehicles_queue: the number of vehicles in queue in link l
        return list(vehicles_per_links.values())

    def comp_n_veh_queue(self):
        return sum(self.comp_state())

    def step(self, action_index):
        """
        proceed env by 1 step = `operation_timestep_width` seconds
        """
        operation_timestep_width = 10

        n_queue_veh_old = self.comp_n_veh_queue()

        # change signal by action
        # decode action
        binstr = f"{action_index:04b}"
        i1, i2, i3, i4 = int(binstr[3]), int(binstr[2]), int(binstr[1]), int(binstr[0])
        self.I1.signal_phase = i1
        self.I1.signal_t = 0

        # traffic dynamics. execute simulation for `operation_timestep_width` seconds
        if self.W.check_simulation_ongoing():
            self.W.exec_simulation(duration_t=operation_timestep_width)

        # observe state
        observation = np.array(self.comp_state())

        # compute reward
        n_queue_veh = self.comp_n_veh_queue()
        reward = -(n_queue_veh - n_queue_veh_old)

        # check termination
        done = False
        if self.W.check_simulation_ongoing() == False:
            done = True

        # log
        self.log_state.append(observation)
        self.log_reward.append(reward)

        # info
        if done:
            average_delay = self.W.analyzer.average_delay
        else:
            average_delay = None

        info = {"average_delay": average_delay}

        # terminated
        terminated = done

        return observation, reward, terminated, False, info
