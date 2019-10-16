import gym
from gym import error, spaces, utils
from gym.utils import seeding

class ScmlEnv(gym.Env):
    metadata = {'render.modes': ['factory_manager']}
    
    def __init__(self):
        pass
    
    def step(self, action):
        pass
    
    def reset(self):
        pass
    
    def render(self, mode='factory_manager'):
        pass
    
    def close(self):
        pass