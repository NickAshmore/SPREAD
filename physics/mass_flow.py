from simulation.state import Drone

# Update function that intakes deposition command and drone parameters and outputs payload deposition rate for integration

def update_mp(drone: Drone):
    # set mass loss rate to negative deposition rate if deposition command is true
    if drone.fsw.u[2] == 1:
        dm = -drone.config.dep_rate
    else:
        dm = 0
        
    return dm