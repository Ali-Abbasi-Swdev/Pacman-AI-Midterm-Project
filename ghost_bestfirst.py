import board


def distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def find_path(start, goal):
    frontier = [(distance(start, goal), start)]
    came_from = {start: None}
    nodes = 0

    while len(frontier) > 0:
        best = min(frontier)
        frontier.remove(best)
        current = best[1]
        nodes = nodes + 1

        if current == goal:
            break

        for n in board.get_neighbors(current[0], current[1]):
            if n not in came_from:
                came_from[n] = current
                frontier.append((distance(n, goal), n))

    path = board.get_path(came_from, goal)
    return path, nodes
