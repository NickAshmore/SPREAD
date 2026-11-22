# SPREAD

Prototype dashboard for agricultural-drone flight planning and illustrative
material deposition. The constant-speed mission and Gaussian deposition are
placeholders for the future simulation engine.

## Run

From the repository root, with Python 3.9 or later:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
streamlit run mock_sim.py
```

## Where to work

| File | Responsibility |
| --- | --- |
| `mock_sim.py` | Streamlit inputs, calls to the models, dashboard layout, and mock metrics |
| `models/trajectory.py` | Alternating passes and semicircular turns; planned dispensing per segment |
| `models/mission.py` | Constant-speed timing, position interpolation, and timed application samples |
| `models/deposition.py` | Illustrative wind drift and Gaussian deposition integration |
| `visualization.py` | Matplotlib heatmap, flight path, drone position, and wind arrow |
| `models/power.py` | Reserved for a future power model |

The data flow is:

```text
UI inputs -> waypoints + segment flags -> Mission -> deposition grid -> figure
```

The model modules have no Streamlit dependency. For example, from the repo root:

```python
from models.trajectory import generate_trajectory
from models.mission import sample_mission
from models.deposition import deposition_grid, wind_vector

points, flags = generate_trajectory(100., 100., 9., 8.)
mission = sample_mission(points, flags, flight_speed=5., dt=0.5)
field = deposition_grid(
    mission, mission.duration, 100., 100., wind=wind_vector(3., 90.)
)
```

## Conventions and assumptions

- Distances and coordinates are meters, time is seconds, speed is m/s.
- The origin is the bottom-left of the field; +x is right and +y is up.
- Wind direction points **toward** the indicated direction: 0 degrees is +x,
  90 degrees is +y. This is not the meteorological "from" convention.
- A plan with N waypoints has N-1 dispensing flags. Flag i applies to movement
  from waypoint i to i+1. Passes permit application; turns do not.
- `Mission` stores waypoint times and integration intervals split at every
  waypoint boundary. Each interval has a midpoint position and dispensing flag.
  `dt` is the maximum interval length. Playback accumulates only elapsed time;
  interval midpoint positions approximate the moving source.
- The field array uses rows for y and columns for x. Values are relative
  deposition, not calibrated mass. Wind drift and Gaussian spread are mock models.
- The heatmap rescales to each frame's maximum; colors do not share an absolute
  scale across playback times.
- Flight duration is calculated. Energy, coverage, uniformity, and remaining
  payload are explicitly displayed as placeholders.

Replace the mission timing and deposition models as the engine develops, keeping
units and interfaces documented. Actual dispensing may later also depend on
payload, flow rate, and controller state in addition to the plan's intent.

## Checks

From the repository root:

```sh
python -m unittest discover -s models -p 'test_*.py'
```
