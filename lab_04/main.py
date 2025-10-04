# life_lab5.py — Вариант 5: Glider + Blinker, 50×50
# pip install pygame numpy
import random, sys, time
from dataclasses import dataclass
from typing import Tuple
import numpy as np
import pygame as pg

# ---- Параметры ----
W, H = 50, 50                  # размер сетки
CELL = 12                      # пикселей на клетку (окно ~ 600x600)
WRAP_EDGES = True              # тор (True) / жесткие края (False)
SEED_BASE = "YourName_Group"   # поставь свое: ФИО/группа для уникального шума

# ---- Паттерны ----
GLIDER = np.array([
    [0,1,0],
    [0,0,1],
    [1,1,1]
], dtype=np.uint8)

BLINKER = np.array([[1,1,1]], dtype=np.uint8)  # горизонтальный

@dataclass
class World:
    grid: np.ndarray   # (H,W) из 0/1
    tick: int = 0

def rnd_seed():
    # сид уникален на студента, но еще чуть «шумит» от времени запуска
    base = abs(hash(SEED_BASE)) % (2**32)
    return (base + int(time.time()*1000)) % (2**32)

def random_grid(h=H, w=W, p_range=(0.2, 0.5), rng=None) -> np.ndarray:
    if rng is None: rng = random.Random()
    p = rng.uniform(*p_range)
    return (np.random.RandomState(rng.randrange(2**31)).rand(h, w) < p).astype(np.uint8)

def neighbours_torus(g: np.ndarray) -> np.ndarray:
    # сумма 8 соседей через np.roll (тор)
    s = np.zeros_like(g, dtype=np.uint8)
    for dy in (-1,0,1):
        for dx in (-1,0,1):
            if dx==0 and dy==0: continue
            s = s + np.roll(np.roll(g, dy, 0), dx, 1)
    return s

def neighbours_bounded(g: np.ndarray) -> np.ndarray:
    # без тора: за пределами считаем мертвые (чуть медленнее, но просто)
    s = np.zeros_like(g, dtype=np.uint8)
    h, w = g.shape
    for y in range(h):
        y0 = max(0,y-1); y1 = min(h, y+2)
        for x in range(w):
            x0 = max(0,x-1); x1 = min(w, x+2)
            s[y,x] = np.sum(g[y0:y1, x0:x1]) - g[y,x]
    return s

def step_conway(g: np.ndarray) -> np.ndarray:
    n = neighbours_torus(g) if WRAP_EDGES else neighbours_bounded(g)
    # правила: рождается при n=3; живет при (n==2 | n==3)
    born = (n == 3) & (g == 0)
    stay = ((n == 2) | (n == 3)) & (g == 1)
    return (born | stay).astype(np.uint8)

def can_place_free(base: np.ndarray, pat: np.ndarray, y: int, x: int) -> bool:
    h, w = pat.shape
    if y+h > base.shape[0] or x+w > base.shape[1]: return False
    # «свободная зона» — под паттерном сейчас только нули
    return np.all(base[y:y+h, x:x+w] == 0)

def try_place_pattern(base: np.ndarray, pat: np.ndarray, rng: random.Random, attempts=200) -> Tuple[int,int]:
    h, w = pat.shape
    H, W = base.shape
    for _ in range(attempts):
        y = rng.randrange(0, H - h + 1)
        x = rng.randrange(0, W - w + 1)
        if can_place_free(base, pat, y, x):
            base[y:y+h, x:x+w] |= pat  # накладываем
            return y, x
    # fallback: ищем место с минимальным конфликтом и перезатираем его
    best = None; best_conf = 10**9
    for y in range(0, H - h + 1):
        for x in range(0, W - w + 1):
            overlap = np.sum(base[y:y+h, x:x+w] & pat)
            if overlap < best_conf:
                best_conf, best = overlap, (y,x)
    if best:
        y,x = best
        base[y:y+h, x:x+w] = (base[y:y+h, x:x+w] & (1 - pat)) | pat
        return y, x
    return -1, -1

# ---------- ВИЗУАЛИЗАЦИЯ ----------
WHITE=(240,240,240); DEAD=(230,230,230); ALIVE=(35,35,35); GRID=(200,200,200)
HUD=(30,30,30)

def draw(screen, world: World, cell=CELL):
    screen.fill(WHITE)
    h, w = world.grid.shape
    # клетки
    alive = np.argwhere(world.grid == 1)
    for y, x in alive:
        pg.draw.rect(screen, ALIVE, pg.Rect(x*cell, y*cell, cell, cell))
    # сетка
    for x in range(w+1):
        pg.draw.line(screen, GRID, (x*cell,0), (x*cell,h*cell), 1)
    for y in range(h+1):
        pg.draw.line(screen, GRID, (0,y*cell), (w*cell,y*cell), 1)
    # HUD
    font = pg.font.SysFont("consolas", 18)
    txt = font.render(f"tick: {world.tick:5d} | alive: {int(np.sum(world.grid))}", True, HUD)
    screen.blit(txt, (10, 8))

def new_world(rng=None) -> World:
    if rng is None:
        rng = random.Random(rnd_seed())
    base = random_grid(H, W, (0.2, 0.5), rng)
    # добавляем glider и blinker в свободные зоны
    try_place_pattern(base, GLIDER, rng)
    try_place_pattern(base, BLINKER, rng)
    return World(grid=base, tick=0)

def main():
    pg.init()
    screen = pg.display.set_mode((W*CELL, H*CELL))
    pg.display.set_caption("Game of Life — Variant 5 (Glider + Blinker, 50x50)")
    clock = pg.time.Clock()
    rng = random.Random(rnd_seed())

    world = new_world(rng)
    paused = False

    while True:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                pg.quit(); sys.exit(0)
            elif e.type == pg.KEYDOWN:
                if e.key == pg.K_SPACE:   # пауза
                    paused = not paused
                elif e.key == pg.K_n:     # шаг вперед
                    if paused:
                        world.grid = step_conway(world.grid); world.tick += 1
                elif e.key == pg.K_r:     # пересоздать
                    world = new_world(rng); paused = False
                elif e.key == pg.K_s:     # сохранить скрин
                    pg.image.save(screen, f"life_{int(time.time())}.png")

        if not paused:
            world.grid = step_conway(world.grid)
            world.tick += 1

        draw(screen, world)
        pg.display.flip()
        clock.tick(20)    # скорость анимации (FPS)

if __name__ == "__main__":
    main()
