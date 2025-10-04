import pygame as pg
import numpy as np
from config import P

WHITE=(240,240,240); GREEN=(20,200,80); BLUE=(40,120,220); BLACK=(25,25,25);RED = (220, 60, 60)
GLOW_SURF = None

def init_window(w, h):
    pg.init()
    screen = pg.display.set_mode((w,h))
    pg.display.set_caption("Pedestrians (Boids + Goal)")
    return screen

def draw_world(screen, world):
    screen.fill(WHITE)
    # полупрозрачные красные прямоугольники для зон спавна
    if hasattr(world, "zones"):
        import pygame as pg
        overlay = pg.Surface(screen.get_size(), pg.SRCALPHA)  # отдельный слой с альфой
        for (x, y, w, h) in world.zones:
            pg.draw.rect(overlay, (220, 60, 60, 70), pg.Rect(x, y, w, h), border_radius=10)  # RGBA, alpha=70
            pg.draw.rect(overlay, (200, 40, 40, 180), pg.Rect(x, y, w, h), width=2, border_radius=10)
        screen.blit(overlay, (0, 0))
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

def _get_glow():
    global GLOW_SURF
    if GLOW_SURF: return GLOW_SURF
    R = 10
    s = pg.Surface((R*2, R*2), pg.SRCALPHA)
    #pg.draw.circle(s, (255, 189, 56, 90), (R, R), R)  - ВКЛЮЧИТЬ ПОДСТВЕТКУ
    GLOW_SURF = s
    return GLOW_SURF

def draw_agents(screen, agents):
    glow = _get_glow()
    for a in agents:
        x, y = int(a.pos[0]), int(a.pos[1])
        screen.blit(glow, (x - glow.get_width() // 2, y - glow.get_height() // 2))
        p = (int(a.pos[0]), int(a.pos[1]))
        v = a.vel
        if np.linalg.norm(v) > 1e-6:
            d = (int(p[0]+0.8*v[0]*0.1), int(p[1]+0.8*v[1]*0.1))
            pg.draw.line(screen, BLUE, p, d, 2)

        pg.draw.circle(screen, BLUE, p, 4)

