import sys

import gym
from gym import wrappers, looger

class MyFactoryManagerAgent(object):

    def __init__(self, action_space):
        self.action_space = action_space
    
    def act(self, observation, reward, done):
        return self.action_space.sample()


if __name__ == "__main__":

    logger.set_level(logger.INFO)

    env = gym.make("scml-v0")
    
    outdir = '/tmp/random-agent-results'
    env = wrappers.Monitor(env, directory=outdir, force=True)
    env.seed(0)
    
    episode_count = 100
    reward = 0
    done = False

    for i in range(episode_count):
        ob = env.reset()