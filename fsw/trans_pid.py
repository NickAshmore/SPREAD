import numpy as np
from spread import SimConfig, DroneConfig

# Translation PID controller that takes in current position, velocity, and trajectory waypoint and outputs thrust command.

def trans_pid(sim_config: SimConfig, drone: DroneConfig, x, wp):
    # Calculate state errors
    err = wp - x
    err_dot = -x; # Assuming static waypoint, derivative of error is -velocity
    err_integral = err_integral + err * sim_config.dt
    
    # Calculate commanded force
    u = drone.Kp * err + drone.Ki * err_integral + drone.Kd * err_dot
    
    # Saturate control output (Actuator limits)
    force_mag = np.linalg.norm(u)
    if force_mag > drone.max_force:
        u = u * (drone.max_force / force_mag)
    
    return u