import gymnasium as gym
from uxsim_env.envs.N12S4_Env import N12S4Env
from uxsim_env.envs.N4S1_Env import N4S1Env
from stable_baselines3 import PPO

from stable_baselines3.common.callbacks import BaseCallback


class AverageDelayCallback(BaseCallback):
    def __init__(self, verbose=0):
        super().__init__(verbose)

    def _on_step(self) -> bool:
        # infos is a list (one per environment in VecEnv)
        infos = self.locals["infos"]

        for info in infos:
            # Your env sets "average_delay" only when done=True
            if "average_delay" in info and info["average_delay"] is not None:
                self.logger.record("custom/average_delay", info["average_delay"])

        return True


env = gym.make("uxsim_env/N12S4-Env-v0")
# env = gym.make("uxsim_env/N4S1-Env-v0")
obs, info = env.reset()
for _ in range(10):
    action = env.action_space.sample()
    obs, reward, terminated, truncated, info = env.step(action)
    if terminated or truncated:
        print(
            f"Action: {action}, Reward: {reward}, Average Delay: {info['average_delay']}"
        )
        obs, info = env.reset()

# Example of training a PPO agent
model = PPO("MlpPolicy", env, verbose=1, tensorboard_log="./ppo_uxsim_tensorboard/")
model.learn(total_timesteps=1000000, callback=AverageDelayCallback())
model.save("ppo_uxsim_traffic_sim_four_way")
