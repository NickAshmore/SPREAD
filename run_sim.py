import numpy as np
import math
from fsw.trans_pid import trans_pid
from runge_kutta_4 import runge_kutta_4
from configure import SimConfig, DroneConfig, Drone

# This function is the core simulation function of SPREAD. It takes in the sim and drone configurations,
# initial conditions, and the trajectory and outputs a time history of the drones flight using a flight controller
# and integration via 4th order Runge-Kutta method.

def run_sim(trajectory: np.ndarray):
    # initialize simulation, drone, and state derivative at first trajectory waypoint using default DroneConfig
    sim_config   = SimConfig()
    x0           = trajectory[0]
    drone_config = DroneConfig()
    drone        = Drone(drone_config, x0)

    # initialize lists for time series storage
    t    = [0]
    pos  = [[drone.x[0], drone.x[1]]]
    vel  = [[drone.x[2], drone.x[3]]]
    m    = [drone.x[4]]

    # calculate initial straight line distance from ending waypoint
    i          = -1
    final_targ = trajectory[i]
    e_mag      = math.dist(drone.x[:2], final_targ)
    i          += 1
    curr_targ  = trajectory[i]

    # loop through simulation until e_mag is within tolerance
    while e_mag > drone.config.fsw.wp_rad:
        # check to see if current waypoint reached
        dist = math.dist(drone.x[:2], curr_targ)
        if dist <= drone.config.fsw.wp_rad:
            # update current target
            i += 1
            curr_targ = trajectory[i]
        
        # run PID controller to find thrust
        drone.fsw.u[:2], drone.fsw.integral_err = trans_pid(sim_config, drone, curr_targ)
        
        # run RK4 integration
        drone.x = runge_kutta_4(sim_config, drone)
        
        # update distance from final waypoint
        e_mag = math.dist(drone.x[:2], final_targ)
        
        # append results to storage lists
        t.append(t[-1] + sim_config.dt)
        pos.append([drone.x[0], drone.x[1]])
        vel.append([drone.x[2], drone.x[3]])
        m.append(drone.x[4])

    # convert history lists into numpy arrays
    timestamps = np.array(t)
    positions  = np.array(pos)
    velocities = np.array(vel)
    mass       = np.array(m)
    
    return timestamps, positions, velocities, mass