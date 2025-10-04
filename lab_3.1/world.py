from __future__ import annotations
from dataclasses import dataclass
from typing import List
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
        # One exit on the right wall
        exit_w, exit_h = 24, 80
        exit_y = height // 2 - exit_h // 2
        # ставим дверь ВНУТРИ на 2 пикселя от правой кромки, чтобы в неё можно было «войти»
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

    def clamp_inside(self, p: Vec) -> Vec:
        # по умолчанию правая граница — стена
        right_limit = self.width - 6

        # если по y агент находится на уровне двери — позволим x заходить ДО края двери
        for ex in self.exits:
            if ex.y - 2 <= p[1] <= ex.y + ex.h + 2:
                right_limit = ex.x + ex.w
                break

        p[0] = np.clip(p[0], 6, right_limit)
        p[1] = np.clip(p[1], 6, self.height - 6)
        return p

