# -*- coding: utf-8 -*-
"""
@author: nzupp
"""
import os
import pkg_resources
from .. import SFSGym

default_script = pkg_resources.resource_filename('slim_gym', 'scripts/bottleneck.slim')

def make_sfs_env(slim_file=default_script,
    mutation_rate=1e-7,
    num_sites=999,
    sampled_individuals=25):
    """
    Initalizes the env.
    
    Params:
        slim_file (String): Name of the SLiM script
        mutation_rate (Float): Starting mutation rate of the SLiM simulation
        num_sites (Int): Number of sites to simulate (reccomend under 1k for testing)
        sampled_individuals (Int): number of individuals sampled each step
         
    Returns:
        Nothing       
    """
    
    env = SFSGym(
        slim_file=slim_file,
        mutation_rate=mutation_rate,
        num_sites=num_sites,
        sampled_individuals=sampled_individuals,
    )
    
    return env
