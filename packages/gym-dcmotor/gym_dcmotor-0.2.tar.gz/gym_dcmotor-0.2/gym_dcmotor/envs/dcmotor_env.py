import os
import numpy as np
import gymnasium as gym
from typing import Optional, Dict
from gymnasium import spaces
from gymnasium_robotics import GoalEnv
import matplotlib.pyplot as plt

from .numapp import RK45


class DCMotor(GoalEnv):
    metadata = {'render_modes': ['human']}

    #It might be cool to make this a gym env but not at the moment.
    def __init__(self, reward_type='dense', continuing_task=True, steady_state=True, sparse_scalar=1., tolerance = 0.1):
        #Motor Constants
        self.configure()
        self._step_size = 0.5
        self._stepper = RK45(self._kinematic_equation, self._step_size, 1e-4)
        self._t = 0
        self._state = None
        self._rend = None
        self._render_vars = None
        self._reward_type = reward_type
        self._continuing_task = continuing_task
        self._sampler = None
        self._steady_state = steady_state
        self._sparse_scalar = sparse_scalar
        self._goal = None
        self._steps_close = 0
        self._steps_close_linalg = None
        self._tolerance = tolerance

    # def set_sampler(self, sampler):
    #     self._sampler = sampler

    # def get_sampler(self):
    #     return self._sampler

    def configure(self,J=0.01,B=0.1,Kb=0.01,Kt=0.01,Ra=1.,La=0.5, Tl=0,\
                 max_Va=24,max_Tl=0):
        self._J = J
        self._B = B
        self._Kb = Kb
        self._Kt = Kt
        self._Ra = Ra
        self._La = La
        self._Tl = Tl
        self._calc_observation_limits(max_Va, max_Tl)
        self._observation_space()
        self._action_space(max_Va)

    def set_step_size(self, step_size):
        self._step_size = step_size

    def get_time(self):
        return self._t

    def step(self, action, *args, **kwargs):
        info = {}
        action = action.reshape(self.action_space.shape)
        if self._state is None:
            return self.reset()
        tbound = self._t + self._step_size
        while self._t < tbound:
            prev_state = self._state['observation']
            current_state, self._t = self._stepper.step(prev_state,self._t,\
                                                     tbound,Va=action[0])
        reward = self.compute_reward(current_state, self._goal, info, prev_state)
        info['steps_close'] = self._steps_close
        info['success'] = self._steps_close > 10
        terminated = self.compute_terminated(current_state, self._goal, info)
        truncated = self.compute_truncated(current_state, self._goal, info)
        assert self._t == tbound
        self._render_vars = np.vstack((self._render_vars,\
                                       np.hstack((current_state,self._t))))
        self._state = self._get_obs(current_state)
        return self._state, reward, terminated, truncated, info

    def reset(self,
        *,
        seed: Optional[int] = None,
        options: Optional[Dict[str, Optional[np.ndarray]]] = None,
        ):

        #Motor can start absolutly anywhere in the space
        self._stepper.reset()
        self._t = 0
        self._rend = None
        self._render_vars = None
        start_state = self.observation_space['observation'].sample()
        start_state[0] = (self._B * start_state[1] + self._Tl) / self._Kt
        self._render_vars = np.asarray([np.hstack((start_state, self._t))])
        # self.set_goal(start_state)
        self._state = self._get_obs(start_state)
        return self._state, {}

    # def set_goal(self, obs=None, goal=None):
    #     if goal is None:
    #         if self._sampler is None:
    #             self._goal = self.observation_space['desired_goal'].sample()
    #         else:
    #             if obs is None:
    #                 raise ValueError('Observation must be provided if sampler is used')
    #             # can't do this here becuse it is not using the wrapped envs so the transform is not occuring.
    #             # but also kinda want to do it here so the samplers should also do I guess.
    #             self._goal = self._sampler.sample(obs)
    #     else:
    #         self._goal = goal

    def set_goal(self, goal):
        self._goal = goal
        
    def _get_obs(self, state):
        return dict(observation=state.copy(),
                     desired_goal=self._goal.copy() if self._goal else state[1:].copy(), 
                     achieved_goal=state[1:].copy()
                    )

    def render(self):
        if self._rend is None:
            self._render_init()
        self._plot_render_vars()
        plt.pause(0.01)

    def save_render(self, epoch, render_des, path):
        """
        As this is not a default function for envs 
        it should probably be removed
        """
        if self._rend is None:
            self._render_init()
        check_create_directory(path)
        self._fig.suptitle("Behaviour at epoch #{}".format(epoch), fontsize=25)
        self._plot_render_vars()
        self._axarr[1].plot(self._render_vars[:, 2],
                            render_des[:, 1],
                            c='r',
                            linestyle="--")
        self._axarr[0].plot(self._render_vars[:, 2],
                            render_des[:, 0],
                            c='r',
                            linestyle="--")
        self._fig.savefig(path + "epoch#{}.png".format(epoch),
                          bbox_inches="tight")

    def set_evaluate(self):
        pass
    
    def unset_evaluate(self):
        pass

    def compute_reward(self, state, des_state, info, prev_state=None, w=[0.1,0.001,0.00001]):
        distance = np.linalg.norm(state[1:] - des_state) < self._tolerance*self._omega_max
        self._steps_close = self._steps_close + 1 if distance else 0      
        info['success'] = distance
        if self._reward_type == 'dense':
            raw_proportional_error = np.abs(state[1:] - des_state)
            info['raw_proportional_error'] = raw_proportional_error
            cost = -w[0]*raw_proportional_error**2
            if prev_state is not None:
                raw_derivative_error = np.abs(state[1:] - prev_state[1])
                info['raw_derivative_error'] = raw_derivative_error
                cost -= w[1] * raw_derivative_error**2
            return cost.astype(np.float64)[0]
        elif self._reward_type == 'sparse':
            return distance.astype(np.float64)*self._sparse_scalar
        
    def linalg_compute_reward(self, state, des_state, info, prev_state=None, w=[0.1,0.001,0.00001]):
        distance = np.linalg.norm(state[:, 1:] - des_state, axis = 1) < self._tolerance*self._omega_max
        if self._steps_close_linalg is None:
            self._steps_close_linalg = np.zeros_like(distance)
        self._steps_close_linalg = self._steps_close_linalg + distance
        # self._steps_close = self._steps_close + 1 if distance else 0      
        info['success'] = self._steps_close_linalg > 1
        if self._reward_type == 'dense':
            raw_proportional_error = np.abs(state[:, 1:] - des_state)
            info['raw_proportional_error'] = raw_proportional_error
            cost = -w[0]*raw_proportional_error**2
            if prev_state is not None:
                raw_derivative_error = np.abs(state[:, 1:] - prev_state[1])
                info['raw_derivative_error'] = raw_derivative_error
                cost -= w[1] * raw_derivative_error**2
            return cost.astype(np.float64)[0]
        elif self._reward_type == 'sparse':
            return distance.astype(np.float64)*self._sparse_scalar

    def compute_terminated(self, state, des_state, info):
        if self._continuing_task:
            return False
        return info['success']

        # if self._continuing_task:
        #     if np.linalg.norm(state - des_state) < 0.1 and not self._steady_state:
        #         self.set_goal()
        #     return False
        # else:
        #     return bool(np.linalg.norm(state - des_state) < 0.1)
        
    def compute_truncated(self, state, des_state, info):
        return False
        
    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        if self._state is not None:
            if self._state.shape == value.shape:
                self._state = value
            else:
                raise ValueError(
                    f'Input shape: {value.shape} != Expected shape: {self._state.shape}'
                )
        else:
            raise ValueError(
                f'Reset the environment before trying to set the state')

    def _render_init(self):
        self._rend = 1
        self._fig, self._axarr = plt.subplots(2, sharex=True)
        self._axarr[0].set_title("I_a")
        self._axarr[1].set_title("Omega")

    def _plot_render_vars(self):
        self._axarr[0].plot(self._render_vars[:,2],self._render_vars[:,0],\
                            c="g")
        self._axarr[1].plot(self._render_vars[:,2],self._render_vars[:,1],\
                            c="b")

    def _kinematic_equation(self, t, y, Va):
        #y[0] will be Ia
        #y[1] will be omega
        return np.array([(Va - self._Kb*y[1]-self._Ra*y[0])/self._La,\
                        (self._Kt*y[0]-self._B*y[1]-self._Tl)/self._J])

    def _action_space(self, max_Va):
        #Va is the only input... Torque losses are from the environment but\
        #not sure how to model this yet
        self.action_space = spaces.Box(low=-max_Va, high=max_Va, shape=(1, ), dtype=np.float64)

    def _observation_space(self):
        #Two observations [Ia,Omega]
        obs_high = np.array([self._Ia_max, self._omega_max])
        self.observation_space = spaces.Dict(
            dict(
                observation=spaces.Box(low=-obs_high, high=obs_high, dtype=np.float64),
                desired_goal=spaces.Box(low=-obs_high[1], high=obs_high[1], dtype=np.float64),
                achieved_goal=spaces.Box(low=-obs_high[1], high=obs_high[1], dtype=np.float64)
            )
        )

    def _calc_observation_limits(self, max_Va, max_Tl):
        self._omega_max = (self._Kt*max_Va-self._Ra*max_Tl)/(self._Ra*self._B+\
                                                             self._Kt*self._Kb)
        self._Ia_max = (self._B * self._omega_max + max_Tl) / self._Kt

def check_create_directory(directory):
    """
    Checks a given directory and creates it if it isn't real. If thisDir is false
    directory must be the full directory otherwise it can just be a filename
    Keyword argments:
    thisDir -- If not false must be __file__ of the input file (default false)
    """
    if not os.path.exists(directory):
        os.makedirs(directory)