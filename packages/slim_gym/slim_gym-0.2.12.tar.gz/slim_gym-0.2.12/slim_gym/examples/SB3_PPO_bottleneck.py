# -*- coding: utf-8 -*-
"""
@author: nzupp

Sample PPO example using SB3 for population genetics

Task: Identify the change in mutation rate needed to maintain previous
AFS in a bottleneck
"""

import pkg_resources
from .. import make_sfs_env
from stable_baselines3 import PPO

def PPO_example():
    # Create the environment
    bottleneck_script = pkg_resources.resource_filename('slim_gym', 'scripts/bottleneck.slim')

    # Make env
    env = make_sfs_env(slim_file=bottleneck_script)
    
    # Create PPO model
    model = PPO("MlpPolicy", env, verbose=1)

    # Train the model
    model.learn(total_timesteps=5000)

    # Save the model
    model.save("ppo_sfs_env")

    print("Training complete. Model saved as ppo_sfs_env.zip")
