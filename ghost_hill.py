import board


def distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def find_path(start, goal):
    best = start
    best_dist = distance(start, goal)

    neighbors = board.get_neighbors(start[0], start[1])
    for n in neighbors:
        d = distance(n, goal)
        if d < best_dist:
            best = n
            best_dist = d

    nodes = len(neighbors)

    if best == start:
        return [start], nodes
    return [start, best], nodes
