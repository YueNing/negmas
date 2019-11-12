import gym
import gym.spaces
from collections import OrderedDict

class Dict(gym.spaces.Dict):
    def no_op(self):
        return OrderedDict([(k, space.no_op()) for k, space in self.spaces.items()])

class Discrete(gym.spaces.Discrete):
    def no_op(self):
        return None
