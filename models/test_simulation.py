"""Numerical checks independent of the Streamlit dashboard."""

import unittest

import numpy as np

from models.deposition import deposition_grid
from models.mission import sample_mission
from models.trajectory import generate_trajectory


class MissionTests(unittest.TestCase):
    def test_generated_paths_and_application_time(self):
        for spacing in (5., 8., 20.):
            margin = spacing / 2 + 5
            points, flags = generate_trajectory(100., 100., margin, spacing)
            mission = sample_mission(points, flags)
            lengths = np.linalg.norm(np.diff(points, axis=0), axis=1)
            self.assertTrue(np.all(lengths > 0))
            self.assertTrue(np.all((points >= 0) & (points <= 100)))
            durations = np.diff(mission.interval_edges)
            self.assertTrue(np.all(durations <= 0.5 + 1e-12))
            self.assertAlmostEqual(durations.sum(), mission.duration)
            self.assertAlmostEqual(
                durations[mission.dispensing].sum(), lengths[flags].sum() / 5
            )
            np.testing.assert_allclose(mission.position_at(0), points[0])
            np.testing.assert_allclose(mission.position_at(mission.duration), points[-1])

    def test_intervals_split_at_turns(self):
        mission = sample_mission([[0, 0], [0, 1], [1, 1]], [True, False], 1, 0.6)
        np.testing.assert_allclose(mission.interval_edges, [0, .6, 1, 1.2, 1.8, 2])
        np.testing.assert_array_equal(mission.dispensing, [True, True, False, False, False])
        self.assertAlmostEqual(mission.elapsed_intervals(.8).sum(), .8)

    def test_invalid_sampling_inputs(self):
        for kwargs in ({'flight_speed': 0}, {'dt': 0}):
            with self.assertRaises(ValueError):
                sample_mission([[0, 0], [1, 0]], [True], **kwargs)
        with self.assertRaises(ValueError):
            sample_mission([[0, 0], [0, 0]], [True])
        with self.assertRaises(ValueError):
            sample_mission([[0, 0], [1, 0]], [])

    def test_deposition_elapsed_time_and_turns(self):
        # The grid origin is one meter from the application interval midpoint.
        mission = sample_mission([[0, 0], [2, 0], [4, 0]], [True, False], 1, 10)
        def grid(time):
            return deposition_grid(mission, time, 4, 4, sigma=1, grid_size=5)
        np.testing.assert_array_equal(grid(0), np.zeros((5, 5)))
        self.assertAlmostEqual(grid(.25)[0, 0], np.exp(-.5) * .25)
        self.assertAlmostEqual(grid(2)[0, 0], np.exp(-.5) * 2)
        np.testing.assert_allclose(grid(2), grid(4))
        np.testing.assert_allclose(grid(4), grid(100))


if __name__ == '__main__':
    unittest.main()
