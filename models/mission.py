"""Convert a geometric flight plan into a constant-speed mission timeline."""

from dataclasses import dataclass

import numpy as np


@dataclass
class Mission:
    """Timed waypoints and integration intervals; positions in m, times in s.

    Each interval lies entirely within one flight-plan segment. Its position
    is sampled at its midpoint and its dispensing flag describes that interval.
    """

    waypoints: np.ndarray
    waypoint_times: np.ndarray
    interval_edges: np.ndarray
    sample_positions: np.ndarray
    dispensing: np.ndarray

    @property
    def duration(self):
        return float(self.waypoint_times[-1])

    def position_at(self, time):
        """Interpolate position, clamping times to the mission bounds."""
        return np.array([
            np.interp(time, self.waypoint_times, self.waypoints[:, axis])
            for axis in (0, 1)
        ])

    def elapsed_intervals(self, time):
        """Seconds elapsed in each interval at a playback time."""
        return np.clip(
            time - self.interval_edges[:-1],
            0,
            np.diff(self.interval_edges),
        )


def sample_mission(waypoints, dispensing_segments, flight_speed=5.0, dt=0.5):
    """Sample a plan without crossing pass/turn boundaries.

    flight_speed is in m/s. dt is the maximum integration interval in seconds.
    Segment flags apply from waypoint i to waypoint i + 1.
    """
    waypoints = np.asarray(waypoints, dtype=float)
    flags = np.asarray(dispensing_segments, dtype=bool)
    if waypoints.ndim != 2 or waypoints.shape[1] != 2 or len(waypoints) < 2:
        raise ValueError("Waypoints must have shape (N, 2), with N >= 2.")
    if not np.all(np.isfinite(waypoints)):
        raise ValueError("Waypoints must be finite.")
    if flags.shape != (len(waypoints) - 1,):
        raise ValueError("Provide one dispensing flag per waypoint segment.")
    if not np.isfinite(flight_speed) or flight_speed <= 0:
        raise ValueError("Flight speed must be finite and positive.")
    if not np.isfinite(dt) or dt <= 0:
        raise ValueError("Sample interval must be finite and positive.")

    lengths = np.linalg.norm(np.diff(waypoints, axis=0), axis=1)
    if np.any(lengths <= 0):
        raise ValueError("Consecutive waypoints must be distinct.")
    times = np.r_[0., np.cumsum(lengths) / flight_speed]
    # Include every waypoint boundary so a sample never mixes a pass and turn.
    edges = np.unique(np.r_[np.arange(0., times[-1], dt), times])
    midpoints = edges[:-1] + np.diff(edges) / 2
    segment_indices = np.searchsorted(times, midpoints, side="right") - 1
    positions = np.column_stack([
        np.interp(midpoints, times, waypoints[:, axis]) for axis in (0, 1)
    ])
    return Mission(waypoints, times, edges, positions, flags[segment_indices])
