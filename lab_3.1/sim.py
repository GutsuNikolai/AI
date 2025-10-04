from __future__ import annotations
import numpy as np
from typing import List
from agent import Agent
from config import P

def neighbour_indices(pos_list: np.ndarray, i: int, radius: float) -> list:
    pi = pos_list[i]
    d2 = np.sum((pos_list - pi)**2, axis=1)
    within = np.where(d2 <= radius*radius)[0]
    return [int(j) for j in within if j != i]

def step_agents(agents: List[Agent], world) -> List[Agent]:
    pos = np.array([a.pos for a in agents], dtype=float)
    survivors: List[Agent] = []
    for i, ag in enumerate(agents):
        idxs = neighbour_indices(pos, i, P.radius)
        neighbors = [agents[j] for j in idxs]
        ag.step(neighbors, world)
        if not world.in_exit(ag.pos):
            survivors.append(ag)
    return survivors
