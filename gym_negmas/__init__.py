from gym.envs.registration import register
from gym_negmas.envs import spaces

register(
    id='scml-v0',
    entry_point='gym_negmas.envs:ScmlEnv',
)

# numbers of step of Negotiation and normalizes between 0 and 1 
RLBOANegmasNegotiationSteps = 100

register(
    id='RLBOANegmasNegotiation-v0',
    entry_point='gym_negmas.envs:RLBOANegmasNegotiationEnv',
    kwargs={
        'observation_space':spaces.Dict(spaces={
            'ub(wat)':spaces.Discrete(10),
            'ub(wbt)':spaces.Discrete(10),
            'ub(wat-1)':spaces.Discrete(10),
            'ub(wbt-1)':spaces.Discrete(10),
            'time':spaces.Discrete(RLBOANegmasNegotiationSteps),
        }),
        'action_space':spaces.Discrete(3),
        'steps': RLBOANegmasNegotiationSteps
    }
)