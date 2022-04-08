import directions as direct
from copy import deepcopy
from random import randint


class Table:
    def __init__(self):
        self.table = [[direct.EMPTY] * direct.M for _ in range(direct.N)]
        self.n = direct.N
        self.m = direct.M
        self.food_freq = direct.FOOD_FREQ

    # unsafe, maybe just [coords]?
    def get(self, coords):
        if 0 <= coords[0] < self.n and 0 <= coords[1] < self.m:
            return self.table[coords[0]][coords[1]]
        else:
            return direct.WALL

    # unsafe
    def place(self, coords, val):
        self.table[coords[0]][coords[1]] = val

    def __str__(self):
        return '\n'.join(''.join(elem) for elem in self.table)

    def make_snapshot(self, snapshots):
        snapshots.append(deepcopy(self.table))

    def get_random_coords(self):
        return randint(0, self.n - 1), randint(0, self.m - 1)

    # unsafe
    def place_food_carefully(self):
        coords = self.get_random_coords()
        while self.get(coords) != direct.EMPTY:
            coords = self.get_random_coords()
        self.place(coords, direct.FOOD)

    def place_food(self):
        if randint(1, self.food_freq) == 1:
            self.place_food_carefully()
