from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from typing import List
from config import P

Vec = np.ndarray

def norm(v: Vec) -> float:
    return float(np.linalg.norm(v))

def unit(v: Vec) -> Vec:
    n = norm(v)
    return v/n if n > 1e-6 else np.zeros_like(v)

@dataclass
class Agent:
    pos: Vec
    vel: Vec

    def goal_vec(self, world) -> Vec:
        return world.nearest_exit_dir(self.pos)

    def separation_vec(self, neighbors: List['Agent']) -> Vec:
        force = np.zeros(2, dtype=float)
        for nb in neighbors:
            d = self.pos - nb.pos
            dist = norm(d)
            if dist < 1e-6: 
                continue
            if dist < P.d_min * 1.2:
                force += unit(d) * (1.0 / max(dist, 8.0))
        return force

    def alignment_vec(self, neighbors: List['Agent']) -> Vec:
        if not neighbors: return np.zeros(2)
        v_avg = np.mean([nb.vel for nb in neighbors], axis=0)
        return unit(v_avg)

    def cohesion_vec(self, neighbors: List['Agent']) -> Vec:
        if not neighbors: return np.zeros(2)
        center = np.mean([nb.pos for nb in neighbors], axis=0)
        return unit(center - self.pos)

    def step(self, neighbors: List['Agent'], world) -> None:
        g = self.goal_vec(world) * P.w_goal
        s = self.separation_vec(neighbors) * P.w_sep
        a = self.alignment_vec(neighbors) * P.w_ali
        c = self.cohesion_vec(neighbors) * P.w_coh

        desire = g + s + a + c
        if norm(desire) > 1e-6:
            desire = unit(desire) * P.amax

        self.vel = self.vel + desire * P.dt
        speed = norm(self.vel)
        if speed > P.vmax:
            self.vel = self.vel * (P.vmax / speed)

        self.pos = self.pos + self.vel * P.dt
        self.pos = world.clamp_inside(self.pos)
