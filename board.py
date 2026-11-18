import tkinter as tk


CELL = 30
layout = [
    "######T###########T######",
    "#o......#.......#......o#",
    "#.####..#.#####.#.###.#.#",
    "#.............#.......#.#",
    "###..#.#####.#####.##...#",
    "#....#.....#............#",
    "#.######.#.###.#.#####..#",
    "T......#.#.....#........T",
    "#.####.#.#####.###.###..#",
    "#.#....#.......#...#....#",
    "#.#.####.......#.#....###",
    "#........## ##.....#....#",
    "#.##.###..H H..#.###.#..#",
    "#....#...# H #.#.....#..#",
    "#..###.#..H H..###.#.#..#",
    "#......#.## ##.....#....#",
    "#..#####.......###.###..#",
    "T......#.##.##.#........T",
    "#.####.#.....#.#.###.#..#",
    "#......###.#.#...#...#..#",
    "#..###.....#.#####.###..#",
    "#....#.#####.....#......#",
    "#.#..#.......###.#####..#",
    "#o#.......#............o#",
    "######T###########T######",
]

PORTAL_PAIRS = (
    (((0, 6), (24, 6))),
    (((0, 18), (24, 18))),
    (((7, 0), (7, 24))),
    (((17, 0), (17, 24))),
)

maze = []
score = 0

def get_portal_destination(row, col):
    position = (row, col)
    for pair in PORTAL_PAIRS:
        if position == pair[0]:
            return pair[1]
        if position == pair[1]:
            return pair[0]
    return None


def reset_maze():
    global maze, score
    maze = []
    for line in layout:
        maze.append(list(line))
    score = 0


def get_tile_cost(row, col):
    center_row = len(maze) // 2
    center_col = len(maze[0]) // 2
    distance = abs(row - center_row) + abs(col - center_col)

    if distance <= 6:
        return 1
    if distance <= 12:
        return 2
    return 3


def get_path_cost(path):
    total = 0
    for row, col in path[1:]:
        total = total + get_tile_cost(row, col)
    return total


def is_wall(row, col):
    if row < 0 or row >= len(maze) or col < 0 or col >= len(maze[0]):
        return True
    if maze[row][col] == "#":
        return True
    return False


def get_neighbors(row, col):
    result = []
    if not is_wall(row - 1, col):
        result.append((row - 1, col))
    if not is_wall(row + 1, col):
        result.append((row + 1, col))
    if not is_wall(row, col - 1):
        result.append((row, col - 1))
    if not is_wall(row, col + 1):
        result.append((row, col + 1))
    destination = get_portal_destination(row, col)
    if destination is not None:
        result.append(destination)
    return result


def get_move_destination(row, col, row_delta, col_delta):
    new_row = row + row_delta
    new_col = col + col_delta

    if new_row < 0 or new_row >= len(maze) or new_col < 0 or new_col >= len(maze[0]):
        return get_portal_destination(row, col)
    
    if not is_wall(new_row, new_col):
        return (new_row, new_col)
    return None


def get_path(came_from, goal):
    if goal not in came_from:
        return []
    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path


def eat_dot(row, col):
    global score
    if maze[row][col] == ".":
        maze[row][col] = " "
        score = score + 10
    elif maze[row][col] == "o":
        maze[row][col] = " "
        score = score + 50


def count_dots():
    total = 0
    for row in maze:
        for cell in row:
            if cell == "." or cell == "o":
                total = total + 1
    return total


def make_canvas(root):
    width = len(layout[0]) * CELL
    height = len(layout) * CELL
    canvas = tk.Canvas(
        root, width=width, height=height, bg="#05050d",
        highlightthickness=2, highlightbackground="#263cff"
    )
    canvas.pack(side="left")
    return canvas


def make_label(root):
    label = tk.Label(
        root, text="", font=("Courier New", 12), justify="left",
        anchor="nw", bg="#101020", fg="#f4f0d0", padx=12, pady=12
    )
    label.pack()
    return label


