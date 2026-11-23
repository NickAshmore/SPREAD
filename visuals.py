import numpy as np

""" Overlays an arrow and wind speed text onto the deposition heatmap"""
def overlay_wind(
    ax,
    x: float,
    y: float,
    wind_speed: float,
    wind_angle: float,
    arrow_length: int = 15,
    color: str = "cyan",
    width: float = 0.5,
    head_width: float = 3.0,
    head_length: float = 4.0,
) -> None:
    if wind_speed == 0:
        return

    ax.arrow(
        x,
        y,
        arrow_length * np.cos(wind_angle),
        arrow_length * np.sin(wind_angle),
        color=color,
        width=width,
        head_width=head_width,
        head_length=head_length,
        length_includes_head=True,
        zorder=5,
    )
    
    ax.annotate(
        f"Wind: {wind_speed:.1f} m/s",
        xy=(x, y),
        xytext=(10, 10),
        textcoords="offset points",
        color=color,
        fontsize=10,
        fontweight="bold",
        zorder=6,
    )

def plot_trajectory(
    ax,
    trajectory,
    color: str = "white",
    width: float = 0.6,
    style: str = "-",

) -> None:
    ax.plot(
        trajectory[:, 0], # x
        trajectory[:, 1], # y
        color=color,
        linewidth=width,
        linestyle=style

    )
