import board
def find_path(start, goal):
    frontier = [(0, start)]
    cost_so_far = {start: 0}
    came_from = {start: None}
    best_cost = float("inf")
    nodes = 0
    while len(frontier) > 0:
        item = min(frontier)
        frontier.remove(item)
        cost = item[0]
        current = item[1]
        nodes = nodes + 1

        if cost >= best_cost:
            break

        if current == goal:
            best_cost = cost
            continue

        for n in board.get_neighbors(current[0], current[1]):
            new_cost = cost + board.get_tile_cost(n[0], n[1])
            if new_cost < best_cost:
                if n not in cost_so_far or new_cost < cost_so_far[n]:
                    cost_so_far[n] = new_cost
                    came_from[n] = current
                    frontier.append((new_cost, n))

    path = board.get_path(came_from, goal)
    return path, nodes
