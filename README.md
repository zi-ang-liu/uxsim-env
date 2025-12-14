# UXsim-Env

This project is built on top of [UXsim](https://github.com/toruseo/UXsim), an open-source simulation framework available under the MIT License.

UXsim-Env is a Gymnasium environment that provides a simple interface for using UXsim in reinforcement learning tasks.

## Installation

To install the UXsim environment, run the following commands:

```{shell}
pip install -e .
```

## Benchmarks

- [N12S4-Env-v0](uxsim_env/envs/n12s4_env.py): A benchmark environment with 12 nodes and 4 signals.
- [N4S2-Env-v0](uxsim_env/envs/n4s2_env.py): A benchmark environment with 4 nodes and 2 signals.

## Usage

To use the UXsim environment, you can create an instance of the environment and interact with it using the Gymnasium API. Here's a simple example:

```python
import gymnasium as gym

env = gym.make("uxsim_env/N12S4-Env-v0")
```