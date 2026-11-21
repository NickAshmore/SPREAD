import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

st.title("SPREAD")
st.subheader("Simulation for Predicting Run Efficiency of Agricultural Drones")


# Heat map is an NxN array representing the field
# Each element is a location on the field, and its value is the amount of deposited material
N = 100
field_width = 50.0 # meters
field_height = 50.0 # meters
field = np.zeros((N, N))

# Dummy deposition values
field[20:50, 20:50] = 2.0
field[40:80, 40:80] = 5.0




# Display heatmap
fig, ax = plt.subplots()
heatmap = ax.imshow(field, cmap="viridis", origin="lower", extent=[0, field_width, 0, field_height])
    # cmap="viridis" maps low values to purple, high values to yellow
    # origin="lower" places row 0 at the bottom rather than the top

# Color legend
fig.colorbar(heatmap, ax=ax, label="Deposition")

ax.set_title("Field Deposition Heatmap")
ax.set_xlabel("X Position")
ax.set_ylabel("Y Position")

# Display in Streamlit
st.pyplot(fig)
plt.close(fig)
