from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple
import numpy as np

Vec = np.ndarray

# ---------- Геометрия ----------
@dataclass
class Exit:
    x: int; y: int; w: int; h: int
    def contains(self, p: Vec) -> bool:
        return (self.x <= p[0] <= self.x + self.w) and (self.y <= p[1] <= self.y + self.h)

@dataclass
class RectWall:
    x: int; y: int; w: int; h: int

@dataclass
class CircleWall:
    cx: int; cy: int; r: int    # круглая «стена» (для дуги у двери)

# ---------- Мир ----------
@dataclass
class World:
    width: int; height: int
    exits: List[Exit]
    rects: List[RectWall]
    circles: List[CircleWall]

    # Базовая «пустая» комната (оставляем на всякий случай)
    @staticmethod
    def simple_room(width: int, height: int) -> 'World':
        exit_w, exit_h = 30, 90
        exit_y = height // 2 - exit_h // 2
        exit_x = width - exit_w - 2
        return World(width, height,
                     exits=[Exit(exit_x, exit_y, exit_w, exit_h)],
                     rects=[],
                     circles=[])

    # === НОВАЯ КОМНАТА — «как на твоём рисунке» (условно) ===
    @staticmethod
    def custom_room(width: int, height: int) -> 'World':
        W, H = width, height

        # Два выхода по бокам (чуть "внутри", чтобы можно было войти)
        exit_w, exit_h = 16, 100
        exits = [
            Exit(6, H // 2 - exit_h // 2, exit_w, exit_h),  # левый
            Exit(W - exit_w - 6, H // 2 - exit_h // 2, exit_w, exit_h),  # правый
        ]

        # Три вертикальные колонны (чёрные прямоугольники)
        rects = [
            # левая колонна
            RectWall(int(W * 0.32), int(H * 0), 24, int(H * 0.45)),
            RectWall(int(W * 0.32), int(H * 0.55), 24, int(H * 0.45)),
            # центральная-верхняя колонна
            RectWall(int(W * 0.58), int(H * 0), 24, int(H * 0.45)),
            RectWall(int(W * 0.58), int(H * 0.45), int(H * 0.36), 24),
            # правая-нижняя колонна
            RectWall(int(W * 0.78), int(H * 0.55), 24, int(H * 0.5)),

        ]

        # Большое круглое препятствие по центру
        circles = [
            #CircleWall(W // 2, H // 2, int(min(W, H) * 0.18)),  # радиус ~18% от меньшей стороны
        ]

        return World(W, H, exits=exits, rects=rects, circles=circles)

    # --------- Направление к ближайшему выходу ---------
    def nearest_exit_dir(self, p: Vec) -> Vec:
        centers = [np.array([e.x + e.w/2, e.y + e.h/2], dtype=float) for e in self.exits]
        target = centers[int(np.argmin([np.linalg.norm(c - p) for c in centers]))]
        v = target - p
        n = np.linalg.norm(v)
        return v / n if n > 1e-6 else np.zeros(2)

    def in_exit(self, p: Vec) -> bool:
        return any(e.contains(p) for e in self.exits)

    # --------- Отталкивание от наружных границ комнаты ---------
    def boundary_repulsion_dir(self, p: np.ndarray, d0: float) -> np.ndarray:
        fx = 0.0;
        fy = 0.0

        # --- прозрачно в вертикальном диапазоне дверей ---
        left_open = False
        right_open = False
        right_limit = self.width - 6.0

        for ex in self.exits:
            in_span = (ex.y - 2 <= p[1] <= ex.y + ex.h + 2)
            if not in_span:
                continue
            # дверь на левой стене?
            if ex.x <= 8:
                left_open = True
            # дверь на правой стене?
            if ex.x + ex.w >= self.width - 8:
                right_open = True
                # для клампа дальше используем край двери
                right_limit = max(right_limit, ex.x + ex.w)

        # расстояния до рамки с учётом «прозрачных» зон
        dl = (p[0] - 6.0) if not left_open else 1e9
        dr = (right_limit - p[0]) if not right_open else 1e9
        dt = p[1] - 6.0
        db = (self.height - 6.0) - p[1]

        if dl < d0: fx += 1.0 / max(dl, 1.0)
        if dr < d0: fx -= 1.0 / max(dr, 1.0)
        if dt < d0: fy += 1.0 / max(dt, 1.0)
        if db < d0: fy -= 1.0 / max(db, 1.0)

        v = np.array([fx, fy], dtype=float)
        n = np.linalg.norm(v)
        return v / n if n > 1e-9 else np.zeros(2)

    # --------- Отталкивание от внутренних препятствий ---------
    def rects_repulsion_dir(self, p: Vec, d0: float) -> Vec:
        fx = 0.0; fy = 0.0
        for r in self.rects:
            # ближайшая точка прямоугольника к p
            cx = np.clip(p[0], r.x, r.x + r.w)
            cy = np.clip(p[1], r.y, r.y + r.h)
            d = np.array([p[0]-cx, p[1]-cy], dtype=float)
            dist = np.linalg.norm(d)
            if dist < d0:
                if dist < 1e-6: d = np.array([1.0, 0.0])  # защита
                d_unit = d / max(dist, 1.0)
                k = 1.0 / max(dist, 1.0)
                fx += d_unit[0]*k; fy += d_unit[1]*k
        v = np.array([fx, fy], dtype=float)
        n = np.linalg.norm(v)
        return v / n if n > 1e-9 else np.zeros(2)

    def circles_repulsion_dir(self, p: Vec, d0: float) -> Vec:
        fx = 0.0; fy = 0.0
        for c in self.circles:
            d = np.array([p[0]-c.cx, p[1]-c.cy], dtype=float)
            dist = np.linalg.norm(d)
            # расстояние до окружности (если внутри — отрицательное)
            gap = abs(dist - c.r)
            if gap < d0:
                if dist < 1e-6: d = np.array([1.0, 0.0])
                d_unit = d / max(dist, 1.0)
                # если внутри круга — толкать наружу, если снаружи близко — тоже отталкивать
                sgn = 1.0 if dist < c.r else 1.0
                k = sgn / max(gap, 1.0)
                fx += d_unit[0]*k; fy += d_unit[1]*k
        v = np.array([fx, fy], dtype=float)
        n = np.linalg.norm(v)
        return v / n if n > 1e-9 else np.zeros(2)

    def walls_repulsion(self, p: Vec, d0: float, w_boundary: float = 1.0, w_rects: float = 1.0, w_circles: float = 1.0) -> Vec:
        v = (self.boundary_repulsion_dir(p, d0) * w_boundary
             + self.rects_repulsion_dir(p, d0) * w_rects
             + self.circles_repulsion_dir(p, d0) * w_circles)
        n = np.linalg.norm(v)
        return v / n if n > 1e-9 else np.zeros(2)

    # --------- Простое «скольжение» по внешней рамке комнаты ---------
    def clamp_and_slide(self, p: Vec, v: Vec) -> Tuple[Vec, Vec]:
        # только внешняя рамка; внутренние стены мы «держим» силой отталкивания
        x, y = float(p[0]), float(p[1])
        vx, vy = float(v[0]), float(v[1])
        hit_x = hit_y = False

        right_limit = self.width - 6.0
        # вход на правой границе возможен в зоне выхода
        for ex in self.exits:
            if ex.y - 2 <= y <= ex.y + ex.h + 2:
                right_limit = max(right_limit, ex.x + ex.w)

        if x < 6.0: x = 6.0; hit_x = True
        elif x > right_limit: x = right_limit; hit_x = True

        if y < 6.0: y = 6.0; hit_y = True
        elif y > self.height - 6.0: y = self.height - 6.0; hit_y = True

        if hit_x: vx = 0.0
        if hit_y: vy = 0.0
        return np.array([x, y], dtype=float), np.array([vx, vy], dtype=float)

    def resolve_rects_collision(self, p_new: np.ndarray, v: np.ndarray):
        """
        Если точка p_new оказалась ВНУТРИ какого-то прямоугольника,
        выталкиваем её по минимальному перекрытию и гасим скорость по нормали.
        Возвращает (p, v) после коррекции.
        """
        x, y = float(p_new[0]), float(p_new[1])
        vx, vy = float(v[0]), float(v[1])
        pushed = False

        for r in self.rects:
            inside = (r.x <= x <= r.x + r.w) and (r.y <= y <= r.y + r.h)
            if not inside:
                continue

            # сколько "зашли" внутрь каждой стороны
            left = x - r.x
            right = (r.x + r.w) - x
            top = y - r.y
            bottom = (r.y + r.h) - y

            m = min(left, right, top, bottom)
            eps = 0.1  # маленький зазор, чтобы не залипать на ребре

            if m == left:
                x = r.x - eps;
                vx = 0.0
            elif m == right:
                x = r.x + r.w + eps;
                vx = 0.0
            elif m == top:
                y = r.y - eps;
                vy = 0.0
            else:  # bottom
                y = r.y + r.h + eps;
                vy = 0.0

            pushed = True

        if pushed:
            return np.array([x, y], dtype=float), np.array([vx, vy], dtype=float)
        else:
            return p_new, v