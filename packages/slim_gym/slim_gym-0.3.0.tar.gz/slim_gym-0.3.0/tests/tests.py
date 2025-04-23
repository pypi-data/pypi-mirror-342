# -*- coding: utf-8 -*-
"""
@author: nzupp

Unit tests
"""

from slim_gym.utils.utils import check_slim_installed
from slim_gym import make_sfs_env

def test_check_slim_installed():
    print("Running: test_check_slim_installed")
    assert check_slim_installed() is True, "SLiM is not installed or not found in PATH."
    print("✓ SLiM installation check passed.")
  
def test_env_initialization_and_step():
    print("Running: test_env_initialization_and_step")
    env = make_sfs_env()
    obs, _ = env.reset()
    assert obs is not None, "Environment failed to return an observation on reset."

    action = env.action_space.sample()
    obs, reward, done, truncated, info = env.step(action)
    assert obs is not None, "Environment failed to return an observation on step."
    print("✓ Environment step test passed.")

if __name__ == "__main__":
    test_check_slim_installed()
    test_env_initialization_and_step()
    print("All tests passed.")
