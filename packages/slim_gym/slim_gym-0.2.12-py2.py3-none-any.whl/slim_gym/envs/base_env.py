# -*- coding: utf-8 -*-
"""
@author: nzupp

The SLiM-Gym Wrapper. 

Extends Gymanisum and handles communication and action signaling with the 
SLiM 4 simulation.
"""

import gymnasium as gym
import subprocess
import time
from pathlib import Path
from abc import abstractmethod

# This format should be easily integratable with current reinforcement learning
# frameworks such as Stable Baselines
class SLiMGym(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, slim_file, timeout=10.0):
        super().__init__()
        self.slim_file = slim_file
        self.timeout = timeout
        self.process = None
        self.previous_log_data = ""
        self.current_log_data = ""
        self.step_count = 0
        
    @abstractmethod
    def process_state(self, state_data):
        """Implemented by the env"""
        pass
    
    @abstractmethod
    def process_action(self, action):
        """Implemented by the env"""
        pass
      
    @abstractmethod
    def calculate_reward(self, state, action, next_state):
        """Implemented by the env"""
        pass
     
    @abstractmethod
    def get_initial_state(self):
        """Implemented by the env"""
        pass

    def _cleanup_files(self):
        """
        Removes state, flag and generation complete files

        Returns
            Nothing
        """
        try:
            for filename in ['flag.txt', 'state.txt', 'generation_complete.txt']:
                file_path = Path(filename)
                if file_path.exists():
                    # Wait for the file to be released before deletion.
                    if self.wait_for_file_release(str(file_path), timeout=1.0):
                        file_path.unlink()
                    else:
                        print(f"Warning: {filename} is still in use; cannot unlink at this time.")
        except Exception as e:
            print(f"Error cleaning up files: {e}")

    def wait_for_file_release(self, filepath, timeout=1.0):
        """
        Additional race condition helper file that waits for a file to be released.
        Currently timeout is handtuned but seems servicable- will open up an issue if
        that changes

        Params
            filepath (String): The filepath we are waiting for
            timeout (Float): How long to wait before timing out

        Returns
            (Bool): Release status
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                with open(filepath, 'r+'):
                    return True
            except (IOError, PermissionError):
                time.sleep(0.01)
        return False

    # TODO: This is currently set up to only really read one param effectively-
    # this could be extended in future versions
    def make_flag(self, param_string):
        """
        # Makes the flag file to be passed to SLiM. Previously was experiencing race
        # conditions with the file, so I used an atomic rename to prevent reading
        # from the flag file before the action was written

        Params
            param_string (STRING): New parameters to passed onto SLiM

        Returns
            (Bool): True if successful making flag
        """
        try:
            temp_file = Path('flag.txt.tmp')
            flag_file = Path('flag.txt')
            
            temp_file.write_text(param_string)
            temp_file.rename(flag_file)
            return True
        except Exception as e:
            print(f"Error writing flag file: {e}")
            return False

    
    def step(self, action):
        """
        Extends Gymnasiums step function. This function handles the file communucation
        with the SLiM simulation at each step, receiving the log data and sending the
        action signal back
        
        Step returns a tuple with 5 parts:
        1) State: current state
        2) Reward: reward from previous action
        3) Terminated: epsiode terminated
        4) Truncated: episode cut short
        5) Info: any info passed along as a message

        Params
            action (Float): Numerical action space; could also be discrete

        Returns
            (Tuple): State, Reward, Terminated, Truncated, Info
        """
        self.step_count += 1
        param_string = self.process_action(action)
        
        terminated = False
        truncated = False
        reward = 0
        current_state = None
        
        complete_path = Path('generation_complete.txt')
        state_path = Path('state.txt')
        flag_path = Path('flag.txt')
        
        start_time = time.time()
        while True:
            if complete_path.exists():
                self.close()
                return current_state or self.get_initial_state(), reward, True, False, {"completed": True}
            
            if self.process.poll() is not None:
                if complete_path.exists():
                    self.close()
                    return current_state or self.get_initial_state(), reward, True, False, {"completed": True}
                if current_state is not None:
                    self.close()
                    return current_state, reward, True, False, {"completed": True}
                break
            
            # Time out acts as a last resort against file communication corruption
            # Allows the episode to be escaped without crashing the training run
            if time.time() - start_time > self.timeout:
                print("TIMEOUT - killing episode")
                self.close()
                self.reset()
                return self.get_initial_state(), -1, True, False, {"error": "timeout"}
            
            if complete_path.exists():
                self.close()
                return current_state or self.get_initial_state(), reward, True, False, {"completed": True}
            
            # The main protocol loop. When a state file exists but the flag file does not,
            # that is the signal from SLiM to proceed with the step. We calculate the reward,
            # get the next action, generate the flag file and continue on to the next step. nice!
            if state_path.exists() and not flag_path.exists():
                if self.wait_for_file_release('state.txt'):
                    with open('state.txt', 'r') as f:
                        self.current_log_data = f.read().strip()
                    
                    state_data = self.current_log_data[len(self.previous_log_data):].strip()
                    current_state = self.process_state(state_data)
                    
                    if hasattr(self, 'previous_state'):
                        reward = self.calculate_reward(self.previous_state, action, current_state)
                    
                    self.previous_state = current_state
                    self.previous_log_data = self.current_log_data
                    self.make_flag(param_string)
                    
                    return current_state, reward, terminated, truncated, {}
            
            time.sleep(0.01)
        
        if current_state is not None:
            return current_state, reward, True, False, {"episode_complete": True}
        
        # Error handling code for process errors, although this has largely been resolved
        
        return_code = self.process.returncode
        stdout, stderr = "", ""
        try:
            stdout, stderr = self.process.communicate(timeout=1)
        except:
            pass
        
        print("Process ended unexpectedly before getting state!")
        print(f"Return code: {return_code}")
        print(f"Last step count: {self.step_count}")
        if stdout: print(f"stdout: {stdout}")
        if stderr: print(f"stderr: {stderr}")
        
        print("Attempting to reset environment...")
        initial_state, _ = self.reset()
        return initial_state, -1, True, False, {
            "error": "process_ended",
            "return_code": return_code,
            "step_count": self.step_count,
            "stdout": stdout,
            "stderr": stderr
        }

    def reset(self, seed=None):
        """
        Reset the environment to an initial state.

        Params
            seed (Int): Set the random seed with an integer
            
        Returns
            (Tuple): The initial SFS stack state and empty dictionary for gymnasium compatibility
        """
        super().reset(seed=seed)
        
        # Shut down process
        if self.process is not None:
            self.close()
        
        # Delete files
        self._cleanup_files()
        
        self.previous_log_data = ""
        self.current_log_data = ""
        self.step_count = 0
        
        # Relaunch subprocess
        try:
            self.process = subprocess.Popen(
                ["slim", self.slim_file],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )
        
        except Exception as e:
            print(f"Error starting SLiM process: {e}")
            self.process = None
        
        # Pass initial observations
        initial_state = self.get_initial_state()
        self.previous_state = initial_state
        return initial_state, {}

    def close(self):
        """
        Handles closing any processes still hanging

        Returns
            Nothing
        """
        
        if self.process:
            try:
                self.process.kill()
                self.process.wait(timeout=5)
            except:
                print("Process kill timeout")
        time.sleep(0.05)
        self._cleanup_files()
