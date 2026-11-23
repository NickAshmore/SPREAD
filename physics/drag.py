import numpy as np
from simulation.state import Drone

# Update function that intakes drone parameters and state and outputs drag force on drone

def update_drag(drone: Drone):
    vx   = drone.x[2]
    vy   = drone.x[3]
    cd   = drone.config.c_d
    area = drone.config.area
    rho  = drone.config.rho
    
    # START TODO add wind effects
    # calculate total velocity magnitude (speed)
    speed = np.hypot(vx, vy)
    # END TODO
    
    # prevent math errors if the drone is perfectly stationary
    if speed < 1e-8:
        return np.zeros(2)
        
    # calculate the scalar drag multiplier: -0.5 * rho * Cd * Area * |v|
    drag_multiplier = -0.5 * rho * cd * area * speed
    
    # return the decomposed force vector [F_dx, F_dy]
    f_dx = drag_multiplier * vx
    f_dy = drag_multiplier * vy
    
    return np.array([f_dx, f_dy])