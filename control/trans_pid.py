import numpy as np
from config import SimConfig
from simulation.state import Drone

# Translation PID controller that takes in current position, velocity, and trajectory waypoint and outputs thrust command.

def trans_pid(sim_config: SimConfig, drone: Drone, wp: np.ndarray):
    # Calculate state errors
    err = wp - drone.x[:2]
    err_dot = -drone.x[2:4]; # Assuming static waypoint, derivative of error is -velocity
    integral_err = drone.fsw.integral_err + err * sim_config.dt
    
    # Calculate commanded force
    u = drone.config.fsw.kp * err + drone.config.fsw.ki * integral_err + drone.config.fsw.kd * err_dot
    
    # Saturate control output (Actuator limits)
    force_mag = np.linalg.norm(u)
    if force_mag > drone.config.max_force:
        u = u * (drone.config.max_force / force_mag)
    
    return u, integral_err