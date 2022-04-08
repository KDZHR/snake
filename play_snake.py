import tkinter

from snake import Snake
from table import Table
import directions as direct

from tkinter import Tk, Canvas


def move_snake(event: tkinter.Event):
    # print(event.char, event.type, event.keysym)
    global table, snake
    if not snake.move(direct.BIND_DICT[event.keysym]):
        table = Table()
        snake = Snake((3, 3), table)
    draw()


def draw():
    for i in range(direct.N):
        for j in range(direct.M):
            canvas.create_rectangle(j * direct.SZ_M, i * direct.SZ_N,
                                    (j + 1) * direct.SZ_M, (i + 1) * direct.SZ_N,
                                    fill=direct.get_color(table.get((i, j))))


if __name__ == "__main__":
    table = Table()
    snake = Snake((3, 3), table)
    root = Tk()
    root.geometry(f"{direct.APP_WIDTH}x{direct.APP_HEIGHT}")
    canvas = Canvas(root, width=direct.APP_WIDTH, height=direct.APP_HEIGHT)
    # not in right order
    root.bind("<Left>", move_snake)
    root.bind("<Right>", move_snake)
    root.bind("<Up>", move_snake)
    root.bind("<Down>", move_snake)
    canvas.pack()
    draw()
    canvas.mainloop()
