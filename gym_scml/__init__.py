from gym.envs.registration import register

register(
    id='scml-v0',
    entry_point='gym_scml.envs:ScmlEnv',
)