import numpy as np, random, pygame as pg
from config import P
from world import World
from agent import Agent
from sim import step_agents
from viz import init_window, draw_world, draw_agents

W, H = P.win_w, P.win_h
zones = [
    (int(W * 0.35), int(H * 0), 80, 80),  # слева от круга
    (int(W * 0.5), int(H * 0.5), 80, 80),  # сверху-справа от круга (между кругом и верхней колонной)
    (int(W * 0.65), int(H * 0.85), 80, 80),  # справа-снизу от круга (у правой колонны)
    (int(W * 0), int(H * 0.85), 80, 80),
]

def init_agents(n, world):
    import random, numpy as np
    rng = random.Random(P.seed)
    agents=[]
    for i in range(n):
        x0, y0, w, h = zones[i % len(zones)]
        x = rng.uniform(x0, x0 + w)
        y = rng.uniform(y0, y0 + h)
        pos = np.array([x, y], dtype=float)
        vel = np.zeros(2, dtype=float)
        agents.append(Agent(pos, vel))
    return agents


def main():
    screen = init_window(P.win_w, P.win_h)
    clock = pg.time.Clock()
    world = World.custom_room(P.win_w, P.win_h)
    world.zones = zones# <-- НОВАЯ КОМНАТА
    agents = init_agents(P.n_agents, world)

    sim_time = 0.0
    running=True
    font = pg.font.SysFont("consolas", 16)
    while running:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running=False

        agents = step_agents(agents, world)
        sim_time += P.dt

        draw_world(screen, world)
        draw_agents(screen, agents)
        evacuated = P.n_agents - len(agents)
        hud1 = font.render(f"FPS: {clock.get_fps():5.1f} | agents: {len(agents)}", True, (30,30,30))
        hud2 = font.render(f"t={sim_time:5.2f}s | evacuated: {evacuated}/{P.n_agents}", True, (30,30,30))
        screen.blit(hud1, (8,8))
        screen.blit(hud2, (8,28))
        pg.display.flip()

        if not agents:
            running=False
        clock.tick(15)

    print(f"Total sim time: {sim_time:.2f} s")
    pg.quit()

if __name__ == "__main__":
    main()
