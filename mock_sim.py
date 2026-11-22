"""Streamlit entry point for the mock simulation dashboard."""

import matplotlib.pyplot as plt
import streamlit as st

from models.deposition import deposition_grid, wind_vector
from models.mission import sample_mission
from models.trajectory import generate_trajectory
from visualization import plot_mission


# Mock assumptions, in meters, seconds, and meters per second.
FIELD_WIDTH = 100.0
FIELD_HEIGHT = 100.0
FLIGHT_SPEED = 5.0
SAMPLE_INTERVAL = 0.5
GRID_SIZE = 200


def mission_controls():
    """Collect user inputs; numerical model modules do not depend on the UI."""
    line_spacing = st.sidebar.slider(
        "Flight Line Spacing (m)", 5.0, 20.0, 8.0, 1.0
    )
    wind_speed = st.sidebar.slider("Wind Speed (m/s)", 0.0, 15.0, 3.0, 0.5)
    wind_direction = st.sidebar.slider("Wind Direction (°)", 0, 359, 90, 5)
    sigma = st.sidebar.slider("Deposition Spread (m)", 1.0, 15.0, 4.0, 0.5)
    return line_spacing, wind_vector(wind_speed, wind_direction), sigma


def display_metrics(mission):
    """Only duration is calculated; other metrics await the real engine."""
    st.subheader("Mission Metrics")
    st.metric("Flight Duration", f"{mission.duration / 60:.1f} min")
    st.caption("The following values are placeholders.")
    st.metric("Energy Consumed", "185 Wh")
    st.metric("Field Coverage", "92.4%")
    st.metric("Deposition CV", "18.6%")
    st.metric("Payload Remaining", "12.5 kg")


def main():
    st.title("SPREAD")
    st.subheader("Simulation for Predicting Run Efficiency of Agricultural Drones")
    line_spacing, wind, sigma = mission_controls()

    # Leave five meters beyond each turn before the top/bottom field edge.
    field_margin = line_spacing / 2 + 5.0
    waypoints, dispensing_segments = generate_trajectory(
        FIELD_WIDTH, FIELD_HEIGHT, field_margin, line_spacing
    )
    mission = sample_mission(
        waypoints, dispensing_segments, FLIGHT_SPEED, SAMPLE_INTERVAL
    )
    current_time = st.slider(
        "Mission Progress (seconds)", 0.0, mission.duration, 0.0, 1.0
    )
    field = deposition_grid(
        mission, current_time, FIELD_WIDTH, FIELD_HEIGHT,
        wind=wind, sigma=sigma, grid_size=GRID_SIZE,
    )
    fig = plot_mission(
        field, mission, current_time, FIELD_WIDTH, FIELD_HEIGHT, wind
    )
    map_col, metrics_col = st.columns([3, 1], gap="large")
    try:
        with map_col:
            st.pyplot(fig, width="stretch")
        with metrics_col:
            display_metrics(mission)
    finally:
        plt.close(fig)


if __name__ == "__main__":
    main()
