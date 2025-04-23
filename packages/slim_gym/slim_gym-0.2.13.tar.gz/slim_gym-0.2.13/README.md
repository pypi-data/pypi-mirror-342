# SLiM-Gym
SLiM-Gym is an early-stage Gymnasium wrapper for the SLiM 4 simulator, designed to enable reinforcement learning as a tool for population genetics.

## General overview
Reinforcement learning (RL) is a machine learning approach where agents learn optimal actions through interaction with an environment, while Gymnasium (formerly OpenAI Gym) provides standardized environments for developing and comparing RL algorithms. SLiM is a powerful forward-time simulation software that models evolutionary processes by tracking individuals and their genomes across generations. 

SLiM-Gym framework provides seamless communication between SLiM 4's evolutionary models and Gymnasium's intuitive action, observation, and reward systems, allowing computational researchers to assess the types of reinforcement learning approaches best suited to evolutionary genomics, population geneticists to explore the relationships between parameters over genetic time, and a unified way to structure these problems for comparable results.

## Requirements
- Python 3.8+
- SLiM 4.0 or newer
- For visualization features: matplotlib, seaborn (optional)
- Stable-Baselines3 for reinforcement learning example

## Quick start guide
1. Install via pip: `pip install slim_gym`
2. Install SLiM 4 from the [Messer Lab Github](https://github.com/MesserLab/SLiM/releases?q=4.3&expanded=true) and ensure it's in your system PATH or working directory
3. Run the example to train a PPO agent on a bottleneck simulation example:

```python
import slim_gym
slim_gym.PPO_example()
```

## Components
### SLiM evolutionary model
SLiM-Gym utilizes Eidos scripts created for running evolutionary simulations with SLiM. The SLiM 4 documentation goes into extensive detail regarding the specifics of these tools, but in short SLiM is highly powerful and flexible, able to model most evolutionary scenarios. The SLiM-Gym package includes two established SLiM scripts- one tracking a single population experiencing a bottleneck, and another that tracks population growth.

Both of these models contain SLiM-Gym 'hooks', or additions to the underlying model, that enable SLiM to communicate with the rest of the SLiM-Gym framework. For a SLiM script to be compatible with SLiM-Gym, it needs to implement several specific hooks:

1. **Flag File Definition**:
```python
defineConstant("FLAG_FILE", "flag.txt");
```
This defines a flag file that serves as a communication channel between SLiM and the Python environment.

2. **State Output**:
```python
g = p1.sampleIndividuals(100).genomes;
g.outputMS("state.txt", append=T);
```
This hook outputs the current state of the simulation in MS format, which the environment uses to construct observations.

3. **Action Reading**:
```python
while (fileExists(FLAG_FILE) == F) {}
mutRateStr = readFile(FLAG_FILE);
while (size(mutRateStr) == 0) {
    mutRateStr = readFile(FLAG_FILE);
}
mutRate = asFloat(mutRateStr);
sim.chromosome.setMutationRate(mutRate);
```
This hook waits for the flag file to exist, reads the action value from it (in this case, a new mutation rate), and applies the action to the simulation.

4. **Simulation Completion Signal**:
```python
writeFile("generation_complete.txt", "1");
```
This hook signals that the simulation has completed, allowing the Python environment to clean up resources.

5. **File Cleanup**:
```python
deleteFile(FLAG_FILE);
```
This hook deletes the flag file after reading the action, preparing for the next communication cycle.

You can verify if your script contains the necessary hooks using the `validate_slim_script()` utility function.

### Base environment
The base environment extends the Gymnasium framework, handling observations from the environment and passing actions to the environment, along with other helping Gymnasium functions. Importantly, the base environment does not attempt to modify the observation from the environment or calculate a reward or action; rather these will be extended by the custom environment designed to handle the task at hand.

### Task environment
This component assigns the proper observation, action and reward handling for the task at hand. Researchers may need to completely reformulate this file to ask the questions they are interested in. We provide an example task file, explained in further detail under the 'Examples' section.

## Core API
SLiM-Gym provides a few key components and functions for setting up evolutionary simulations with reinforcement learning:

To create an environment for agent training, we need to call the task specific environment, `sfs_env` in this case. The custom task environment takes in the evolutionary model via a SLiM file, as well as the starting mutation rate, number of sites and the number of individuals sampled. These must agree with the starting parameters of the simulation, and do not need to be specified if starting with a SLiM-Gym defined model.
```python
import slim_gym
env = slim_gym. make_sfs_env(
    slim_file='bottleneck',     # Path to custom .slim file or 'bottleneck'/'growth'
    mutation_rate=1e-7,         # Starting mutation rate for the simulation
    num_sites=999,              # Number of sites (recommend under 1k for testing)
    sampled_individuals=100      # Number of individuals sampled each step
)
```

SLiM-Gym also offers validation of both the SLiM simulator download, and SLiM script hook verification to make sure any custom script will satisfy the SLiM-Gym communication protocol.
```python
import slim_gym
is_slim_available = slim_gym.check_slim_installed() # Check if SLiM is properly installed and accessible
is_compatible = slim_gym.validate_slim_script('path/to/custom_script.slim') # Verify if a custom SLiM script contains necessary hooks for SLiM-Gym
```

## Creating Custom Environments

SLiM-Gym allows you to create custom environments tailored to specific evolutionary questions. To create a custom environment, extend the base `SLiMGym` class and implement four key methods:

1. **Process Initial State**: Define how to process the initial state from SLiM
2. **Process State**: Transform SLiM output into meaningful observations
3. **Process Action**: Convert reinforcement learning actions into SLiM parameters
4. **Calculate Reward**: Determine the reward based on actions and resulting states

Here's a simplified example:

```python
class MyCustomEnv(SLiMGym):
    def __init__(self, slim_file, other_params):
        super().__init__(slim_file=slim_file)
        
        # Define action and observation spaces
        self.action_space = spaces.Discrete(3)  # Example: 3 possible actions
        self.observation_space = spaces.Box(...)  # Define observation shape
        
    def process_state(self, state_data):
        # Transform SLiM output into observation
        # Example: Parse MS format, extract metrics, etc.
        return observation
        
    def process_action(self, action):
        # Convert action to SLiM parameter
        # Example: Map discrete action to mutation rate
        return parameter_string
        
    def calculate_reward(self, state, action, next_state):
        # Calculate reward based on state transition
        # Example: Reward based on diversity or other metrics
        return reward_value
        
    def get_initial_state(self):
        # Define starting observation
        return initial_observation
```
See the SFSGym implementation in the package for a complete example that uses the Site Frequency Spectrum as the observation space.

## Worked example
The SLiM-Gym package comes equipped with two custom evolutionary simulations, representing a bottleneck and a growth scenario, and one test environment labeled SFSGym. SFS is a population genetics term standing for the Site Frequency Spectra, which represents the counts of alleles in a measured population. The SFS is critical for estimating demography, genetic diversity, population size, and other important summary statistics.

In the example provided, the task is to maintain the original SFS pattern despite demographic changes occurring in the simulation. While the SFS can be used to estimate theta, the reward function directly measures how similar the current SFS is to baseline SFS patterns collected during a burn-in period. Specifically, it calculates the negative Kullback-Leibler divergence between these distributions - the more similar they are, the higher the reward. The agent has three discrete actions: decrease mutation rate by 10%, maintain the current rate, or increase it by 10%. The reinforcement training uses Stable Baseline3's Proximal Policy Optimization (PPO) algorithm to learn the optimal policy.

In order train on this task, first we would want to import the necessary dependencies and load our simulation file.

```python
import slim_gym
from stable_baselines3 import PPO

slim_script = 'scripts/bottleneck.slim' # for your own script, or 'bottleneck' or 'growth' for predefined models
```

We will then want to create an environment for our agent.

```python
env = make_sfs_env(slim_file=slim_script)
```

Then instantiate a PPO model from Stable Baselines. These are default parameters to run a multilayer perceptron policy on our environment. The verbose output set to 1 will log training details to the console. See the Stable Baselines documentation for more information or customization strategies regarding the reinforcement learning approach to the problem.

```python
model = PPO("MlpPolicy", env, verbose=1)
```

Finally, we can train and save our results.

```python
model.learn(total_timesteps=5000)
model.save("ppo_sfs_env")
```

This completes the training run. Note: this code can be directly run using the 'slim_gym.PPO_example()' code as well.

## Troubleshooting
If you encounter any issues with installation or simulation errors, please report them on our GitHub issue tracker [link]. Common issues include SLiM not being found in PATH (ensure SLiM is properly installed and accessible from your command line) and simulation failures due to biologically implausible parameter settings.
