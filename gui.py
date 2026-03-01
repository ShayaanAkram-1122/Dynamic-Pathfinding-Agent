"""
GUI module: Pygame visualization for the pathfinding grid.
- Draws grid, start (green), goal (red), walls, frontier (yellow), visited (red/blue), path (green).
- Interactive editor: click to add/remove walls.
- Algorithm & heuristic selection, metrics dashboard.
"""

import pygame
import sys
from typing import Dict, List, Optional, Set, Tuple

from agent import Agent
from grid import Grid
from node import Node


# Colors (RGB)
COLOR_BG = (30, 30, 40)
COLOR_GRID = (60, 60, 70)
COLOR_START = (50, 205, 50)   # green
COLOR_GOAL = (220, 50, 50)    # red
COLOR_WALL = (50, 50, 60)
COLOR_FRONTIER = (255, 255, 0)   # yellow
COLOR_VISITED = (255, 100, 100)  # light red
COLOR_PATH = (0, 200, 100)       # green path
COLOR_AGENT = (0, 255, 200)      # cyan
COLOR_TEXT = (240, 240, 240)


class PathfindingGUI:
    """Pygame window for grid visualization and controls."""

    def __init__(
        self,
        rows: int = 15,
        cols: int = 20,
        cell_size: int = 32,
        obstacle_density: float = 0.25,
    ):
        pygame.init()
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.obstacle_density = obstacle_density
        self.grid = Grid(rows, cols)
        self.agent = Agent(self.grid)
        # UI area: reserve top for controls/metrics
        self.dashboard_height = 80
        self.width = cols * cell_size
        self.height = rows * cell_size + self.dashboard_height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Dynamic Pathfinding Agent")
        self.clock = pygame.time.Clock()
        # State
        self.editing = True
        self.algorithm = "astar"
        self.heuristic = "manhattan"
        self.path: List[Node] = []
        self.frontier_set: Set[Tuple[int, int]] = set()
        self.visited_set: Set[Tuple[int, int]] = set()
        self.dynamic_mode = False
        self.font = pygame.font.Font(None, 24)

    def _cell_rect(self, row: int, col: int) -> pygame.Rect:
        """Screen rect for cell (row, col); grid starts below dashboard."""
        x = col * self.cell_size
        y = self.dashboard_height + row * self.cell_size
        return pygame.Rect(x, y, self.cell_size, self.cell_size)

    def _cell_at_pos(self, px: int, py: int) -> Optional[Tuple[int, int]]:
        """Return (row, col) for pixel (px, py) or None."""
        if py < self.dashboard_height:
            return None
        row = (py - self.dashboard_height) // self.cell_size
        col = px // self.cell_size
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return (row, col)
        return None

    def _draw_cell(self, row: int, col: int, color: Tuple[int, int, int]) -> None:
        r = self._cell_rect(row, col)
        pygame.draw.rect(self.screen, color, r)
        pygame.draw.rect(self.screen, COLOR_GRID, r, 1)

    def _draw_grid(self) -> None:
        for r in range(self.rows):
            for c in range(self.cols):
                node = self.grid.get_node(r, c)
                if not node.walkable:
                    self._draw_cell(r, c, COLOR_WALL)
                elif (r, c) in self.visited_set:
                    self._draw_cell(r, c, COLOR_VISITED)
                elif (r, c) in self.frontier_set:
                    self._draw_cell(r, c, COLOR_FRONTIER)
                else:
                    self._draw_cell(r, c, COLOR_BG)
        # Path on top
        path_set = {n.position() for n in self.path}
        for r in range(self.rows):
            for c in range(self.cols):
                if (r, c) in path_set:
                    self._draw_cell(r, c, COLOR_PATH)
        # Start and goal
        sr, sc = self.grid.get_start()
        gr, gc = self.grid.get_goal()
        self._draw_cell(sr, sc, COLOR_START)
        self._draw_cell(gr, gc, COLOR_GOAL)
        # Agent
        ar, ac = self.agent.current_position
        self._draw_cell(ar, ac, COLOR_AGENT)

    def _draw_dashboard(self) -> None:
        """Draw metrics and mode at top of screen."""
        surf = pygame.Surface((self.width, self.dashboard_height))
        surf.fill((40, 40, 50))
        self.screen.blit(surf, (0, 0))
        m = self.agent.get_metrics()
        lines = [
            f"Nodes visited: {m['nodes_visited']}  Path cost: {m['path_cost']:.1f}  Time: {m['execution_time_ms']:.1f} ms",
            f"Algo: {self.algorithm}  Heuristic: {self.heuristic}  Edit: {'ON' if self.editing else 'OFF'}  Dynamic: {'ON' if self.dynamic_mode else 'OFF'}",
        ]
        y = 8
        for line in lines:
            text = self.font.render(line, True, COLOR_TEXT)
            self.screen.blit(text, (8, y))
            y += 28

    def _run_search_animation(self) -> None:
        """Run search step-by-step and redraw (stub: run sync and show result)."""
        self.grid.reset_costs()
        self.frontier_set = set()
        self.visited_set = set()
        self.path = []
        self.agent.plan(self.algorithm, self.heuristic)
        for n in self.agent.get_frontier_nodes():
            self.frontier_set.add(n.position())
        for n in self.agent.get_visited_nodes():
            self.visited_set.add(n.position())
        self.path = self.agent.get_path()

    def run(self) -> None:
        """Main loop: handle events and redraw."""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    cell = self._cell_at_pos(*event.pos)
                    if cell and self.editing:
                        self.grid.toggle_wall(cell[0], cell[1])
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_e:
                        self.editing = not self.editing
                    elif event.key == pygame.K_g:
                        self.grid.generate_random_maze(self.obstacle_density)
                        self.agent = Agent(self.grid)
                        self.path = []
                        self.frontier_set = set()
                        self.visited_set = set()
                    elif event.key == pygame.K_SPACE:
                        self.editing = False
                        self._run_search_animation()
                    elif event.key == pygame.K_1:
                        self.algorithm = "greedy"
                    elif event.key == pygame.K_2:
                        self.algorithm = "astar"
                    elif event.key == pygame.K_h:
                        self.heuristic = "euclidean" if self.heuristic == "manhattan" else "manhattan"

            self.screen.fill(COLOR_BG)
            self._draw_grid()
            self._draw_dashboard()
            pygame.display.flip()
            self.clock.tick(30)
        pygame.quit()
        sys.exit(0)


def main() -> None:
    gui = PathfindingGUI(rows=15, cols=20, obstacle_density=0.25)
    gui.run()


if __name__ == "__main__":
    main()
