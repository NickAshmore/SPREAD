import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# --- Mission Parameters ---

field_width  = 100.0 # meters
field_height = 100.0 # meters


line_spacing = st.sidebar.slider(
        "Flight Line Spacing (m)", 
        min_value=2.0, 
        max_value=20.0, 
        value=8.0, 
        step=1.0
)

# --- Flight Path Generation ---

flight_lines = np.arange(
        line_spacing / 2, # Starting x coord
        field_width, # Final x coord
        line_spacing # Spacing between each line
)

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
for x in flight_lines:
    ax.axvline(
        x=x, 
        color="white", 
        linestyle="--", 
        linewidth=1.5, 
        alpha=0.8
    )

# Color legend
fig.colorbar(heatmap, ax=ax, label="Deposition")

ax.set_title("Field Deposition Heatmap")
ax.set_xlabel("X Position (m)")
ax.set_ylabel("Y Position (m)")

# Display in Streamlit
st.pyplot(fig)
plt.close(fig)
