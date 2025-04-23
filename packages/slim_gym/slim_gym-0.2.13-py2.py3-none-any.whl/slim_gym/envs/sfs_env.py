# -*- coding: utf-8 -*-
"""
@author: nzupp

Reference env for SLiM-Gym reinforcement learning framework

Extends four key functions
1) Process initial state
2) Process state
3) Process action
4) Calculate reward

In this env, we define our observations, our actions, and how we evaluate those
actions. An overview of the env can be found in the associated paper.
"""

import numpy as np
from gymnasium import spaces
from collections import deque
from .. import SLiMGym

class SFSGym(SLiMGym):
    def __init__(self, 
                slim_file,
                mutation_rate,
                sampled_individuals,
                num_sites):
        """
        Initalizes the env.
        
        Params:
            slim_file (String): Name of the SLiM script
            
        Returns:
            Nothing       
        """
        
        # Initialize base class with generated script
        super().__init__(slim_file=slim_file)
        
        self.current_mutation_rate = mutation_rate
        self.sampled_individuals = sampled_individuals
        self.num_sites = num_sites
        self.num_bins = 100
        self.sfs_stack_size = 8
        self.expectation_sfs = None
        
        # Action space that allows for some parameter of the simulation to be
        # controlled. The current env allows for discrete control of mutation rate,
        # either by increasing it, decreasing it or staying the same.
        self.action_space = spaces.Discrete(3)
        self.action_map = {
            0: 0.9,
            1: 1.0,
            2: 1.1
        }

        # We define the observation space as the SFS of the simulation at each
        # generation. The number of bins in the SFS is equal to the number of 
        # diploid individuals times two.
        self.observation_space = spaces.Box(
            low=0,
            high=self.num_sites,
            shape=(self.sfs_stack_size, self.num_bins),
            dtype=np.float64
        )
        
        # We also implement 'SFS stacking', similar to frame stacking, to extend
        # conext in training
        self.sfs_stack = deque(maxlen=self.sfs_stack_size)
        self.initialize_sfs_stack()

    def initialize_sfs_stack(self):
        """
        Code to initalize the starting SFS stack
        
        Params:
            None

        Returns:
            Nothing
        """
        self.sfs_stack.clear()
        for _ in range(self.sfs_stack_size):
            # Near zero probability in initalized SFS. This is consistent with SLiM;
            # view their documentations for details on how they init pops
            noise = np.full(self.num_bins, 1e-10)
            self.sfs_stack.append(noise)

    # The data passed from SLiM is not immediately in SFS format- it is in MS format
    # (Note: This format can be changed in either the .slim script)
    def get_sfs(self, state_data):
        """
        Code to extract the sfs from ms output

        Params
            state_data (SLiM MS format): The output SLiM in MS format

        Returns
            sfs (np.ndarray)
        """
        lines = state_data.strip().split('\n')
        binary_lines = [line.strip() for line in lines 
                        if set(line.strip()).issubset({'0', '1'})]
        
        # If no valid binary data, return an SFS filled with small values
        if not binary_lines:
            return np.full(self.num_bins, 1e-10, dtype=np.float32)
        
        lengths = [len(line) for line in binary_lines]
        max_len = max(lengths)
        binary_lines = [line.ljust(max_len, '0')[:max_len] for line in binary_lines]
        
        # Build the data matrix: rows are sequences/haplotypes, columns are sites
        data = np.array([[int(char) for char in line] for line in binary_lines])
        total = data.shape[0]  # number of haplotypes (or alleles, since each row is one haplotype)
        column_sums = np.sum(data, axis=0)
        
        # Calculate frequency (in percent) for each site
        # For each column, frequency = (number of 1's / total) * 100
        freqs = (column_sums / total) * 100.0
        
        # Determine the bucket: floor the frequency value
        # Bucket 0 corresponds to frequencies in [0, 1)%, bucket 1 to [1, 2)%, etc.
        buckets = np.floor(freqs).astype(int)
        
        # Ignore fixed sites (i.e. those with frequency 100%)
        valid_buckets = buckets[buckets < 100]
        
        # Initialize SFS with small positive values
        sfs = np.full(self.num_bins, 1e-10, dtype=np.float32)
        
        if valid_buckets.size > 0:
            unique_bins, counts = np.unique(valid_buckets, return_counts=True)
            for b, count in zip(unique_bins, counts):
                sfs[b] = count + 1e-10
                
        return sfs
    
    def get_expectation_sfs(self, state_data):
        """
        Use log data from our burn in to set an expectation SFS before any actions

        Params
            state_data (SLiM MS format): The output of the SLiM in MS format

        Returns
            Nothing
        """
        ms_entries = state_data.strip().split('\n\n')
        all_sfs = []
        
        for entry in ms_entries:
            sfs = self.get_sfs(entry)
            all_sfs.append(sfs)
        
        if all_sfs:
            self.expectation_sfs = all_sfs

    def process_state(self, state_data):
        """
        Implement the abstract SLiM-Gym function. If its the first step we get the
        expectation SFS, otherwise we just call to get_sfs and dequeue the SFS stack

        Params
            state_data (SLiM MS format): The output of SLiM in MS format

        Returns
            sfs_stack (np.ndarray)

        """
        if self.step_count == 1:
            self.get_expectation_sfs(state_data)
            
        new_sfs = self.get_sfs(state_data)
        self.sfs_stack.append(new_sfs)
        return np.stack(list(self.sfs_stack))

    def process_action(self, action):
        """
        Implement the abstract SLiM-Gym function by assigning an adjusted mutation rate.

        Params
            action (Int): Discrete action of 0, 1 or 2

        Returns
            new_rate (Float): The modified rate
        """
        multiplier = self.action_map[action]
        new_rate = np.clip(
    	    self.current_mutation_rate * multiplier,
    	    1e-9,
    	    1e-5
	)
        self.current_mutation_rate = new_rate
        return str(new_rate)

    # TODO I imagine this could be the center of a decent experiment
    def calculate_reward(self, state, action, next_state):
        """
        Implements the abstract SLiM-Gym function 'calculate_reward'. We test how divergent our current SFS is
        from each SFS in our expectation, to get an overall divergence. The negative divergence
        is then applied as the reward, with learning algorithms working to maximize reward i.e.
        minimize divergence

        Params
            state (np.ndarray): A stack of SFS of SFS_stack_size size
            action (Float): Float multiplier to apply to our mutation rate
            next_state (np.ndarray): The resulting state after applying the action

        Returns
            reward (Float): Negative mean KL divergence between current SFS and expectation SFS.
        """
        try:
            current_sfs = next_state[-1] + 1e-10
            
            klds = []
            for exp_sfs in self.expectation_sfs:
                exp_sfs = np.array(exp_sfs) + 1e-10
                
                current_normalized = current_sfs / np.sum(current_sfs)
                expectation_normalized = exp_sfs / np.sum(exp_sfs)
                
                kld = np.sum(expectation_normalized * (
                    np.log(expectation_normalized) - np.log(current_normalized)))
                
                if np.isfinite(kld):
                    klds.append(kld)
            
            # Big negative for errors
            if not klds:
                print("Warning: No valid KLD calculations")
                return -100000.0
            
            return float(-np.mean(klds))
            
        except Exception as e:
            print(f"Error in reward calculation: {e}")
            return -10000.0
    
    def get_initial_state(self):
        """
        Implement the abstract SLiM-Gym function by initalizing the sfs stack

        Returns
            (np.ndarray): Initial sfs stack
        """
        self.initialize_sfs_stack()
        return np.stack(list(self.sfs_stack))
