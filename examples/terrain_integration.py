
import numpy as np
from planning.terrain import generate_3d_trajectory

# Example of a trajectory received from SPREAD
trajectory = np.array([
    [0, 5],
    [100, 5],
    [100, 15],
    [0, 15]
])

# Convert to terrain-following waypoints
terrain_trajectory = generate_3d_trajectory(
    trajectory,
    clearance=10
)

print("Original waypoints:", len(trajectory))
print("Terrain-aware waypoints:", len(terrain_trajectory))

print("\nFirst five 3D waypoints:")
print(np.round(terrain_trajectory[:5], 2))
