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
    w_goal: float = 1.3
    w_sep: float = 2.0
    w_ali: float = 0.5
    w_coh: float = 0.3
    # Walls / repulsion
    wall_d0 = 36.0  # радиус "видимости" стен
    w_wall = 2.0  # сила отталкивания от стен         # weight of wall repulsion
    # Render
    win_w: int = 900
    win_h: int = 560

P = Params()
