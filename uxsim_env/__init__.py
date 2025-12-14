from gymnasium.envs.registration import register

register(
    id="uxsim_env/N12S4-Env-v0",
    entry_point="uxsim_env.envs:N12S4Env",
)

register(
    id="uxsim_env/N4S1-Env-v0",
    entry_point="uxsim_env.envs:N4S1Env",
)
