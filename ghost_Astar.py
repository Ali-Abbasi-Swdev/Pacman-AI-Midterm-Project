import board


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def get_portal_estimates(goal):

    estimates = {}
    for pair in board.PORTAL_PAIRS:
        for position in pair:
            estimates[position] = manhattan(position, goal)

    waiting = list(estimates)
    while len(waiting) > 0:
        current = min(waiting, key=lambda p: estimates[p])
        waiting.remove(current)

        for position in waiting:
            step_cost = manhattan(position, current)
            if board.get_portal_destination(position[0], position[1]) == current:
                step_cost = min(step_cost, 1)
            candidate = step_cost + estimates[current]
            if candidate < estimates[position]:
                estimates[position] = candidate
    return estimates


def distance(position, goal, portal_estimates):
    estimate = manhattan(position, goal)
    for portal in portal_estimates:
        candidate = manhattan(position, portal) + portal_estimates[portal]
        if candidate < estimate:
            estimate = candidate
    return estimate


def find_path(start, goal):
    portal_estimates = get_portal_estimates(goal)
    frontier = [(distance(start, goal, portal_estimates), 0, start)]
    cost_so_far = {start: 0}
    came_from = {start: None}
    nodes = 0

    while len(frontier) > 0:
        item = min(frontier)
        frontier.remove(item)
        cost = item[1]
        current = item[2]

        if cost != cost_so_far[current]:
            continue
        nodes = nodes + 1

        if current == goal:
            break

        for n in board.get_neighbors(current[0], current[1]):
            new_cost = cost + board.get_tile_cost(n[0], n[1])
            if n not in cost_so_far or new_cost < cost_so_far[n]:
                cost_so_far[n] = new_cost
                came_from[n] = current
                f = new_cost + distance(n, goal, portal_estimates)
                frontier.append((f, new_cost, n))

    path = board.get_path(came_from, goal)
    return path, nodes
