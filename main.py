import tkinter as tk
import board
import ghost_bfs
import ghost_bestfirst
import ghost_bnb
import ghost_hill
import ghost_Astar

TICK = 200
GHOST_SLOW = 2

START_ROW = 23
START_COL = 12

root = tk.Tk()
root.title("PAC-MAN | Search Ghosts")
root.configure(bg="#080812")
root.resizable(True, True)
cell_by_height = (root.winfo_screenheight() - 100) // len(board.layout)
cell_by_width = (root.winfo_screenwidth() - 450) // len(board.layout[0])
board.CELL = max(16, min(board.CELL, cell_by_height, cell_by_width))
root.state("zoomed")

main_layout = tk.Frame(root, bg="#080812")
main_layout.pack(fill="both", expand=True)

info_panel = tk.Frame(main_layout, bg="#101020", width=410, padx=14, pady=12)
info_panel.pack(side="left", fill="y")
info_panel.pack_propagate(False)

title_area = tk.Frame(info_panel, bg="#101020")
title_area.pack(anchor="w", pady=(0, 12))
tk.Label(
    title_area, text="PAC-MAN", font=("Courier New", 28, "bold"),
    bg="#101020", fg="#ffe500"
).pack(anchor="w")
tk.Label(
    title_area, text="SEARCH GHOSTS", font=("Courier New", 12, "bold"),
    bg="#101020", fg="#ff5364"
).pack(anchor="w")

score_area = tk.Frame(info_panel, bg="#101020")
score_area.pack(fill="x", pady=(0, 12))

score_box = tk.Frame(score_area, bg="#080812", padx=12, pady=6)
score_box.pack(fill="x", pady=(0, 6))
tk.Label(
    score_box, text="SCORE", font=("Courier New", 12, "bold"),
    bg="#080812", fg="#9c9cb5"
).pack(anchor="w")
score_display = tk.Label(
    score_box, text="000000", font=("Courier New", 22, "bold"),
    bg="#080812", fg="#ffe500", width=7, anchor="w"
)
score_display.pack(anchor="w")

dots_box = tk.Frame(score_area, bg="#080812", padx=12, pady=6)
dots_box.pack(fill="x")
tk.Label(
    dots_box, text="DOTS LEFT", font=("Courier New", 12, "bold"),
    bg="#080812", fg="#9c9cb5"
).pack(anchor="w")
dots_display = tk.Label(
    dots_box, text="000", font=("Courier New", 22, "bold"),
    bg="#080812", fg="#fff2bd", width=4, anchor="w"
)
dots_display.pack(anchor="w")

algorithm_key = tk.Frame(info_panel, bg="#101020")
algorithm_key.pack(fill="x", pady=(0, 10))
for color_name, color, algorithm in (
    ("RED", "#f52b35", "BFS"),
    ("PINK", "#f0a2e8", "Best-First"),
    ("BLUE", "#1bcddd", "Branch & Bound"),
    ("ORANGE", "#ffb82e", "Hill Climbing"),
    ("GREEN", "#4cff70", "A*"),
):
    tk.Label(
        algorithm_key, text=color_name + ": " + algorithm,
        font=("Courier New", 12, "bold"), bg="#101020", fg=color,
        anchor="w"
    ).pack(anchor="w", pady=2)

game_area = tk.Frame(main_layout, bg="#080812", padx=24, pady=8)
game_area.pack(side="left", anchor="n", fill="both", expand=True)
canvas = board.make_canvas(game_area)
canvas.pack_configure(side="top", anchor="center", expand=True)
side_panel = tk.Frame(info_panel, bg="#101020", padx=0, pady=8)
sidebar_visible = True

def toggle_sidebar():
    global sidebar_visible

    if sidebar_visible:
        side_panel.pack_forget()
        sidebar_visible = False
        sidebar_toggle_button.config(text="SHOW GHOST DATA")
    else:
        side_panel.pack(fill="x")
        sidebar_visible = True
        sidebar_toggle_button.config(text="HIDE GHOST DATA")


sidebar_toggle_button = tk.Button(
    info_panel, text="HIDE GHOST DATA", command=toggle_sidebar,
    font=("Courier New", 12, "bold"), bg="#080812", fg="#ffe500",
    activebackground="#252545", activeforeground="#ffffff",
    relief="flat", padx=10, pady=7
)
sidebar_toggle_button.pack(fill="x")

tk.Label(
    side_panel, text="GHOST TRACKER", font=("Courier New", 14, "bold"),
    bg="#101020", fg="#ffe500"
).pack(anchor="w")
tk.Frame(side_panel, bg="#34345c", height=2).pack(fill="x", pady=(8, 12))

label = board.make_label(side_panel)
label.pack(fill="x")
side_panel.pack(fill="x")

