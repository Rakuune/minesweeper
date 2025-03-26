from tkinter import *
import json
import sys
from datetime import datetime

def load_config():
    try:
        with open("config.json", "r") as config:
            file = json.load(config)
    except (IOError, json.JSONDecodeError):
        print("Config file could not be loaded")
    return file

def create_large_button(target, command, settings=load_config(), text="Start Game"):
    info = settings["create_menu"]["button"]
    start_button = Button(
        target,
        width=info["width"], height=info["height"],
        font=info["font"], text=text,
        bg=info["bg"], command=command)
    return start_button

def create_input_fields(target):
    width = Entry(target, width="40")
    height = Entry(target, width="40")
    mines = Entry(target, width="40")
    return width, height, mines

def exit_menu(remaining):
    exit_window = Tk()
    exit_window.geometry("500x250")
    exit_window.title("New Game?")
    win_label = Label(exit_window, text="You won the game!", font=("Mono Sans", 35))
    lose_label = Label(exit_window, text="You lost the game!", font=("Mono Sans", 35))
    new_game = Button(exit_window, text="New Game", font=("Mono Sans", 20), command=exit_window.destroy)
    exit_game = Button(exit_window, text="Exit Game", font=("Mono Sans", 20), command=sys.exit)
    new_game.place(x=75, y=180)
    exit_game.place(x=300, y=180)
    if not remaining:
        win_label.place(x=120, y=80)
    else:
        lose_label.place(x=120, y=80)
    exit_window.mainloop()

def create_menu(target, command1, command2, command3):
    target.geometry("450x600")
    target.title("Minesweeper")
    inputs = create_input_fields(target)
    for i, input_field in enumerate(inputs, 1):
        input_field.place(x=80, y=100*i)

    Label(target, text="Enter grid width.").place(x=80, y=70)
    Label(target, text="Enter grid height.").place(x=80, y=170)
    Label(target, text="Enter number of mines.").place(x=80, y=270)

    create_large_button(target, command1).place(x=80, y=360)
    create_large_button(target, command2, text="Statistics").place(x=80, y=420)
    create_large_button(target, command3, text="Exit").place(x=80, y=480)
    target.mainloop()
    
    return inputs

def handle_menu(target, menu):
    while True:
        try:
            width_input, height_input, mines_input = menu
            width = int(width_input.get())
            height = int(height_input.get())
            mines = int(mines_input.get())
            if mines > height * width:
                error = Toplevel(target, width="400", height="150")
                error_text = Label(error, text="Too many mines", font="bold")
                error_text.place(x=80, y=50)
                Button(error, text="Ok", command=error.destroy).place(x=80, y=100)
                error.mainloop()
                continue
        except ValueError:
            top = Toplevel(target, width="400", height="150")
            error_text = Label(top, text="Only integers allowed.", font="bold")
            error_text.place(x=80, y=50)
            Button(top, text="Ok", command=top.destroy).place(x=80, y=100)
            top.mainloop()
        except TclError:
            return
        else:
            return width, height, mines

def create_main_menu(command):
    try:
        display = Tk()
        width, height, mines = handle_menu(
               display, create_menu(display, display.quit, command, sys.exit))
    except TypeError:
        return
    else:
        display.destroy()
        return width, height, mines
