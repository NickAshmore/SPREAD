import numpy as np
from config import DroneConfig, FSWConfig

# define drone object
class FSW:
    def __init__(self, fsw_config: FSWConfig):
        # store fsw configuration
        self.config = fsw_config
        
        # initialize dynamic fsw variables
        self.integral_err = np.zeros(2, dtype=float)
        self.u            = np.zeros(3, dtype=float)

class Drone:
    def __init__(self, drone_config: DroneConfig, x0: np.ndarray):
        # store drone and fsw configurations
        self.config = drone_config
        self.fsw    = FSW(self.config.fsw)
        
        # initialize dynamic state variables
        initial_mass = self.config.dry_m + self.config.pay_m
        self.x       = np.array([x0[0], x0[1], 0.0, 0.0, initial_mass], dtype=float)