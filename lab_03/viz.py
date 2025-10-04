import pygame as pg
import numpy as np
from config import P

WHITE=(240,240,240); GREEN=(20,200,80); BLUE=(40,120,220); BLACK=(25,25,25)

def init_window(w, h):
    pg.init()
    screen = pg.display.set_mode((w,h))
    pg.display.set_caption("Pedestrians (Boids + Goal)")
    return screen

def draw_world(screen, world):
    screen.fill(WHITE)

    # --- прямоугольные стены ---
    if hasattr(world, "rects"):
        for r in world.rects:
            pg.draw.rect(screen, BLACK, pg.Rect(r.x, r.y, r.w, r.h))

    # --- круглые стены (дуги) ---
    if hasattr(world, "circles"):
        for c in world.circles:
            # толщина 6 px; можно сделать заполненный круг, если нужно
            pg.draw.circle(screen, BLACK, (int(c.cx), int(c.cy)), int(c.r), width=6)

    # --- выходы ---
    for ex in world.exits:
        pg.draw.rect(screen, GREEN, pg.Rect(ex.x, ex.y, ex.w, ex.h))

def draw_agents(screen, agents):
    for a in agents:
        p = (int(a.pos[0]), int(a.pos[1]))
        v = a.vel
        if np.linalg.norm(v) > 1e-6:
            d = (int(p[0]+0.8*v[0]*0.1), int(p[1]+0.8*v[1]*0.1))
            pg.draw.line(screen, BLUE, p, d, 2)
        pg.draw.circle(screen, BLUE, p, 4)
