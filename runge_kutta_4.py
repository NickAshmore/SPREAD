from sim_physics import sim_physics
from configure import SimConfig, Drone

# This function performs 4th order Runge-Kutta integrations on the 
# state derivative in accordance with simulaton configuration parameters

def runge_kutta_4(sim_config: SimConfig, drone: Drone):
    # access dt for easier calling
    dt = sim_config.dt
    
    # run sim_physics to find state derivative
    k1 = sim_physics(drone, drone.x)
    k2 = sim_physics(drone, drone.x + 0.5 * dt * k1)
    k3 = sim_physics(drone, drone.x + 0.5 * dt * k2)
    k4 = sim_physics(drone, drone.x + dt * k3)
    
    x = drone.x + 1/6 * (k1 + 2*k2 + 2*k3 + k4)
    return x