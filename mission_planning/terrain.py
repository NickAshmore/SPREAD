
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable


# ============================================================
# 1. SYNTHETIC TERRAIN MODEL
# ============================================================

def terrain_height(x, y):
    """
    Calculate terrain elevation at any (x, y) position.
    Uses a Gaussian hill for initial testing.
    All distances are in meters.
    """

    center_x = 50
    center_y = 30
    peak_height = 20
    hill_width = 25

    distance_squared = (
        (x - center_x)**2 +
        (y - center_y)**2
    )

    height = peak_height * np.exp(
        -distance_squared / (2 * hill_width**2)
    )

    return height


# ============================================================
# 2. GENERATE TERRAIN-FOLLOWING TRAJECTORY
# ============================================================

def generate_3d_trajectory(trajectory_2d, clearance, spacing=2.0):
    """
    Convert 2D waypoints into a detailed 3D trajectory.

    trajectory_2d: NumPy array of [x, y] waypoints
    clearance: Desired vertical clearance above terrain (m)
    spacing: Maximum horizontal spacing between samples (m)
    """

    trajectory_2d = np.asarray(trajectory_2d, dtype=float)

    if trajectory_2d.ndim != 2 or trajectory_2d.shape[1] != 2:
        raise ValueError("trajectory_2d must have shape (N, 2)")

    if len(trajectory_2d) < 2:
        raise ValueError("At least two waypoints are required")

    if spacing <= 0 or clearance <= 0:
        raise ValueError("Spacing and clearance must be positive")

    detailed_path = []

    for i in range(len(trajectory_2d) - 1):

        start = trajectory_2d[i]
        end = trajectory_2d[i + 1]

        distance = np.linalg.norm(end - start)

        num_steps = max(1, int(np.ceil(distance / spacing)))

        for j in range(num_steps):
            fraction = j / num_steps

            point = start + fraction * (end - start)

            detailed_path.append(point)

    detailed_path.append(trajectory_2d[-1])

    detailed_path = np.array(detailed_path)

    x = detailed_path[:, 0]
    y = detailed_path[:, 1]

    ground_z = terrain_height(x, y)
    drone_z = ground_z + clearance

    trajectory_3d = np.column_stack((x, y, drone_z))

    return trajectory_3d


# ============================================================
# 3. TERRAIN-AWARE SPEED PLANNER
# ============================================================

def plan_terrain_speed(
    trajectory_3d,
    desired_speed=5.0,
    max_climb_rate=1.0
):
    """
    Reduce horizontal speed on uphill segments when required
    to satisfy an assumed climb-rate limit.

    Returns:
        segment_speeds: Speed for each trajectory segment (m/s)
        mission_time: Estimated total travel time (seconds)
    """

    trajectory_3d = np.asarray(trajectory_3d, dtype=float)

    if trajectory_3d.ndim != 2 or trajectory_3d.shape[1] != 3:
        raise ValueError("trajectory_3d must have shape (N, 3)")

    if len(trajectory_3d) < 2:
        raise ValueError("At least two waypoints are required")

    if desired_speed <= 0 or max_climb_rate <= 0:
        raise ValueError("Speed and climb-rate limit must be positive")

    # Horizontal distance between consecutive waypoints
    horizontal_segments = np.diff(trajectory_3d[:, :2], axis=0)
    horizontal_distances = np.linalg.norm(horizontal_segments, axis=1)

    # Change in altitude between consecutive waypoints
    vertical_changes = np.diff(trajectory_3d[:, 2])

    # Calculate slope for each segment
    slopes = np.zeros_like(horizontal_distances)
    moving = horizontal_distances > 1e-9

    slopes[moving] = (
        vertical_changes[moving] / horizontal_distances[moving]
    )

    # Start with the desired speed on every segment
    segment_speeds = np.full(len(slopes), desired_speed)

    # Apply speed restrictions to uphill segments
    uphill = slopes > 0

    segment_speeds[uphill] = np.minimum(
        desired_speed,
        max_climb_rate / slopes[uphill]
    )

    # Calculate time for each segment
    segment_times = np.zeros_like(horizontal_distances)

    segment_times[moving] = (
        horizontal_distances[moving] / segment_speeds[moving]
    )

    mission_time = np.sum(segment_times)

    return segment_speeds, mission_time


# ============================================================
# 4. DEMONSTRATION AND TESTING
# ============================================================

