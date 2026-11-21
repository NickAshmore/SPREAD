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

# -- Visualization ---

st.title("SPREAD")
st.subheader("Simulation for Predicting Run Efficiency of Agricultural Drones")


# Heat map is an NxN array representing the field
# Each element is a location on the field, and its value is the amount of deposited material

N = 100
field = np.zeros((N, N))

# Dummy deposition values
field[20:50, 20:50] = 2.0
field[40:80, 40:80] = 5.0


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

# Color legend
fig.colorbar(heatmap, ax=ax, label="Deposition")

ax.set_title("Field Deposition Heatmap")
ax.set_xlabel("X Position (m)")
ax.set_ylabel("Y Position (m)")

# Display in Streamlit
st.pyplot(fig)
plt.close(fig)
