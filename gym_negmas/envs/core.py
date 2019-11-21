import gym
from gym import error, spaces, utils
from gym.utils import seeding
from copy import copy, deepcopy
from retrying import retry
import gym_negmas
from gym_negmas.envs.negmas_manager import Instance

class RLBOANegmasNegotiationEnv(gym.Env):
    """
    Env used for autonomous negotiation in framwork RLBOA
    """

    metadata = {'render.modes': ['human', 'rgb_array']}
    reward_range = (-float('inf'), float('inf')) 
    spec = """
    reinforcement learning framwork for autonomous negotiation, 
    implemente this framwork with python adn openai gym 
    in simulator Negmas. 
    """

    def __init__(
        self, 
        observation_space, 
        action_space,
        steps,
        noop_action=None
    ):
        """
        :params: observation_sapce: utility value of every outcome as activation space
        :params: action_space: go up, go down, stay in the current bin.
        "params: steps
        """
        self.observation_space = None
        self.action_space = None
        self.steps = steps
        # need to normalize the time into interval [0, 1]
        self.time_step = 1 / steps
        self.resets = 0
        self._default_action = noop_action

        self._setup_spaces(observation_space, action_space)
    
    def _setup_spaces(
        self, 
        observation_space, 
        action_space
    ):
        self.observation_space = observation_space
        self.action_space = action_space
        
        # here consided action_space as a 3 values Discrete {0, 1, 2}, means {"go_up", "go_down", "stay"}
        if self._default_action is None:
            if isinstance(action_space, gym_negmas.envs.spaces.Dict):
                self._default_action = action_space.no_op()
    
    @property
    def noop_action(
        self
    ):
        """
        return the _default_action
        """
        return deepcopy(self._default_action)
    
    def init(self):
        """
        Initializes the RLBOANegmasNegotiationEnv, 
        means here setup  negotiation/mechanism of negmas
        """
        self.instance = Instance(
            checkpoint_folder = "./tmp",
            checkpoint_filename = "mechanism",
        )

    def step(self, action):
        """
        call step in checkpoints in Negmas,
        Action space as[
            []
        ]
        here action is the call the function of negotiator that 
        """
        next_state, reward, done = self.instance.step(action)
        return next_state, reward, done
    
    def reset(self):
        """
        call reset function in checkpoints in negmas
        """
        pass
    
    def seed(self, seed=None):
        """
        set seed for random generator
        """
        assert isinstance(seed, int), "Seed must be an int!"
        self._seed = seed
    
    @retry
    def _start_up(self):
        pass

    def render(self, mode='human'):
        """
        Here Can Use pyglet to implemnte a pure visulization of Process,
        return some information every frame
        """
        pass

class ScmlEnv(gym.Env):
    metadata = {'render.modes': ['human']}
    
    def __init__(self):
        pass
    
    def step(self, action):
        pass
    
    def reset(self):
        pass
    
    def render(self, mode='human'):
        pass
    
    def close(self):
        pass