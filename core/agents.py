from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Callable
import heapq

from core.grid import Grid
from core.path import Path


@dataclass(slots=True)
class Agent:
    name: str

    def find_path(self, grid: Grid, start: tuple[int, int], goal: tuple[int, int]) -> Path:
        raise NotImplementedError


class ExampleAgent(Agent):

    def __init__(self):
        super().__init__("Example")

    def find_path(self, grid: Grid, start: tuple[int, int], goal: tuple[int, int]) -> Path:
        nodes = [start]
        while nodes[-1] != goal:
            r, c = nodes[-1]
            neighbors = grid.neighbors4(r, c)

            min_dist = min(grid.manhattan(t.pos, goal) for t in neighbors)
            best_tiles = [
                tile for tile in neighbors
                if grid.manhattan(tile.pos, goal) == min_dist
            ]
            best_tile = best_tiles[random.randint(0, len(best_tiles) - 1)]

            nodes.append(best_tile.pos)

        return Path(nodes)


class DFSAgent(Agent):

    def __init__(self):
        super().__init__("DFS")

    def find_path(self, grid: Grid, start: tuple[int, int], goal: tuple[int, int]) -> Path:
        stack = [start]
        visited = set()
        parent = {start: None}
        path = []

        while stack:
            current = stack.pop()
            if current in visited:
                continue
            visited.add(current)

            if current == goal:
                break

            r, c = current
            neighbors = grid.neighbors4(r, c)
            neighbors.sort(
                key=lambda t: (
                    t.cost,
                    [(0, 1), (1, 0), (0, -1), (-1, 0)].index((t.pos[0] - r, t.pos[1] - c))
                ),
                reverse=True
            )

            for tile in neighbors:
                if tile.pos not in visited:
                    parent[tile.pos] = current
                    stack.append(tile.pos)

        if goal not in parent:
            return Path([])

        node = goal
        while node is not None:
            path.append(node)
            node = parent[node]

        path.reverse()
        return Path(path)


class BranchAndBoundAgent(Agent):

    def __init__(self):
        super().__init__("BranchAndBound")

    def find_path(self, grid: Grid, start: tuple[int, int], goal: tuple[int, int]) -> Path:
        frontier = []
        heapq.heappush(frontier, (0, 1, [start]))
        best_cost = {}

        while frontier:
            cost, _, path = heapq.heappop(frontier)
            current = path[-1]

            if current == goal:
                return Path(path)

            if current in best_cost and best_cost[current] <= cost:
                continue
            best_cost[current] = cost

            r, c = current
            neighbors = grid.neighbors4(r, c)
            for tile in neighbors:
                new_cost = cost + tile.cost
                new_path = path + [tile.pos]
                heapq.heappush(
                    frontier,
                    (new_cost, len(new_path), new_path)
                )

        return Path([])


class AStar(Agent):

    def __init__(self):
        super().__init__("AStar")

    def find_path(self, grid: Grid, start: tuple[int, int], goal: tuple[int, int]) -> Path:
        frontier = []
        heapq.heappush(
            frontier,
            (grid.manhattan(start, goal), 0, 1, [start])
        )

        lowest_cost_to_node = {}

        while frontier:
            f, g, _, path = heapq.heappop(frontier)
            current = path[-1]

            if current == goal:
                return Path(path)

            if current in lowest_cost_to_node and lowest_cost_to_node[current] <= g:
                continue
            lowest_cost_to_node[current] = g

            r, c = current
            neighbors = grid.neighbors4(r, c)
            for tile in neighbors:
                ng = g + tile.cost
                nf = ng + grid.manhattan(tile.pos, goal)
                new_path = path + [tile.pos]
                heapq.heappush(
                    frontier,
                    (nf, ng, len(new_path), new_path)
                )

        return Path([])

AGENTS: dict[str, Callable[[], Agent]] = {
    "Example": ExampleAgent,
    "DFS": DFSAgent,
    "BranchAndBound": BranchAndBoundAgent,
    "AStar": AStar
}


def create_agent(name: str) -> Agent:
    if name not in AGENTS:
        raise ValueError(f"Unknown agent '{name}'. Available: {', '.join(AGENTS.keys())}")
    return AGENTS[name]()