from random import random, randint

from snake import Snake
from table import Table
import directions as direct
from copy import deepcopy


class BrainSkeleton:
    def rand(self):
        return 2 * random() - 1
        # return randint(-100000, 1000000)

    def ask_table(self, table, head_coords, i, j):
        return table.get((head_coords[0] + i, head_coords[1] + j))

    def get_score(self):
        table = Table()
        snake = Snake(table.get_random_coords(), table)
        for _ in range(direct.START_FOOD_COUNT):
            table.place_food_carefully()
        score = 0
        for _ in range(direct.MAX_TIME):
            decision, mistake_count = self.make_decision(table, snake, snake.get_head_coords())
            plus_val = snake.move(decision)
            if plus_val is None:
                break
            score += plus_val + mistake_count * direct.BAD_CHOICE_PENALTY
        return score

    def get_game_history(self):
        table = Table()
        snake = Snake(table.get_random_coords(), table)
        for _ in range(direct.START_FOOD_COUNT):
            table.place_food_carefully()
        snaps = list()
        for _ in range(direct.MAX_TIME):
            table.make_snapshot(snaps)
            if snake.move(self.make_decision(table, snake, snake.get_head_coords())[0]) is None:
                break
        return snaps

    def get_best_decision(self, snake, weights):
        if direct.SOFT_PUNISHMENT:
            for i in range(4):
                if snake.can_move(weights[i][1]):
                    return weights[i][1], i
            return weights[0][1], 4
        else:
            return weights[0][1], 0


class B1(BrainSkeleton):
    def __init__(self):
        self.radius = direct.VISION_RADIUS
        self.food_brain = self.get_random_matrix()
        self.wall_brain = self.get_random_matrix()

    def get_random_matrix(self):
        return [[[self.rand() for _ in range(4)] for _ in range(2 * self.radius - 1)] for _ in range(2 * self.radius - 1)]

    def make_decision(self, table, snake, head_coords):
        weights = [[0, i] for i in range(4)]
        for i in range(2 * self.radius - 1):
            for j in range(2 * self.radius - 1):
                val = self.ask_table(table, head_coords, i, j)
                if val == direct.FOOD:
                    for k in range(4):
                        weights[k][0] += self.food_brain[i][j][k]
                elif val in (direct.FOOD, direct.WALL):
                    for k in range(4):
                        weights[k][0] += self.wall_brain[i][j][k]
        weights.sort(reverse=True)
        return self.get_best_decision(snake, weights)

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

    def get_cell(self, coords, is_food_brain):
        return self.food_brain[coords[0]][coords[1]] if is_food_brain else self.wall_brain[coords[0]][coords[1]]

    def export_brains(self):
        return self.food_brain, self.wall_brain

    def cross(self, other_brain):
        new_brain = deepcopy(self)
        for i in range(2 * self.radius - 1):
            for j in range(2 * self.radius - 1):
                for k in range(4):
                    if randint(0, 1) == 0:
                        new_brain.set((i, j), other_brain.get_cell((i, j), False), False)
                        new_brain.set((i, j), other_brain.get_cell((i, j), True), True)
        return new_brain


class B2(BrainSkeleton):
    def __init__(self):
        self.brain = [[self.rand() for _ in range(4)] for _ in range(16)]  # F, W

    def mutate(self):
        self.brain[randint(0, len(self.brain) - 1)] = [self.rand() for _ in range(4)]

    def set(self, coord, val):
        self.brain[coord] = val

    def get_cell(self, coord):
        return self.brain[coord]

    def cross(self, other_brain):
        new_brain = deepcopy(self)
        for i in range(len(self.brain)):
            if randint(0, 1) == 0:
                new_brain.set(i, other_brain.get_cell(i))
        return new_brain

    # SHITTY CODE
    def make_decision(self, table, snake, head_coords):
        weights = [[0, i] for i in range(4)]
        for d in range(4):
            coords = direct.get_new_coords(head_coords, d)
            dist = 1
            while table.get(coords) not in (direct.FOOD, direct.WALL):
                coords = direct.get_new_coords(coords, d)
                dist += 1
            if table.get(coords) != direct.FOOD:
                dist = direct.RATE_IF_NOT_FOUND
            for i in range(4):
                weights[i][0] += dist * self.brain[d][i]

            coords = direct.get_new_coords(head_coords, d)
            dist = 1
            while table.get(coords) not in (direct.SNAKE, direct.WALL):
                coords = direct.get_new_coords(coords, d)
                dist += 1
            for i in range(4):
                weights[i][0] += dist * self.brain[8 + d][i]

        for d1 in range(2):
            for d2 in range(2, 4):
                coords = direct.get_new_coords(direct.get_new_coords(head_coords, d1), d2)
                dist = 1
                while table.get(coords) not in (direct.FOOD, direct.WALL):
                    coords = direct.get_new_coords(direct.get_new_coords(coords, d1), d2)
                    dist += 1
                if table.get(coords) != direct.FOOD:
                    dist = direct.RATE_IF_NOT_FOUND
                for i in range(4):
                    weights[i][0] += dist * self.brain[4 + d1 * 2 + (d2 - 2)][i]

                coords = direct.get_new_coords(direct.get_new_coords(head_coords, d1), d2)
                dist = 1
                while table.get(coords) not in (direct.SNAKE, direct.WALL):
                    coords = direct.get_new_coords(direct.get_new_coords(coords, d1), d2)
                    dist += 1
                for i in range(4):
                    weights[i][0] += dist * self.brain[8 + 4 + d1 * 2 + (d2 - 2)][i]
        weights.sort(reverse=True)
        return self.get_best_decision(snake, weights)

    # def export_brains(self):
    #     return self.brain


class Brain(B1 if direct.RADIUS_BRAIN else B2):
    pass
