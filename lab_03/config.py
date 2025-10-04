from dataclasses import dataclass

@dataclass
class Params:
    # Simulation
    dt: float = 0.06
    n_agents: int = 60
    seed: int = 7
    # Perception / behavior
    radius: float = 700.0          # радиус поиска других агетов
    d_min: float = 18.0           # личное пространство
    vmax: float = 90.0            # px/sec - макс. скорость
    amax: float = 240.0           # px/sec^2 - макс. ускорение
    # Weights
    w_goal: float = 1.3
    w_sep: float = 1000.5
    w_ali: float = 0.5
    w_coh: float = 0.3
    # Walls / repulsion
    wall_d0 = 16.0  # радиус видимости стен
    w_wall = 3.0  # сила отталкивания от стен
    # Render
    win_w: int = 900
    win_h: int = 560

P = Params()
