Crowd Simulation (Boids + Goal) — Starter Project
=================================================

Stack: Python 3.x, pygame, numpy, matplotlib

Install deps (one time):
    pip install pygame numpy matplotlib

Run:
    python main.py

What’s included now
-------------------
- Minimal world (rect room) with one exit.
- Agents with Goal + Separation (basic).
- Pygame visualization + simple FPS counter.
- Clear TODOs for: Alignment, Cohesion, better wall handling, metrics, experiments.

File map
--------
main.py      - entry point, sets params, creates world+agents, runs loop
agent.py     - Agent class and behavior rules (goal, separation, TODO others)
world.py     - World (walls, exit), collision helpers
sim.py       - Simulation step (neighbour search, update, remove evac'd agents)
viz.py       - Pygame drawing helpers
config.py    - Tunable parameters in one place
