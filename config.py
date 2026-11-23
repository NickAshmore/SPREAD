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

