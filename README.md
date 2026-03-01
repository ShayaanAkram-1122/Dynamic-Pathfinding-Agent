# Dynamic Pathfinding Agent

A Python GUI application for grid-based pathfinding with multiple search algorithms and dynamic obstacle spawning.

## Features (planned)

- Grid-based environment (user-defined rows & columns)
- Fixed Start and Goal nodes
- Random maze generation with adjustable obstacle density
- Interactive map editor (click to add/remove walls)
- **Algorithms:** Greedy Best-First Search, A* Search
- **Heuristics:** Manhattan, Euclidean
- **Dynamic mode:** Spawn obstacles while agent moves; re-plan when path is blocked
- **Visualization:** Frontier (yellow), Visited (red/blue), Path (green)
- **Metrics:** Nodes visited, path cost, execution time (ms)

## Structure

- `node.py` — Node class for grid cells
- `grid.py` — Grid environment
- `search.py` — Search algorithms (Greedy BFS, A*)
- `agent.py` — Agent logic and dynamic re-planning
- `gui.py` — Pygame visualization
- `main.py` — Entry point

## Setup

```bash
pip install -r requirements.txt
python main.py
```

## Suggested commit order (for incremental history)

1. **Project setup** — `requirements.txt`, `README.md`, `.gitignore`
2. **Node module** — `node.py`
3. **Grid module** — `grid.py`
4. **Search algorithms** — `search.py` (Greedy BFS, A*, heuristics)
5. **Agent module** — `agent.py`
6. **GUI and main** — `gui.py`, `main.py`
7. **Real-time search animation** — animate frontier/visited step-by-step in GUI
8. **Metrics dashboard** — polish and layout
9. **Dynamic mode** — spawn obstacles during movement, re-plan when blocked
10. **Algorithm/heuristic selector** — dropdowns or buttons in GUI
