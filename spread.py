import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from configure import SimConfig
from dataclasses import field
from run_sim import run_sim

# --- Mission Parameters ---

field_width  = 100.0 # meters
field_height = 100.0 # meters


line_spacing = st.sidebar.slider(
        "Flight Line Spacing (m)", 
        min_value=5.0, 
        max_value=20.0, 
        value=8.0, 
        step=1.0
)

wind_speed = st.sidebar.slider(
    "Wind Speed (m/s)",
    min_value=0.0,
    max_value=15.0,
    value=3.0,
    step=0.5
)

wind_direction = st.sidebar.slider(
    "Wind Direction (°)",
    min_value=0,
    max_value=359,
    value=90,
    step=5
)


# --- Flight Path Generation ---

# START TODO Add waypoints on straightaways for flight controller
# field_margin = (line_spacing / 2) * 1.5 # Add space between drone and field boundary
field_margin = (line_spacing / 2) + 5.0


flight_lines = np.arange(
        line_spacing / 2, # Starting x coord
        field_width, # Final x coord
        line_spacing # Spacing between each line
)

path = []

for i, x in enumerate(flight_lines):
    if i % 2 == 0:
        # Even: flying upward
        path.append([x, field_margin])
        path.append([x, field_height - field_margin])
    else:
        # Odd: flying downward
        path.append([x, field_height - field_margin])
        path.append([x, field_margin])
    if i < len(flight_lines) - 1:
        next_x = flight_lines[i + 1]
        radius = (next_x - x) / 2
        center_x = (x + next_x) / 2

        if i % 2 == 0:
            center_y = field_height - field_margin
            theta = np.linspace(np.pi, 0, 30)
        else:
            center_y = field_margin
            theta = np.linspace(np.pi, 2 * np.pi, 30)

        for angle in theta:
            turn_x = center_x + radius * np.cos(angle)
            turn_y = center_y + radius * np.sin(angle)
            path.append([turn_x, turn_y])

trajectory = np.array(path)
# END TODO

# --- Run Simulation ---

timestamps, positions, velocities, mass = run_sim(trajectory)

# Calculate distance between consecutive waypoints
segments = np.diff(trajectory, axis=0)
segment_lengths = np.linalg.norm(segments, axis=1)

# Calculate cumulative distance
cumulative_distance = np.concatenate((
    [0],
    np.cumsum(segment_lengths)
))

mission_duration = timestamps[-1]

current_time = st.slider(
    "Mission Progress (seconds)",
    min_value=0.0,
    max_value=float(mission_duration),
    value=0.0,
    step=0.1
)
drone_x = np.interp(
    current_time,
    timestamps,
    positions[:, 0]
)

drone_y = np.interp(
    current_time,
    timestamps,
    positions[:, 1]
)

# START TODO
# --- Deposition Playback ---

dt = SimConfig.dt  # Seconds between simulation samples

sample_times = np.arange(0, mission_duration + dt, dt)
sample_times = np.clip(sample_times, 0, mission_duration)

sample_x = np.interp(sample_times, timestamps, positions[:, 0])
sample_y = np.interp(sample_times, timestamps, positions[:, 1])

# Identify which samples belong to straight application passes.
# During turns, the drone should not dispense.
dispensing = np.zeros(len(sample_times), dtype=bool)

for x_line in flight_lines:
    dispensing |= (
        (np.abs(sample_x - x_line) < 0.01)
        & (sample_y >= field_margin)
        & (sample_y <= field_height - field_margin)
    )
# END TODO

# --- Wind Vector ---

wind_angle = np.radians(wind_direction)
wind_x = wind_speed * np.cos(wind_angle)
wind_y = wind_speed * np.sin(wind_angle)

# --- Mission Metrics ---
# START TODO: Replace placeholder metrics with sim outputs

metrics = {
    "duration": 7.2,           # minutes
    "energy_used": 185.0,      # Wh
    "coverage": 92.4,          # %
    "uniformity_cv": 18.6,     # %
    "payload_remaining": 12.5  # kg
}


# END TODO

# -- Visualization ---

st.title("SPREAD")
st.subheader("Simulation for Predicting Run Efficiency of Agricultural Drones")


