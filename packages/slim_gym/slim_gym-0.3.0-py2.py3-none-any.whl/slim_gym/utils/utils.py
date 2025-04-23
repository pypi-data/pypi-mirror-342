# -*- coding: utf-8 -*-
"""
@author: nzupp

SLiM-Gym Utilities 
"""

import shutil
import os

def check_slim_installed() -> bool:
    """
    Checks if the SLiM executable is available in the system PATH.

    Returns:
        bool: True if SLiM is found, False otherwise.
    """
    slim_path = shutil.which("slim")
    return slim_path is not None


def validate_slim_script(path: str) -> bool:
    """
    Basic check to validate if a SLiM script is SLiM-Gym compatible.

    Checks for key markers:
    - FLAG_FILE definition
    - outputMS usage
    - generation_complete signal
    - readFile + setMutationRate logic

    Params:
        path (str): Path to the .slim file to validate

    Returns:
        bool: True if the script appears SLiM-Gym compatible, False otherwise
    """
    if not os.path.isfile(path):
        return False

    with open(path, "r") as f:
        content = f.read()

    required_keywords = [
        "defineConstant(\"FLAG_FILE\"",  # comm signal
        "outputMS",                      # log format
        "readFile(FLAG_FILE)",           # read action
        "setMutationRate",               # RL control hook
        "generation_complete.txt"        # terminal signal
    ]

    return all(keyword in content for keyword in required_keywords)
