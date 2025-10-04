import numpy as np, random, pygame as pg
from config import P
from world import World
from agent import Agent
from sim import step_agents
from viz import init_window, draw_world, draw_agents

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
        clock.tick(60)

    print(f"Total sim time: {sim_time:.2f} s")
    pg.quit()

if __name__ == "__main__":
    main()
