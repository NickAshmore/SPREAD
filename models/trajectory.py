"""Plan application passes connected by semicircular turns."""

import numpy as np


def generate_trajectory(field_width, field_height, field_margin, line_spacing):
    """Return waypoints and intended dispensing state for each segment.

    Dimensions are in meters. field_margin measures from the top/bottom
    boundary to straight-pass endpoints. Turns extend outward from those
    endpoints by half the line spacing.

    Returns:
        waypoints: Float array of shape (N, 2), containing (x, y) positions.
        dispensing_segments: Boolean array of shape (N - 1,). Entry i
            describes movement from waypoints[i] to waypoints[i + 1].
            Passes are True; turns are False. The simulation determines
            actual dispensing from this planned intent.
    """
    if not np.all(np.isfinite((field_width, field_height, field_margin, line_spacing))):
        raise ValueError("Dimensions, margin, and spacing must be finite.")
    if field_width <= 0 or field_height <= 0 or line_spacing <= 0:
        raise ValueError("Field dimensions and line spacing must be positive.")
    if not 0 <= field_margin < field_height / 2:
        raise ValueError("Margin must be nonnegative and less than half the height.")

    flight_lines = np.arange(line_spacing / 2, field_width, line_spacing)
    if len(flight_lines) == 0:
        raise ValueError("Line spacing leaves no flight lines inside the field.")
    if len(flight_lines) > 1 and field_margin < line_spacing / 2:
        raise ValueError("Margin must accommodate the semicircular turns.")

    path = [[flight_lines[0], field_margin]]
    dispensing_segments = []

    for i, x in enumerate(flight_lines):
        upward = i % 2 == 0
        end_y = field_height - field_margin if upward else field_margin
        path.append([x, end_y])
        dispensing_segments.append(True)

        if i == len(flight_lines) - 1:
            continue

        next_x = flight_lines[i + 1]
        radius = (next_x - x) / 2
        center_x = (x + next_x) / 2
        end_angle = 0 if upward else 2 * np.pi

        # Start already exists; use an exact endpoint shared with the next pass.
        for angle in np.linspace(np.pi, end_angle, 30)[1:-1]:
            path.append([
                center_x + radius * np.cos(angle),
                end_y + radius * np.sin(angle),
            ])
            dispensing_segments.append(False)
        path.append([next_x, end_y])
        dispensing_segments.append(False)

    return np.asarray(path, dtype=float), np.asarray(dispensing_segments, dtype=bool)
