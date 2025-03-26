import random as rnd
import haravasto as hv
import time
import sys
import os
from menu import create_main_menu, exit_menu
from datetime import datetime

game_state = {
        "visible_grid": [],
        "hidden_grid": [],
        }

statistics = {
    "time": 0,
    "clicks": 0,
    "date": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
}

def create_grid(width, height):
    grid = []
    for i in range(height):
        grid.append([])
        for n in range(width):
            grid[-1].append(" ")

    remaining = []
    for x in range(width):
        for y in range(height):
            remaining.append((x, y))

    return grid, remaining

def place_mines(area, free_cells, mines):
    for i in range(mines):
        random_cell = rnd.choice(free_cells)
        x, y = random_cell
        area[y][x] = "x"
        free_cells.remove(random_cell)

def draw_handler():
    hv.clear_window()
    hv.start_drawing_tiles()
    for y_index, row in enumerate(game_state["visible_grid"]):
        y_coord = y_index * 40 
        for x_index, key in enumerate(row):
            x_coord = x_index * 40
            hv.add_drawable_tile(key, x_coord, y_coord)
    hv.draw_tiles()

def count_mines(grid, x, y):
    mines = 0
    for row in grid[max(y-1, 0): y+2]:
        for cell in row[max(x-1, 0): x+2]:
            if cell == "x":
                mines += 1
    return mines

def process_hidden_grid(grid):
    for i, row in enumerate(grid):
        for n, cell in enumerate(row):
            if cell != "x":
                grid[i][n] = str(count_mines(grid, n, i))

def write_to_stats(file):
    try:
        with open(file, "a") as f:
            time_elapsed = statistics["time"]
            date = statistics["date"]
            moves = statistics["clicks"]
            mins, sec = divmod(time_elapsed, 60)
            result = "Win" if not free_cells else "Loss"
            f.write("Date: {date}\nTime: {mins} min {s} s\nMoves: {moves}\nResult: {result}\nSize: {width}x{height} with {mines} mines\n\n".format(
                                date=date, mins=mins, s=sec,
                                width=width, height=height,
                                mines=mines, moves=moves, result=result))
    except IOError:
        print("File opening failed")

def open_stats():
    with open("stats.txt") as f:
        if sys.platform == "win32":
            os.system("start " + "stats.txt")
        else:
            os.system("vim stats.txt &")

def flood_fill(hidden, visible, x, y):
    if (x, y) in free_cells:
        statistics["clicks"] += 1
    if hidden[y][x] == "x":
        for i, row in enumerate(hidden):
            for n, cell in enumerate(row):
                if cell == "x":
                    visible[i][n] = hidden[i][n]
        statistics["clicks"] += 1
        hv.stop()
    else:
        area = [(x, y)]
        while area:
            xk, yk = area.pop(-1)
            visible[yk][xk] = hidden[yk][xk]
            if hidden[yk][xk] != "0" and hidden[yk][xk] != "x":
                visible[yk][xk] = hidden[yk][xk]
                if (xk, yk) in free_cells:
                    free_cells.remove((xk, yk))
                continue
            for i in range(yk-1, yk+2):
                for n in range(xk-1, xk+2):
                    if (0 <= i < len(hidden)) and (0 <= n < len(hidden[i])):
                        if (visible[i][n] == " " or visible[i][n] == "f") and (hidden[i][n] != "x"):
                            area.append((n, i))
                            if (n, i) in free_cells:
                                free_cells.remove((n, i))

def flag_tile(grid, x, y):
    if grid[y][x] == "f":
        grid[y][x] = " "
    elif grid[y][x] == " ":
        grid[y][x] = "f"

def mouse_handler(x, y, button, modifier):
    if button == hv.LEFT_MOUSE:
        flood_fill(game_state["hidden_grid"], game_state["visible_grid"], int(x/40), int(y/40))
        if not free_cells:
            hv.stop()
    if button == hv.RIGHT_MOUSE:
        flag_tile(game_state["visible_grid"], int(x/40), int(y/40))

def timer(n):
    statistics["time"] += 1

def main():
    game_state["visible_grid"], _ = create_grid(width, height)
    game_state["hidden_grid"], _ = create_grid(width, height)
    visible = game_state["visible_grid"]
    hidden = game_state["hidden_grid"]
    width_px = len(visible[0]) * 40
    height_px = len(visible) * 40
    place_mines(hidden, free_cells, mines)
    process_hidden_grid(hidden)
    hv.load_images("sprites")
    hv.create_window(width_px, height_px)
    hv.set_repeat_handler(timer, interval=1)
    hv.set_draw_handler(draw_handler)
    hv.set_mouse_handler(mouse_handler)
    hv.start()
    write_to_stats("stats.txt")
    exit_menu(free_cells)

if __name__ == "__main__":
    while True:
        try:
            width, height, mines = create_main_menu(open_stats)
            statistics["time"] = 0
            statistics["clicks"] = 0
        except TypeError:
            break
        else:
            _, free_cells = create_grid(width, height)
            main()
