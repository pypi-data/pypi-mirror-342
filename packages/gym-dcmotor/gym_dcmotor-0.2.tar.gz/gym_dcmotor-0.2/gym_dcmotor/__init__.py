from gymnasium.envs.registration import register

register(
    id='DCMotor-v0',
    entry_point='gym_dcmotor.envs:DCMotor',
    max_episode_steps=200,
)