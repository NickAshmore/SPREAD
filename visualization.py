"""Matplotlib views of simulation results; no Streamlit dependency."""

import matplotlib.pyplot as plt
import numpy as np


def plot_mission(field, mission, current_time, field_width, field_height, wind):
    """Return a figure; the caller owns displaying and closing it."""
    fig, ax = plt.subplots()
    heatmap = ax.imshow(
        field, cmap="viridis", origin="lower",
        extent=[0, field_width, 0, field_height],
        vmin=0, vmax=max(float(field.max()), 1e-12),
    )
    path = mission.waypoints
    ax.plot(path[:, 0], path[:, 1], color="white", linewidth=2)
    position = mission.position_at(current_time)
    completed = np.vstack([path[mission.waypoint_times <= current_time], position])
    ax.plot(completed[:, 0], completed[:, 1], color="cyan", linewidth=3, zorder=8)
    ax.scatter(*position, color="red", s=120, edgecolors="white",
               linewidths=2, zorder=10, label="Drone")
    ax.legend(loc="upper right")

    speed = np.linalg.norm(wind)
    if speed > 0:
        arrow = np.asarray(wind) / speed * min(field_width, field_height) * 0.15
        ax.arrow(field_width * 0.85, field_height * 0.15, *arrow,
                 color="cyan", width=0.6, head_width=3, head_length=4,
                 length_includes_head=True, zorder=5)
    ax.text(field_width * 0.7, field_height * 0.1,
            f"Wind: {speed:.1f} m/s", color="cyan", fontsize=10,
            fontweight="bold", zorder=6)
    fig.colorbar(heatmap, ax=ax, label="Relative Deposition")
    ax.set(title="Field Deposition Heatmap", xlabel="X Position (m)",
           ylabel="Y Position (m)")
    return fig