# Heat map is an NxN array representing the field
# Each element is a location on the field, and its value is the amount of deposited material

N = 200
field = np.zeros((N, N))

# START TODO Remove dummy data and replace with simulated deposition

drift_factor = 1.5  # Illustrative meters of drift per m/s

drift_x = wind_x * drift_factor
drift_y = wind_y * drift_factor 


# --- Gaussian Deposition Model ---
x = np.linspace(0, field_width, N)
y = np.linspace(0, field_height, N)
X, Y = np.meshgrid(x, y)

sigma = st.sidebar.slider(
    "Deposition Spread (m)",
    min_value=1.0,
    max_value=15.0,
    value=4.0,
    step=0.5
)

amplitude = 1.0
field = np.zeros((N, N))

for i in range(len(sample_times)):

    if sample_times[i] > current_time:
        break

    if not dispensing[i]:
        continue

    # Wind shifts the center of each deposition footprint
    center_x = sample_x[i] + drift_x
    center_y = sample_y[i] + drift_y

    gaussian = amplitude * np.exp(
        -(
            (X - center_x)**2 +
            (Y - center_y)**2
        ) / (2 * sigma**2)
    )

    field += gaussian * dt
# END TODO


# Create heatmap
fig, ax = plt.subplots()
heatmap = ax.imshow(
        field, 
        cmap="viridis", # maps low values to purple, high values to yellow 
        origin="lower", # places row 0 at the bottom of the field
        extent=[0, field_width, 0, field_height],
        vmin=0, # Ensure colors have same meaning throughout playback
        vmax=field.max() # ^
)

# Overlay flight path
ax.plot(
        trajectory[:, 0],
        trajectory[:, 1],
        color="white",
        linewidth=2,
        linestyle="-"
)

# Completed flight path START TODO
completed_x = positions[timestamps <= current_time, 0]
completed_y = positions[timestamps <= current_time, 1]

# Include the drone's interpolated current position
completed_x = np.append(completed_x, drone_x)
completed_y = np.append(completed_y, drone_y)

ax.plot(
    completed_x,
    completed_y,
    color="cyan",
    linewidth=3,
    zorder=8
)
# END TODO

# Overlay drone position
ax.scatter(
    drone_x,
    drone_y,
    color="red",
    s=120,
    marker="o",
    edgecolors="white",
    linewidths=2,
    zorder=10,
    label="Drone"
)

ax.legend(loc="upper right")

# Overlay wind vector
arrow_x = 85
arrow_y = 15

arrow_length = 15  # Visual length in meters

if wind_speed > 0:
    ax.arrow(
        arrow_x,
        arrow_y,
        arrow_length * np.cos(wind_angle),
        arrow_length * np.sin(wind_angle),
        color="cyan",
        width=0.6,
        head_width=3,
        head_length=4,
        length_includes_head=True,
        zorder=5
    )

# Wind speed label
ax.text(
    70,
    10,
    f"Wind: {wind_speed:.1f} m/s",
    color="cyan",
    fontsize=10,
    fontweight="bold",
    zorder=6
)

# Color legend
fig.colorbar(
    heatmap,
    ax=ax,
    label="Relative Deposition"
)

ax.set_title("Field Deposition Heatmap")
ax.set_xlabel("X Position (m)")
ax.set_ylabel("Y Position (m)")


# --- Dashboard Layout ---
# START TODO: Clean up dashboard
metrics["duration"] = mission_duration / 60
map_col, metrics_col = st.columns([3, 1], gap="large")

with map_col:
    st.pyplot(fig, width="stretch")

with metrics_col:
    st.subheader("Mission Metrics (Placeholders)")

    st.metric(
        "Flight Duration",
        f"{metrics['duration']:.1f} min"
    )

    st.metric(
        "Energy Consumed",
        f"{metrics['energy_used']:.0f} Wh"
    )

    st.metric(
        "Field Coverage",
        f"{metrics['coverage']:.1f}%"
    )

    st.metric(
        "Deposition CV",
        f"{metrics['uniformity_cv']:.1f}%"
    )

    st.metric(
        "Payload Remaining",
        f"{metrics['payload_remaining']:.1f} kg"
    )

plt.close(fig)
# END TODO
