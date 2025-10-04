from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple
import numpy as np

Vec = np.ndarray

@dataclass
class Exit:
    x: int; y: int; w: int; h: int  # axis-aligned rect
    def contains(self, p: Vec) -> bool:
        return (self.x <= p[0] <= self.x + self.w) and (self.y <= p[1] <= self.y + self.h)

@dataclass
class Wall:
    x1: int; y1: int; x2: int; y2: int   # line segment (for future use)

@dataclass
class World:
    width: int; height: int
    walls: list
    exits: list

    @staticmethod
    def simple_room(width: int, height: int) -> 'World':
        # One exit on the right wall (inset a bit inside)
        exit_w, exit_h = 30, 90
        exit_y = height // 2 - exit_h // 2
        exit_x = width - exit_w - 2
        return World(width, height, walls=[], exits=[Exit(exit_x, exit_y, exit_w, exit_h)])

    def nearest_exit_dir(self, p: Vec) -> Vec:
        centers = [np.array([e.x + e.w/2, e.y + e.h/2], dtype=float) for e in self.exits]
        dists = [np.linalg.norm(c - p) for c in centers]
        target = centers[int(np.argmin(dists))]
        v = target - p
        n = np.linalg.norm(v)
        return v / n if n > 1e-6 else np.zeros(2)

    def in_exit(self, p: Vec) -> bool:
        return any(e.contains(p) for e in self.exits)

    def wall_repulsion(self, p: Vec, d0: float) -> Vec:
        """Repulsion away from room boundaries within distance d0.
        Returns a unit vector to interior; strength is handled by weight.
        """
        fx = 0.0; fy = 0.0
        dl = p[0] - 6.0                      # left
        right_limit = self.width - 6.0       # right baseline
        for ex in self.exits:
            if ex.y - 2 <= p[1] <= ex.y + ex.h + 2:
                right_limit = ex.x + ex.w
                break
        dr = right_limit - p[0]              # right
        dt = p[1] - 6.0                      # top
        db = (self.height - 6.0) - p[1]      # bottom
        if dl < d0: fx += (1.0 / max(dl, 1.0))
        if dr < d0: fx -= (1.0 / max(dr, 1.0))
        if dt < d0: fy += (1.0 / max(dt, 1.0))
        if db < d0: fy -= (1.0 / max(db, 1.0))
        v = np.array([fx, fy], dtype=float)
        n = np.linalg.norm(v)
        return v / n if n > 1e-9 else np.zeros(2)

    def clamp_and_slide(self, p: Vec, v: Vec) -> Tuple[Vec, Vec]:
        """Clamp inside room; if we hit boundary, zero normal component of velocity.
        Right boundary is permeable at exit Y-span (limit at exit edge).
        Returns (p_clamped, v_adjusted).
        """
        x, y = float(p[0]), float(p[1])
        vx, vy = float(v[0]), float(v[1])
        hit_x = False; hit_y = False
        # Right boundary may move to exit edge
        right_limit = self.width - 6.0
        for ex in self.exits:
            if ex.y - 2 <= y <= ex.y + ex.h + 2:
                right_limit = ex.x + ex.w
                break
        # Clamp X
        if x < 6.0:
            x = 6.0; hit_x = True
        elif x > right_limit:
            x = right_limit; hit_x = True
        # Clamp Y
        if y < 6.0:
            y = 6.0; hit_y = True
        elif y > self.height - 6.0:
            y = self.height - 6.0; hit_y = True
        if hit_x: vx = 0.0
        if hit_y: vy = 0.0
        return np.array([x, y], dtype=float), np.array([vx, vy], dtype=float)

    def clamp_inside(self, p: Vec) -> Vec:
        right_limit = self.width - 6.0
        for ex in self.exits:
            if ex.y - 2 <= p[1] <= ex.y + ex.h + 2:
                right_limit = ex.x + ex.w
                break
        p[0] = np.clip(p[0], 6, right_limit)
        p[1] = np.clip(p[1], 6, self.height - 6)
        return p
