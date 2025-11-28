# UXsim-Env

This project is built on top of [UXsim](https://github.com/toruseo/UXsim), an open-source simulation framework available under the MIT License.

UXsim-Env is a Gymnasium environment that provides a simple interface for using UXsim in reinforcement learning tasks.

## Installation

To install the UXsim environment, run the following commands:

```{shell}
pip install -e .
```

## Usage

To use the UXsim environment, you can create an instance of the environment and interact with it using the Gymnasium API. Here's a simple example:

```python
import gymnasium as gym

env = gym.make("uxsim_env/TrafficSimFourWay-v0")
```