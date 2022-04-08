import directions as direct


class Snake:
    def __init__(self, coords, table):
        self.snake_coords = list()
        self.snake_coords.append(coords)
        self.table = table
        self.table.place(coords, direct.SNAKE)  # ?

    def __str__(self):
        return self.table.__str__()

    def can_move(self, direction):
        new_head_coords = direct.get_new_coords(self.snake_coords[-1], direction)
        return (new_head_coords == self.snake_coords[0] and len(self.snake_coords) > 2) or \
               self.table.get(new_head_coords) in (direct.EMPTY, direct.FOOD)

    # direction: 0, 1, 2, 3 (L, R, U, D)
    def move(self, direction):
        new_head_coords = direct.get_new_coords(self.snake_coords[-1], direction)
        if self.can_move(direction):
            ate_food = self.table.get(new_head_coords) == direct.FOOD
            if not ate_food:
                self.table.place(self.snake_coords[0], direct.EMPTY)
                self.snake_coords.pop(0)  # needs fix, detected exploit with len = 2
            self.table.place(new_head_coords, direct.SNAKE)
            self.snake_coords.append(new_head_coords)
            self.table.place_food()
            return direct.TIME_REWARD + (direct.FOOD_REWARD if ate_food else 0)

    def get_head_coords(self):
        return self.snake_coords[-1]