if __name__ == "__main__":

    # Example 2D coverage trajectory
    trajectory_2d = np.array([
        [0, 5],
        [100, 5],
        [100, 15],
        [0, 15],
        [0, 25],
        [100, 25]
    ])

    # Assumed operating conditions
    clearance = 10.0       # meters
    desired_speed = 5.0     # m/s
    max_climb_rate = 1.0    # m/s

    # Generate detailed terrain-following trajectory
    trajectory_3d = generate_3d_trajectory(
        trajectory_2d,
        clearance=clearance,
        spacing=2.0
    )

    # Calculate 2D flight distance
    segments_2d = np.diff(trajectory_2d, axis=0)
    distance_2d = np.sum(np.linalg.norm(segments_2d, axis=1))

    # Calculate 3D flight distance
    segments_3d = np.diff(trajectory_3d, axis=0)
    distance_3d = np.sum(np.linalg.norm(segments_3d, axis=1))

    extra_distance = distance_3d - distance_2d

    # Analyze required climb rates
    horizontal_segments = np.diff(trajectory_3d[:, :2], axis=0)
    horizontal_distances = np.linalg.norm(horizontal_segments, axis=1)
    vertical_changes = np.diff(trajectory_3d[:, 2])

    slopes = np.zeros_like(horizontal_distances)
    moving = horizontal_distances > 1e-9

    slopes[moving] = (
        vertical_changes[moving] / horizontal_distances[moving]
    )

    required_climb_rates = desired_speed * slopes
    max_required_climb = np.max(required_climb_rates)

    # Calculate terrain-aware speed profile
    segment_speeds, terrain_aware_time = plan_terrain_speed(
        trajectory_3d,
        desired_speed=desired_speed,
        max_climb_rate=max_climb_rate
    )

    # Constant-speed reference
    constant_speed_time = distance_2d / desired_speed

    # --------------------------------------------------------
    # PRINT MISSION RESULTS
    # --------------------------------------------------------

    print("\n========== JTA TERRAIN ANALYSIS ==========")

    print(f"2D Flight Distance: {distance_2d:.2f} m")
    print(f"3D Flight Distance: {distance_3d:.2f} m")
    print(f"Additional Distance: {extra_distance:.2f} m")

    print("\nClimb Rate Analysis:")
    print(f"Maximum required climb rate: {max_required_climb:.2f} m/s")

    if max_required_climb > max_climb_rate:
        print("Constant-speed route exceeds the assumed climb limit.")
    else:
        print("Constant-speed route satisfies the assumed climb limit.")

    print("\nTerrain-Aware Speed Planning:")
    print(f"Minimum planned speed: {np.min(segment_speeds):.2f} m/s")
    print(f"Constant-speed mission time: {constant_speed_time:.2f} s")
    print(f"Terrain-aware mission time: {terrain_aware_time:.2f} s")

    # ========================================================
    # 5. 3D VISUALIZATION
    # ========================================================

    # Create terrain grid
    x = np.linspace(0, 100, 100)
    y = np.linspace(0, 60, 100)

    X, Y = np.meshgrid(x, y)
    Z = terrain_height(X, Y)

    # Create 3D figure
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection="3d")

    # Plot synthetic terrain
    ax.plot_surface(
        X, Y, Z,
        cmap="terrain",
        alpha=0.8
    )

    # Color mapping for planned horizontal speed
    cmap = plt.get_cmap("coolwarm_r")
    norm = Normalize(vmin=0, vmax=desired_speed)

    # Draw every trajectory segment using its planned speed
    for i in range(len(trajectory_3d) - 1):

        x_segment = trajectory_3d[i:i+2, 0]
        y_segment = trajectory_3d[i:i+2, 1]
        z_segment = trajectory_3d[i:i+2, 2]

        speed = segment_speeds[i]
        color = cmap(norm(speed))

        ax.plot(
            x_segment,
            y_segment,
            z_segment,
            color=color,
            linewidth=3
        )

    # Add speed color bar
    color_map = ScalarMappable(norm=norm, cmap=cmap)
    color_map.set_array([])

    fig.colorbar(
        color_map,
        ax=ax,
        shrink=0.6,
        pad=0.12,
        label="Planned Horizontal Speed (m/s)"
    )

    # Plot labels
    ax.set_xlabel("X Position (m)")
    ax.set_ylabel("Y Position (m)")
    ax.set_zlabel("Elevation (m)")
    ax.set_title("JTA Terrain-Aware Drone Flight Path")

    plt.show()
