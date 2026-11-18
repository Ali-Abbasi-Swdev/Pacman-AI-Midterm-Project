# Pacman AI — Search Algorithm Comparison
## Artificial Intelligence Course Midterm Project

## Project overview

This desktop game is an interactive demonstration of AI search algorithms. A
player-controlled Pacman moves through a maze while five ghosts use different
search strategies to plan routes toward Pacman's current position. Their routes
and search statistics are displayed together so their behavior can be observed
during play.

The game is built with Python's standard library and Tkinter. It runs as a
desktop application; publishing the source on GitHub does not make it playable
in a web browser.

## Why I chose this project

I chose Pacman because it makes abstract search algorithms visible. Rather than
comparing them only through theory, I can watch different strategies explore
the same maze and plan toward a moving target. Weighted tiles and portals also
make it possible to show the differences between finding the fewest moves,
minimizing movement cost, and using a heuristic to guide a search.

## Learning objectives

- Compare uninformed, heuristic, and local search strategies in one maze.
- Observe how each searcher expands states and plans toward a changing goal.
- Distinguish the shortest route by number of moves from the least-cost route.
- Understand how a heuristic and portal shortcuts affect A* search.
- Read route length, movement cost, and expanded-node counts in context.

## Implemented algorithms

Each ghost recomputes a route to Pacman's current position when the ghosts
move. The game reports the number of nodes explored for each search.

- **Breadth-First Search (BFS):** explores the maze by move count and finds a
  route with the fewest moves. It does not account for tile costs, so that
  route is not necessarily the minimum-energy route.
- **Greedy Best-First Search:** prioritizes the estimated remaining distance
  (Manhattan distance). It can reach the goal quickly, but does not guarantee
  an optimal route.
- **Branch and Bound:** expands the lowest accumulated-cost candidate first
  and uses the best goal cost found as a bound. In this implementation it
  behaves similarly to Uniform-Cost Search and seeks a minimum-cost route.
- **Hill Climbing:** chooses an immediate neighbor only when it is closer to
  the goal by Manhattan distance. It can stop at a local minimum and does not
  plan a complete route.
- **A\*:** prioritizes `f = g + h`. With the implemented portal-aware relaxed
  heuristic, it seeks a minimum-cost route.

Here, **g** is the accumulated actual tile-entry cost, **h** estimates the
remaining cost, and **f** is their sum.

## Game features

- Control Pacman through a fixed maze with arrow keys.
- Collect small dots and larger bonus dots to increase the score; collect all
  dots to win.
- Watch five differently colored ghosts pursue Pacman and see their planned
  routes overlaid on the maze.
- Toggle route overlays, pause the game, and restart it from the keyboard.
- View each ghost's explored-node count, planned move count, route cost, and
  route status in the tracker.
- Use four paired portals at the maze edges to travel between distant areas.

## Weighted movement costs

Walkable tiles have an entry cost based on their Manhattan distance from the
maze center: cost **1** within distance 6, cost **2** within distance 12, and
cost **3** farther away. Search algorithms that use these values accumulate
the cost of each entered tile along a route. These regional costs represent
planned movement energy, not movement speed; they do not make a ghost move
faster or slower.

BFS minimizes the number of moves rather than this cost. The displayed route
cost is the sum of entry costs for the route after its starting tile.

## Portals and the A* heuristic

The maze has four pairs of edge portals. Pacman uses a portal by moving outward
off the board from a portal tile. The search graph also includes a transition
from each portal tile to its paired destination. A portal transition charges
the actual entry cost of the destination tile.

A* uses a relaxed-board estimate for `h`: it ignores walls and assumes
cost-1 transitions while retaining the portal shortcuts. This is only an
estimate; actual search movement still respects walls and charges the real
tile-entry cost. Because Branch and Bound and A* minimize the same movement
cost objective, they are expected to find routes with the same minimum cost
when given the same start and goal. Exact paths can differ when several
minimum-cost routes exist. A fair algorithm comparison requires identical
start and goal positions; in the live game, ghosts start at different
positions. Hill Climbing's displayed route represents only its immediate
planned step, not a complete route to Pacman.

## Installation and running instructions

1. Install a currently supported Python 3 release from
   [python.org](https://www.python.org/). During Windows setup, include
   Tcl/Tk and IDLE. On Linux, install the
   distribution's Tkinter package if it is not already available (for example,
   `sudo apt install python3-tk` on Debian or Ubuntu).
2. Check that Tkinter is available by running `py -m tkinter` on Windows or
   `python3 -m tkinter` on macOS/Linux. A small Tk window should open.
3. Clone the repository:

   ```sh
   git clone https://github.com/Ali-Abbasi-Swdev/Pacman-AI-Midterm-Project.git
   ```

4. Open the project directory:

   ```sh
   cd Pacman-AI-Midterm-Project
   ```

5. Run the game:

   ```sh
   py main.py
   ```

   On macOS or Linux, use `python3 main.py` if `python` does not refer to
   Python 3.

The game uses only Python's standard library; no third-party packages or
`requirements.txt` are needed.

## Controls

| Key | Action |
| --- | --- |
| Arrow keys | Move Pacman; the first arrow key starts the game |
| Space | Pause or resume after the game has started |
| P | Toggle the planned-route overlays |
| R | Restart the game |

## Project structure

| File | Purpose |
| --- | --- |
| `main.py` | Tkinter window, game loop, controls, Pacman, and ghost updates |
| `board.py` | Maze layout, movement, tile costs, portals, drawing, and statistics |
| `ghost_bfs.py` | Breadth-First Search |
| `ghost_bestfirst.py` | Greedy Best-First Search |
| `ghost_bnb.py` | Branch and Bound search |
| `ghost_hill.py` | Hill Climbing |
| `ghost_Astar.py` | A* search and portal-aware heuristic |

## Algorithm comparison

| Algorithm | Main priority | Minimum moves guaranteed? | Minimum movement cost guaranteed? | Route shown |
| --- | --- | --- | --- | --- |
| BFS | Fewest steps | Yes | No | Complete planned route |
| Greedy Best-First | Estimated distance to goal | No | No | Complete planned route |
| Branch and Bound | Accumulated movement cost | No | Yes | Complete planned route |
| Hill Climbing | Best improving immediate neighbor | No | No | Immediate step only |
| A* | Accumulated cost plus estimated remaining cost (`g + h`) | No | Yes | Complete planned route |

These are properties of the implemented search strategies and cost model, not
timed benchmark results. Compare algorithms from identical start and goal
positions; the live game uses different starting positions for each ghost.

## Limitations

- The game uses one fixed maze and fixed initial positions.
- Ghosts re-plan toward Pacman's current position; this is not a prediction of
  where Pacman will move next.
- Hill Climbing has no backtracking and may remain at a local minimum.
- The displayed node counts and routes depend on the current positions and
  maze state, so they are not controlled benchmark results.
- This is a Tkinter desktop application, not a browser game.
- No license has been selected for the project.

## Future improvements

- Add a way to select the same start and goal for repeatable algorithm
  comparisons.
- Add configurable mazes and tile costs.
- Record repeatable search measurements for controlled comparisons.
- Improve Hill Climbing with a strategy for escaping local minima.
- Add screenshots captured from the running game.
