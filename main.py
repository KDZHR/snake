# import random

from table import Table
from snake import Snake
import directions as direct
from factory import Factory

from tkinter import Tk, Canvas

# from brain import Brain


def change_color(event):
    canvas.configure(background="black")
    canvas.clipboard_clear()


def draw_table(event, snaps):
    if snaps:
        if snaps[-1]:
            for i in range(direct.N):
                for j in range(direct.M):
                    canvas.create_rectangle(j * direct.SZ_M, i * direct.SZ_N,
                                            (j + 1) * direct.SZ_M, (i + 1) * direct.SZ_N,
                                            fill=direct.get_color(snaps[-1][-1][i][j]))
            snaps[-1].pop()
        else:
            snaps.pop()


if __name__ == '__main__':
    # table = Table()
    # table.place((3, 3), direct.FOOD)
    # snake = Snake(table.get_random_coords(), table)
    # snapshots = list()
    # brain = Brain()
    # snapshots.append(brain.get_game_history())
    # while True:
    #     print(table)
    #     table.make_snapshot(snapshots)
    #     if not snake.move(int(input())):
    #         break
    # # print(table)

    factory = Factory()
    for i in range(direct.EPOCH_COUNT):
        # if i % 100 == 0:
        print(f"Epoch {i}")
        factory.make_epoch()
        # print("Success")

    best_brains = factory.export_epochs()
    snapshots = list()
    # we don't know anything about game that have made this brain the best, but we export some possible game
    best_brains.reverse()

    cnt = 0
    for brain in best_brains:
        cnt += 1
        snapshots.append(brain.get_game_history())
        snapshots[-1].reverse()
        if cnt == direct.SEE_LAST_X:
            break
        # print(snapshots[-1])

    print("Simulation done")

    # Works only with first type of brain
    # print("Best brain:")
    # for brain in best_brains[0].export_brains():
    #     print('\n'.join(' '.join(str(el) for el in elem) for elem in brain))
    #     print()

    root = Tk()
    root.geometry(f"{direct.APP_WIDTH}x{direct.APP_HEIGHT}")
    canvas = Canvas(root, width=direct.APP_WIDTH, height=direct.APP_HEIGHT)
    canvas.pack()
    # canvas.bind("<Button-1>", change_color)
    # canvas.bind("<Button-3>", lambda event: canvas.configure(background="white"))
    snapshots.reverse()
    canvas.bind("<Button-1>", lambda event, snaps=snapshots: draw_table(event, snaps))
    root.mainloop()
