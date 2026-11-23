# SPREAD

Run from the repository root:

```sh
pip install -r requirements.txt
streamlit run app.py

# Standalone planning demonstrations:
python -m examples.terrain_demo
python -m examples.terrain_integration
python -m planning.terrain
```

## Source organization

| Location                      | Responsibility / original source                                                   |
| ----------------------------- | ---------------------------------------------------------------------------------- |
| `config.py`                   | Configuration dataclasses from main/configure.py                                   |
| `simulation/state.py`         | Drone and FSW runtime classes from main/configure.py                               |
| `simulation/runner.py`        | main/run_sim.py                                                                    |
| `simulation/integrators.py`   | main/runge_kutta_4.py                                                              |
| `control/trans_pid.py`        | main/fsw/trans_pid.py                                                              |
| `physics/`                    | main physics models and sim_physics.py; body calculation remains separate          |
| `planning/coverage.py`        | mission-planning coverage generation; replaces duplicate dashboard path generation |
| `planning/terrain.py`         | mission-planning terrain functions and original guarded demo                       |
| `visualization/dashboard.py`  | main/spread.py dashboard and current orchestration                                 |
| `visualization/deposition.py` | Original Gaussian accumulation loop                                                |
| `visualization/plots.py`      | visuals.py helpers                                                                 |
| `examples/`                   | Terrain demos                                                                      |


