import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

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

# --- Wind Vector ---

wind_angle = np.radians(wind_direction)
wind_x = wind_speed * np.cos(wind_angle)
wind_y = wind_speed * np.sin(wind_angle)

# -- Visualization ---

st.title("SPREAD")
st.subheader("Simulation for Predicting Run Efficiency of Agricultural Drones")


# Heat map is an NxN array representing the field
# Each element is a location on the field, and its value is the amount of deposited material

N = 100
field = np.zeros((N, N))

# START TODO Remove dummy data and replace with simulated deposition

drift_factor = 1.5  # Illustrative meters of drift per m/s

drift_x = wind_x * drift_factor
drift_y = wind_y * drift_factor 


# --- Gaussian Deposition Model ---

N = 200
field = np.zeros((N, N))

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

# Distance from each grid cell to the application region
y_min = field_margin
y_max = field_height - field_margin

distance_y = np.maximum(
    np.maximum(y_min - (Y - drift_y), (Y - drift_y) - y_max),
    0
)

for x_line in flight_lines:

    distance_x = X - (x_line + drift_x)
    gaussian = amplitude * np.exp(
        -(distance_x**2 + distance_y**2) / (2 * sigma**2)
    )

    field += gaussian

# END TODO


# Create heatmap
fig, ax = plt.subplots()
heatmap = ax.imshow(
        field, 
        cmap="viridis", # maps low values to purple, high values to yellow 
        origin="lower", # places row 0 at the bottom of the field
        extent=[0, field_width, 0, field_height]
)

# Overlay flight path
ax.plot(
        trajectory[:, 0],
        trajectory[:, 1],
        color="white",
        linewidth=2,
        linestyle="-"
)

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

# Display in Streamlit
st.pyplot(fig)
plt.close(fig)
