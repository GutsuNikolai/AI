from dataclasses import dataclass

@dataclass
class Params:
    # Simulation
    dt: float = 0.16
    n_agents: int = 200
    seed: int = 7
    # Perception / behavior
    radius: float = 70.0          # радиус поиска других агетов
    d_min: float = 18.0           # личное пространство
    vmax: float = 90.0            # px/sec - макс. скорость
    amax: float = 240.0           # px/sec^2 - макс. ускорение
    # Weights
    w_goal: float = 2.6
    w_sep: float = .0
    w_ali: float = 0.5
    w_coh: float = 0.3
    # Walls / repulsion
    wall_d0 = 16.0  # радиус видимости стен
    w_wall = 3.0  # сила отталкивания от стен
    # Render
    win_w: int = 900
    win_h: int = 560

P = Params()
