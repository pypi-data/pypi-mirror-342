# -*- coding: utf-8 -*-
"""
@author: nzupp
SLiM-Gym: A gymnasium environment for SLiM evolutionary simulations
"""
__version__ = "0.2.12"

# Import core components
from .envs.base_env import SLiMGym
from .envs.sfs_env import SFSGym
from .envs.make_sfs_env import make_sfs_env
from .utils.utils import check_slim_installed, validate_slim_script
from .examples.SB3_PPO_bottleneck import PPO_example

__all__ = [
    'SLiMGym',
    'SFSGym',
    'make_sfs_env',
    'check_slim_installed',
    'validate_slim_script',
    'PPO_example'
]
