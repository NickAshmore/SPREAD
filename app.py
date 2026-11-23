import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

from models.trajectory import generate_trajectory
from visuals import overlay_wind, plot_trajectory

def main():
    # --- Mission Parameters ---
        # line_spacing
        # wind_speed
        # wind_direction
        # field_width
        # field_margin
    mission = get_parameters()

    # --- Simulation Outputs ---
    outputs = run_sim(mission)

    
    # TODO Move into simulation.py
    trajectory = generate_trajectory(
            field_width=field_width, 
            field_height=field_height,
            field_margin=field_margin
            line_spacing=line_spacing,
    )


    # --- Create Dashboard ---
    
    create_dashboard(outputs)

    # TODO Move into visualization.py or dashboard.py
    # TODO Display heatmap
    
    plot_trajectory(
        ax,
        trajectory,
    )

    overlay_wind(
        ax,
        x=,
        y=,
        wind_speed=,
        wind_angle=,
    )
    




if __name__ == "__main__":
    main()
