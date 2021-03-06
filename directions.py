X = [-1, +1, 0, 0]
Y = [0, 0, -1, +1]

EMPTY = '.'
SNAKE = 'S'
FOOD = '*'
WALL = 'W'

APP_HEIGHT = 900
APP_WIDTH = 900
N = 10
M = 10
SZ_N = APP_HEIGHT // N
SZ_M = APP_WIDTH // M
FOOD_FREQ = 2
VISION_RADIUS = 5
COUNT_PER_EPOCH = 100
EPOCH_COUNT = 10000
MAX_TIME = 100
FOOD_REWARD = 20
TIME_REWARD = 0
MUTATION_RATE = 5
SEE_LAST_X = 100
TEST_COUNT = 5
START_FOOD_COUNT = 5

BIND_DICT = {"Up": 0, "Down": 1, "Left": 2, "Right": 3}


def get_new_coords(xy, direction):
    return xy[0] + X[direction], xy[1] + Y[direction]


# dict?
def get_color(direct_tag):
    if direct_tag == FOOD:
        return "red"
    if direct_tag == EMPTY:
        return "white"
    if direct_tag == SNAKE:
        return "green"
    return "black"  # wall
