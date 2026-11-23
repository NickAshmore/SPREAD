
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable

from planning.coverage import generate_coverage_path, calculate_path_distance
from planning.terrain import terrain_height, generate_3d_trajectory, plan_terrain_speed


# ==================================================
# 1. FIELD AND OPERATING PARAMETERS
# ==================================================

field_width = 100.0
field_height = 60.0
field_margin = 5.0
swath_width = 10.0

clearance = 10.0
desired_speed = 5.0
max_climb_rate = 1.0


# ==================================================
# 2. GENERATE 2D COVERAGE PATH
# ==================================================

flight_lines = np.arange(
    swath_width / 2,
    field_width,
    swath_width
)

trajectory_2d = generate_coverage_path(
    flight_lines,
    field_height,
    field_margin
)


# ==================================================
# 3. CONVERT TO TERRAIN-FOLLOWING PATH
# ==================================================

trajectory_3d = generate_3d_trajectory(
    trajectory_2d,
    clearance=clearance,
    spacing=1.0
)


# ==================================================
# 4. MISSION PERFORMANCE ANALYSIS
# ==================================================

distance_2d = calculate_path_distance(trajectory_2d)
distance_3d = calculate_path_distance(trajectory_3d)

segment_speeds, terrain_time = plan_terrain_speed(
    trajectory_3d,
    desired_speed=desired_speed,
    max_climb_rate=max_climb_rate
)

flat_time = distance_2d / desired_speed

time_increase = 100 * (terrain_time - flat_time) / flat_time

print("\n========== SPREAD TERRAIN DEMO ==========")
print(f"Coverage passes: {len(flight_lines)}")
print(f"Original waypoints: {len(trajectory_2d)}")
print(f"Terrain waypoints: {len(trajectory_3d)}")
print(f"2D distance: {distance_2d:.2f} m")
print(f"3D distance: {distance_3d:.2f} m")
print(f"Flat reference time: {flat_time:.2f} s")
print(f"Terrain-aware time: {terrain_time:.2f} s")
print(f"Time increase: {time_increase:.1f}%")
print(f"Minimum planned speed: {np.min(segment_speeds):.2f} m/s")


# ==================================================
# 5. 3D TERRAIN AND SPEED VISUALIZATION
# ==================================================

x = np.linspace(0, field_width, 100)
y = np.linspace(0, field_height, 100)

X, Y = np.meshgrid(x, y)
Z = terrain_height(X, Y)

fig = plt.figure(figsize=(11, 7))
ax = fig.add_subplot(111, projection="3d")

ax.plot_surface(
    X, Y, Z,
    cmap="terrain",
    alpha=0.65
)

# Color each segment based on operating speed
cmap = plt.get_cmap("coolwarm_r")
norm = Normalize(vmin=0, vmax=desired_speed)

for i in range(len(trajectory_3d) - 1):

    segment = trajectory_3d[i:i+2]
    color = cmap(norm(segment_speeds[i]))

    ax.plot(
        segment[:, 0],
        segment[:, 1],
        segment[:, 2],
        color=color,
        linewidth=2.5
    )

color_map = ScalarMappable(norm=norm, cmap=cmap)
color_map.set_array([])

fig.colorbar(
    color_map,
    ax=ax,
    shrink=0.6,
    pad=0.12,
    label="Planned Horizontal Speed (m/s)"
)

ax.set_xlabel("X Position (m)")
ax.set_ylabel("Y Position (m)")
ax.set_zlabel("Elevation (m)")

ax.set_title("SPREAD - Terrain-Aware Mission Planning")

plt.tight_layout()
plt.show()
