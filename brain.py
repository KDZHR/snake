from random import random, randint

from snake import Snake
from table import Table
import directions as direct


class Brain:
    def __init__(self):
        self.radius = direct.VISION_RADIUS
        self.food_brain = self.get_random_matrix()
        self.wall_brain = self.get_random_matrix()

    def rand(self):
        # return 2 * random() - 1
        return randint(-100000, 1000000)

    def get_random_matrix(self):
        return [[[self.rand() for _ in range(4)] for _ in range(2 * self.radius - 1)] for _ in range(2 * self.radius - 1)]

    def ask_table(self, table, head_coords, i, j):
        return table.get((head_coords[0] + i, head_coords[1] + j))

    def make_decision(self, table, head_coords):
        weights = [0] * 4
        for i in range(2 * self.radius - 1):
            for j in range(2 * self.radius - 1):
                val = self.ask_table(table, head_coords, i, j)
                if val == direct.FOOD:
                    for k in range(4):
                        weights[k] += self.food_brain[i][j][k]
                elif val in (direct.FOOD, direct.WALL):
                    for k in range(4):
                        weights[k] += self.wall_brain[i][j][k]
        max_val = max(weights)
        for i in range(4):
            if weights[i] == max_val:
                return i

    def set(self, coords, val, is_food_brain):
        if is_food_brain:
            self.food_brain[coords[0]][coords[1]] = val
        else:
            self.wall_brain[coords[0]][coords[1]] = val

    def get_random_coords(self):
        return randint(0, 2 * self.radius - 2), randint(0, 2 * self.radius - 2)

    def mutate(self):
        x, y = self.get_random_coords()
        if randint(0, 1) == 0:
            self.food_brain[x][y] = [self.rand() for _ in range(4)]
        else:
            self.wall_brain[x][y] = [self.rand() for _ in range(4)]

    def get_score(self):
        table = Table()
        snake = Snake(table.get_random_coords(), table)
        for _ in range(direct.START_FOOD_COUNT):
            table.place_food_carefully()
        score = 0
        for _ in range(direct.MAX_TIME):
            plus_val = snake.move(self.make_decision(table, snake.get_head_coords()))
            if plus_val is None:
                break
            score += plus_val
        return score

    def get_cell(self, coords, is_food_brain):
        return self.food_brain[coords[0]][coords[1]] if is_food_brain else self.wall_brain[coords[0]][coords[1]]

    def get_game_history(self):
        table = Table()
        snake = Snake(table.get_random_coords(), table)
        for _ in range(direct.START_FOOD_COUNT):
            table.place_food_carefully()
        snaps = list()
        for _ in range(direct.MAX_TIME):
            table.make_snapshot(snaps)
            if snake.move(self.make_decision(table, snake.get_head_coords())) is None:
                break
        return snaps

    def export_brains(self):
        return self.food_brain, self.wall_brain
