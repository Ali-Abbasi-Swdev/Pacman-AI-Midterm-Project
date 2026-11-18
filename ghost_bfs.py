import board


def find_path(start, goal):
    queue = [start]
    came_from = {start: None}
    nodes = 0

    while len(queue) > 0:
        current = queue.pop(0)
        nodes = nodes + 1

        if current == goal:
            break

        for n in board.get_neighbors(current[0], current[1]):
            if n not in came_from:
                came_from[n] = current
                queue.append(n)

    path = board.get_path(came_from, goal)
    return path, nodes
