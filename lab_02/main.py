from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Tuple, Optional
import random, time

# ----------------- Модель дерева -----------------
@dataclass
class Node:
    children: List["Node"] = field(default_factory=list)
    value: Optional[int] = None  # только для листьев

    @property
    def is_leaf(self) -> bool:
        return self.value is not None

def make_random_tree(depth: int, branching: int, lo: int = -50, hi: int = 50) -> Node:
    """
    Ровное дерево: заданная глубина и фикс. ветвление (для честного сравнения).
    На глубине 0 — лист с value.
    """
    if depth == 0:
        return Node(value=random.randint(lo, hi))
    return Node(children=[make_random_tree(depth - 1, branching, lo, hi) for _ in range(branching)])

# ----------------- Мини-макс (без отсечения) -----------------
def minimax(node: Node, maximizing: bool, stats: dict) -> int:
    stats["visited"] += 1
    if node.is_leaf:
        return node.value  # type: ignore

    if maximizing:
        best = -10**9
        for child in node.children:
            val = minimax(child, False, stats)
            if val > best:
                best = val
        return best
    else:
        best = 10**9
        for child in node.children:
            val = minimax(child, True, stats)
            if val < best:
                best = val
        return best

# ----------------- Мини-макс с альфа-бета -----------------
def alphabeta(node: Node, alpha: int, beta: int, maximizing: bool, stats: dict) -> int:
    stats["visited"] += 1
    if node.is_leaf:
        return node.value  # type: ignore

    if maximizing:
        v = -10**9
        for i, child in enumerate(node.children):
            v = max(v, alphabeta(child, alpha, beta, False, stats))
            alpha = max(alpha, v)
            # условие отсечения
            if alpha >= beta:
                # оставшиеся дети не просматриваем
                stats["pruned"] += len(node.children) - (i + 1)
                break
        return v
    else:
        v = 10**9
        for i, child in enumerate(node.children):
            v = min(v, alphabeta(child, alpha, beta, True, stats))
            beta = min(beta, v)
            if alpha >= beta:
                stats["pruned"] += len(node.children) - (i + 1)
                break
        return v

# делаю пару листьев равным значением
def make_some_leaves_equal(root, ratio=0.1):
    leaves = []
    def dfs(n):
        if n.is_leaf:
            leaves.append(n); return
        for ch in n.children: dfs(ch)
    dfs(root)
    if len(leaves) < 2:
        return
    target = leaves[0].value
    k = max(2, int(len(leaves) * ratio))
    for n in leaves[1:1+k]:
        n.value = target

def collect_leaf_values(root):
    vals = []
    def dfs(n):
        if n.is_leaf:
            vals.append(n.value)
        else:
            for ch in n.children:
                dfs(ch)
    dfs(root)
    return vals

# ----------------- Демонстрация и сравнение -----------------
if __name__ == "__main__":
    random.seed(42)

    DEPTH = 7
    BRANCH =2
    root = make_random_tree(DEPTH, BRANCH, -99, 99)
    # make_some_leaves_equal(root, ratio=0.1)

    # Чистый minimax
    mm_stats = {"visited": 0}
    t0 = time.perf_counter()
    mm_value = minimax(root, maximizing=True, stats=mm_stats)
    t1 = time.perf_counter()

    # Alpha-beta
    ab_stats = {"visited": 0, "pruned": 0}
    t2 = time.perf_counter()
    ab_value = alphabeta(root, alpha=-10**9, beta=10**9, maximizing=True, stats=ab_stats)
    t3 = time.perf_counter()

    # Вывод
    print("=== Результаты ===")
    print(f"Minimax         : value={mm_value:>4} | visited={mm_stats['visited']:>6} | time={(t1-t0)*1000:7.2f} ms")
    print(f"Alpha-Beta      : value={ab_value:>4} | visited={ab_stats['visited']:>6} | pruned={ab_stats['pruned']:>6} | time={(t3-t2)*1000:7.2f} ms")
    assert mm_value == ab_value, "Значения должны совпадать!"

    vals = collect_leaf_values(root)
    print (vals)
    