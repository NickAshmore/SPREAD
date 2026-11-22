
import numpy as np


def generate_coverage_path(flight_lines, field_height, field_margin):
    """
    Generate a 2D lawnmower coverage path with semicircular turns.

    flight_lines: X positions of the coverage passes (meters)
    field_height: Field height in the Y direction (meters)
    field_margin: Margin at each end of a straight pass (meters)
    """

    path = []

    for i, x in enumerate(flight_lines):

        # Alternate upward and downward passes
        if i % 2 == 0:
            path.append([x, field_margin])
            path.append([x, field_height - field_margin])
        else:
            path.append([x, field_height - field_margin])
            path.append([x, field_margin])

        # Connect adjacent passes using semicircular turns
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

    return np.array(path, dtype=float)


def calculate_path_distance(trajectory):
    """Calculate total distance between consecutive waypoints."""

    segments = np.diff(trajectory, axis=0)
    distances = np.linalg.norm(segments, axis=1)

    return np.sum(distances)
