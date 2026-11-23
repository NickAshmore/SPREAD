import numpy as np
from physics.mass_flow import update_mp
from physics.drag import update_drag
from physics.body import update_body
from simulation.state import Drone

# this function runs the physics models of the sim and packs the state
# derivate into a single array for integration


def sim_physics(drone: Drone, x: np.ndarray):
    # set state equal to state passed in
    drone.x = x
    
    # initialize dx array
    dx = np.zeros(len(drone.x), dtype=float)
    
    # assign velocity to position state vectors
    dx[:2] = drone.x[2:4]
    
    # call physics models
    dx[4]       = update_mp(drone)
    drone.f_net = update_drag(drone) + drone.fsw.u[:2]
    dx[2:4]     = update_body(drone)
    
    return dx