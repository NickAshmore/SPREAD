from configure import Drone

# Update function that intakes sum of forces on the drone rigid body and current mass of drone and outputs acceleration

def update_body(drone: Drone):
    dv = drone.f_net / drone.x[4]
    return dv