def draw_maze(canvas):
    canvas.delete("all")
    width = len(maze[0]) * CELL
    height = len(maze) * CELL

    for r in range(len(maze)):
        for c in range(len(maze[0])):
            if maze[r][c] != "#":
                x = c * CELL
                y = r * CELL
                canvas.create_rectangle(
                    x, y, x + CELL, y + CELL,
                    fill="#000000", outline=""
                )
    canvas.create_rectangle(
        4, 4, width - 4, height - 4,
        fill="", outline="#2339f4", width=2
    )

    for r in range(len(maze)):
        for c in range(len(maze[0])):
            x = c * CELL
            y = r * CELL
            if maze[r][c] == "#":
                if r == 0 or maze[r - 1][c] != "#":
                    canvas.create_line(x, y, x + CELL, y, fill="#263cff", width=2)
                if r == len(maze) - 1 or maze[r + 1][c] != "#":
                    canvas.create_line(x, y + CELL, x + CELL, y + CELL, fill="#263cff", width=2)
                if c == 0 or maze[r][c - 1] != "#":
                    canvas.create_line(x, y, x, y + CELL, fill="#263cff", width=2)
                if c == len(maze[0]) - 1 or maze[r][c + 1] != "#":
                    canvas.create_line(x + CELL, y, x + CELL, y + CELL, fill="#263cff", width=2)
            elif maze[r][c] == ".":
                canvas.create_rectangle(
                    x + CELL // 2 - 2, y + CELL // 2 - 2,
                    x + CELL // 2 + 2, y + CELL // 2 + 2,
                    fill="#f3aabb", outline=""
                )
            elif maze[r][c] == "o":
                size = CELL // 2
                canvas.create_oval(
                    x + CELL // 2 - size // 2, y + CELL // 2 - size // 2,
                    x + CELL // 2 + size // 2, y + CELL // 2 + size // 2,
                    fill="#f3aabb", outline=""
                )

    portal_colors = ("#56e0f0", "#c884ff", "#f0b34c", "#74e0a1")
    for i in range(len(PORTAL_PAIRS)):
        color = portal_colors[i]
        for row, col in PORTAL_PAIRS[i]:
            x = col * CELL
            y = row * CELL
            canvas.create_oval(
                x + 5, y + 5, x + CELL - 5, y + CELL - 5,
                outline=color, width=2
            )


def draw_pacman(canvas, row, col, direction=(0, 1)):
    x = col * CELL
    y = row * CELL
    if direction == (-1, 0):
        angle = 90
    elif direction == (1, 0):
        angle = 270
    elif direction == (0, -1):
        angle = 180
    else:
        angle = 0
    margin = CELL // 6
    canvas.create_arc(
        x + margin, y + margin, x + CELL - margin, y + CELL - margin,
        start=angle + 30, extent=300, style=tk.PIESLICE,
        fill="#ffe500", outline=""
    )


def draw_ghost(canvas, ghost):
    x = ghost["col"] * CELL
    y = ghost["row"] * CELL
    sprite = [
        "0001111000",
        "0011111100",
        "0111111110",
        "1111111111",
        "1111111111",
        "1111111111",
        "1111111111",
        "1111111111",
        "1111111111",
        "1100110011",
    ]
    pixel = max(2, CELL // 10)
    left = x + (CELL - len(sprite[0]) * pixel) // 2
    top = y + (CELL - len(sprite) * pixel) // 2

    for r in range(len(sprite)):
        for c in range(len(sprite[r])):
            if sprite[r][c] == "1":
                px = left + c * pixel
                py = top + r * pixel
                canvas.create_rectangle(
                    px, py, px + pixel, py + pixel,
                    fill=ghost["color"], outline=ghost["color"]
                )

    for eye_col in (2, 6):
        eye_x = left + eye_col * pixel
        eye_y = top + 4 * pixel
        canvas.create_rectangle(
            eye_x, eye_y - pixel, eye_x + 2 * pixel, eye_y + 2 * pixel,
            fill="white", outline="white"
        )
        pupil_x = eye_x + pixel
        canvas.create_rectangle(
            pupil_x, eye_y, pupil_x + pixel, eye_y + 2 * pixel,
            fill="#2848e8", outline="#2848e8"
        )


def draw_path(canvas, ghost):
    for cell in ghost["path"][1:]:
        x = cell[1] * CELL
        y = cell[0] * CELL
        canvas.create_oval(
            x + CELL // 2 - 5, y + CELL // 2 - 5,
            x + CELL // 2 + 5, y + CELL // 2 + 5,
            outline=ghost["color"], width=2
        )


def draw_message(canvas, text):
    x = len(layout[0]) * CELL // 2
    y = CELL * 10 if text == "READY!" else len(layout) * CELL // 2
    color = "#ffe500" if "WIN" in text or text in ("READY!", "PAUSED") else "#ff5364"
    canvas.create_rectangle(
        x - 86, y - 20, x + 86, y + 20,
        fill="#030309", outline=""
    )
    canvas.create_text(
        x, y, text=text, fill=color,
        font=("Courier New", 15, "bold")
    )


def show_stats(label, ghosts):
    text = "GHOST      NODES  MOVES  COST\n"
    text = text + "----------------------------\n"
    for g in ghosts:
        steps = max(0, len(g["path"]) - 1)
        name = g["name"][:9]
        cost = "--" if not g["path"] else str(get_path_cost(g["path"]))
        text = text + name.ljust(10) + str(g["nodes"]).rjust(5)
        text = text + str(steps).rjust(7) + cost.rjust(6)
        if g.get("route_status"):
            text = text + "\n  " + g["route_status"]
        elif g["stuck"]:
            text = text + "\n  STUCK"
        text = text + "\n"
    label.config(text=text)
