import numpy as np
from dataclasses import dataclass, field

# --- Class and Object Definitions ---

# define simulation configuration
@dataclass
class SimConfig:
    dt: float  = 0.01 # s
    tol: float = 1e-8 # error tolerance for simulation termination
    
# define flight software configuraton
@dataclass
class FSWConfig:
    kp: float     = 0.5  # proportional gain
    kd: float     = 20.0  # derivative gain
    ki: float     = 0.01 # integral gain
    wp_rad: float = 0.5  # waypoint radius to consider reached

# define drone configuration
@dataclass
class DroneConfig:
    dry_m: float     = 56    # kg dry mass
    pay_m: float     = 80    # kg payload mass
    dep_rate: float  = 5     # kg/s deposition rate
    c_d: float       = 0.2   # drag coefficient
    area: float      = 2.0   # m^2 cross section affected by drag
    rho: float       = 1.224 # kg/m^3 air density
    max_force: float = 50   # N max horizontal thrust force
    
    fsw: FSWConfig   = field(default_factory=FSWConfig)

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