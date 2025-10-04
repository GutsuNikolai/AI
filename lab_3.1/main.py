import numpy as np, random, pygame as pg
from config import P
from world import World
from agent import Agent
from sim import step_agents
from viz import init_window, draw_world, draw_agents, draw_hud

def init_agents(n, world):
    agents=[]
    rng = random.Random(P.seed)
    for _ in range(n):
        x = rng.uniform(40, P.win_w*0.35)
        y = rng.uniform(60, P.win_h-60)
        pos = np.array([x,y], dtype=float)
        vel = np.zeros(2, dtype=float)
        agents.append(Agent(pos, vel))
    return agents

def main():
    screen = init_window(P.win_w, P.win_h)
    clock = pg.time.Clock()
    world = World.simple_room(P.win_w, P.win_h)
    agents = init_agents(P.n_agents, world)

    running=True
    while running:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running=False

        agents = step_agents(agents, world)
        draw_world(screen, world)
        draw_agents(screen, agents)
        draw_hud(screen, clock.get_fps(), len(agents))
        pg.display.flip()

        if not agents:
            running=False
        clock.tick(15)

    pg.quit()

if __name__ == "__main__":
    main()
