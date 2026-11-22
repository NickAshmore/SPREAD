"""Illustrative Gaussian deposition; replace this model with engine physics."""

import numpy as np


def wind_vector(speed, direction_degrees):
    """Return (x, y) velocity in m/s; 0 degrees is +x, 90 is +y.

    Direction describes where wind blows toward, not meteorological origin.
    """
    angle = np.radians(direction_degrees)
    return speed * np.array([np.cos(angle), np.sin(angle)])


def deposition_grid(mission, current_time, field_width, field_height,
                    wind=(0., 0.), sigma=4., grid_size=200,
                    drift_factor=1.5, amplitude=1.):
    """Integrate relative deposition through current_time (seconds).

    Grid rows are y and columns are x, spanning the field in meters.
    sigma is in meters; drift_factor is an illustrative drift in m per m/s.
    amplitude is relative intensity per second, not calibrated mass.
    Interval midpoint positions approximate motion; elapsed interval durations
    prevent deposition before time zero or beyond the selected playback time.
    """
    if not np.isfinite(sigma) or sigma <= 0:
        raise ValueError("Spread must be finite and positive.")
    if field_width <= 0 or field_height <= 0 or grid_size < 2:
        raise ValueError("Field dimensions must be positive and grid size >= 2.")
    x, y = np.meshgrid(
        np.linspace(0, field_width, grid_size),
        np.linspace(0, field_height, grid_size),
    )
    field = np.zeros_like(x)
    drift = np.asarray(wind) * drift_factor
    durations = mission.elapsed_intervals(current_time)
    for position, duration, dispensing in zip(
        mission.sample_positions, durations, mission.dispensing
    ):
        if duration <= 0 or not dispensing:
            continue
        center_x, center_y = position + drift
        gaussian = amplitude * np.exp(
            -((x - center_x)**2 + (y - center_y)**2) / (2 * sigma**2)
        )
        field += gaussian * duration
    return field
