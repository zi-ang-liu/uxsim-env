from gymnasium.envs.registration import register

register(
    id="uxsim_env/TrafficSimFourWay-v0",
    entry_point="uxsim_env.envs:TrafficSimFourWayEnv",
)