footer = tk.Frame(info_panel, bg="#101020", padx=0, pady=0)
footer.pack(side="bottom", fill="x", pady=(12, 0))
tk.Label(
    footer, text="ARROWS  MOVE\nSPACE  PAUSE\nP  PATHS     R  RESTART",
    font=("Courier New", 11, "bold"), justify="left",
    bg="#101020", fg="#c8c8dd"
).pack()

show_paths = True


def make_ghost(name, color, row, col, finder):
    ghost = {}
    ghost["name"] = name
    ghost["color"] = color
    ghost["row"] = row
    ghost["col"] = col
    ghost["finder"] = finder
    ghost["path"] = []
    ghost["nodes"] = 0
    ghost["stuck"] = False
    ghost["route_status"] = ""
    return ghost


def new_game():
    global pac_row, pac_col, dir_row, dir_col, want_row, want_col
    global ghosts, started, game_over, paused, ticks, message

    board.reset_maze()
    pac_row = START_ROW
    pac_col = START_COL
    board.eat_dot(pac_row, pac_col)

    dir_row = 0
    dir_col = 0
    want_row = 0
    want_col = 0

    ghosts = [
    make_ghost("Red: BFS", "#f52b35",
               14, 10, ghost_bfs.find_path),
    
    make_ghost("Pink: BestFirst", "#f0a2e8",
               12, 12, ghost_bestfirst.find_path),

    make_ghost("Blue: B&B", "#1bcddd",
               14, 12, ghost_bnb.find_path),

    make_ghost("Green: A*", "#6cde87",
               13, 11, ghost_Astar.find_path),

    make_ghost("Orange: Hill", "#ffb82e",
               12, 10, ghost_hill.find_path),


    ]

    started = False
    game_over = False
    paused = False
    ticks = 0
    message = "READY!"


def key_press(event):
    global want_row, want_col, started, game_over, paused, message, show_paths
    key = event.keysym

    if key == "Up":
        want_row = -1
        want_col = 0
    elif key == "Down":
        want_row = 1
        want_col = 0
    elif key == "Left":
        want_row = 0
        want_col = -1
    elif key == "Right":
        want_row = 0
        want_col = 1

    if key == "Up" or key == "Down" or key == "Left" or key == "Right":
        if started == False and game_over == False:
            started = True
            message = ""

    if key.lower() == "r":
        new_game()
    if key.lower() == "p":
        show_paths = not show_paths
    if key == "space" and started and not game_over:
        paused = not paused
        message = "PAUSED" if paused else ""


def move_pacman():
    global pac_row, pac_col, dir_row, dir_col

    destination = board.get_move_destination(pac_row, pac_col, want_row, want_col)
    if destination is not None:
        pac_row, pac_col = destination
        dir_row = want_row
        dir_col = want_col
    else:
        destination = board.get_move_destination(pac_row, pac_col, dir_row, dir_col)
        if destination is not None:
            pac_row, pac_col = destination

    board.eat_dot(pac_row, pac_col)


def move_ghosts():
    for g in ghosts:
        start = (g["row"], g["col"])
        goal = (pac_row, pac_col)

        path, nodes = g["finder"](start, goal)
        g["path"] = path
        g["nodes"] = nodes

        if start == goal:
            g["route_status"] = "AT GOAL"
        elif not path:
            g["route_status"] = "UNREACHABLE"
        elif g["finder"] == ghost_hill.find_path:
            g["route_status"] = "STEP ONLY" if len(path) > 1 else "LOCAL MIN"
        else:
            g["route_status"] = "COMPLETE"

        if len(path) > 1:
            g["row"] = path[1][0]
            g["col"] = path[1][1]
            g["stuck"] = False
        else:
            g["stuck"] = True


def check_game():
    global game_over, message

    for g in ghosts:
        if g["row"] == pac_row and g["col"] == pac_col:
            game_over = True
            message = "GAME OVER - press R"

    if board.count_dots() == 0 and game_over == False:
        game_over = True
        message = "YOU WIN - press R"


def draw_all():
    board.draw_maze(canvas)
    if show_paths:
        for g in ghosts:
            board.draw_path(canvas, g)
    board.draw_pacman(canvas, pac_row, pac_col, (dir_row, dir_col))
    for g in ghosts:
        board.draw_ghost(canvas, g)
    if message != "":
        board.draw_message(canvas, message)
    board.show_stats(label, ghosts)
    score_display.config(text=str(board.score).zfill(6))
    dots_display.config(text=str(board.count_dots()).zfill(3))


def game_loop():
    global ticks

    if started and not game_over and not paused:
        move_pacman()
        check_game()

        if not game_over:
            ticks = ticks + 1
            if ticks % GHOST_SLOW == 0:
                move_ghosts()
                check_game()

    draw_all()
    root.after(TICK, game_loop)


new_game()
root.bind("<Key>", key_press)
game_loop()
root.mainloop()
