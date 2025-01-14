import numpy as np
from abc import ABC, abstractmethod
import os
import cv2
import getpass
from mujoco_py import GlfwContext
from unstable_baselines.common import util
# GlfwContext(offscreen=True) 

class BaseTrainer():
    def __init__(self, agent, train_env, eval_env, args, max_trajectory_length, **kwargs):
        self.agent = agent
        self.train_env = train_env
        self.eval_env = eval_env
        self.max_trajectory_length = max_trajectory_length
        pass

    @abstractmethod
    def train(self):
        #do training 
        pass

    @abstractmethod
    def test(self):
        #do testing
        pass
        
        
    def save_video_demo(self, ite, width=128, height=128, fps=30):
        video_demo_dir = os.path.join(util.logger.log_dir,"demos")
        if not os.path.exists(video_demo_dir):
            os.makedirs(video_demo_dir)
        video_size = (height, width)
        video_save_path = os.path.join(video_demo_dir, "ite_{}.avi".format(ite))

        #initilialize video writer
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        video_writer = cv2.VideoWriter(video_save_path, fourcc, fps, video_size)

        #rollout to generate pictures and write video
        state = self.eval_env.reset()
        img = self.eval_env.render(mode="rgb_array", width=width, height=height)
        for step in range(self.max_trajectory_length):
            action, _ = self.agent.select_action(state)
            next_state, reward, done, _ = self.eval_env.step(action)
            state = next_state
            img = self.eval_env.render(mode="rgb_array", width=width, height=height)
            video_writer.write(img)
            if done:
                break
                
        video_writer.release()