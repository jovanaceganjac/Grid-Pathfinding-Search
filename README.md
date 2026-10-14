# Grid Pathfinding Search

Visualised pathfinding on a weighted tile grid, comparing uninformed and
informed search. Built for the *Intelligent Systems* course at ETF Belgrade.

## Agents

| Agent | Algorithm |
|---|---|
| `DFS` | depth-first search |
| `BranchAndBound` | branch and bound (uniform-cost search) |
| `AStar` | A* with a Manhattan distance heuristic |
| `Example` | baseline provided with the assignment |

## Run

```bash
pip install pygame
python main.py maps/map0.txt AStar
```

## Tech

Python 3, Pygame
