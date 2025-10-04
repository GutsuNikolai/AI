from dataclasses import dataclass

@dataclass
class Params:
    # Simulation
    dt: float = 0.06
    n_agents: int = 60
    seed: int = 7
    # Perception / behavior
    radius: float = 70.0          # pixels (visual radius)
    d_min: float = 18.0           # personal space (px)
    vmax: float = 90.0            # px/sec
    amax: float = 240.0           # px/sec^2
    # Weights
    w_goal: float = 1.0
    w_sep: float = 1.6
    w_ali: float = 0.5
    w_coh: float = 0.3
    # Walls / repulsion
    wall_d0: float = 28.0         # influence distance to walls (px)
    w_wall: float = 1.7           # weight of wall repulsion
    # Render
    win_w: int = 900
    win_h: int = 560

P = Params()
