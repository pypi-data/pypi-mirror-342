"""
This is a basic agent class for MetaBBO agents. All agents should inherit from this class.
Your own agent should have the following methods:
    1. __init__(self, config) : to initialize the agent
    2. train_episode(self, env, epoch_id, logger) : to train the agent for an episode by using env.reset() and
       env.step() to interact with environment. It's expected to return a Tuple[bool, dict] whose first element
       indicates whether the learned step has exceeded the max_learning_step and second element is a dictionary
       that contains:
       { 'normalizer' : the best cost in initial population.
         'gbest' : the best cost found in this episode.
         'return' : total reward in this episode.
         'learn_steps' : the number of accumulated learned steps of the agent.
       }
    3. rollout_episode(self, env, epoch_id, logger) : to rollout the agent for an episode by using env.reset() and
       env.step() to interact with environment. It's expected to return a dictionary that contains:
       { 'cost' : a list of costs that need to be maintained in backbone optimizer. See learnable_optimizer.py for more details.
         'fes' : times of function evaluations used by optimizer.
         'return' : total reward in this episode.
       }
"""

from typing import Tuple
from typing import Optional, Union, Literal
class Basic_Agent:
    def __init__(self, config):
        self.__config = config


    def update_setting(self, config):
        pass

    def train_episode(self,
                      env,
                      seeds: int) -> Tuple[bool, dict]:
        raise NotImplementedError

    def rollout_episode(self,
                        env) -> dict:
        raise NotImplementedError

    def train_epoch(self):
        pass

    def set_network(self, networks: dict, learning_rates: int):
        pass

    def get_step(self):
        pass

    @classmethod
    def log_to_tb_train(self):
        pass
