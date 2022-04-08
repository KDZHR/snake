import directions as direct
from brain import Brain
from random import randint, getstate, setstate


class Factory:
    def __init__(self):
        self.n = direct.N
        self.m = direct.M
        self.radius = direct.VISION_RADIUS
        self.count = direct.COUNT_PER_EPOCH
        self.brains = [Brain() for _ in range(self.count)]
        self.best_brain_in_epoch = list()

    def cross(self, first_ind, second_ind):
        new_brain = Brain()
        for i in range(2 * self.radius - 1):
            for j in range(2 * self.radius - 1):
                for k in range(4):
                    new_brain.set((i, j), self.brains[first_ind if randint(0, 1) == 0
                                                                else second_ind].get_cell((i, j), False), False)
                    new_brain.set((i, j), self.brains[first_ind if randint(0, 1) == 0
                                                                else second_ind].get_cell((i, j), True), True)
        return new_brain

    def get_score(self, ind):
        # setstate(rnd_state)
        return sum(self.brains[ind].get_score() for _ in range(direct.TEST_COUNT))

    def make_epoch(self):
        # rnd_state = getstate()
        scores = [(self.get_score(i), i) for i in range(self.count)]
        scores.sort(reverse=True)
        self.best_brain_in_epoch.append(self.brains[scores[0][1]])  # deepcopy?
        new_brains = [self.cross(scores[randint(0, 2 * self.count // 3)][1], scores[randint(0, 2 * self.count // 3)][1])
                      for _ in range(self.count)]
        # for i in range(self.count):
        #     a, b = randint(0, self.count // 2), randint(0, self.count // 2)
        #     new_brains[i] = self.cross(scores[a][1], scores[b][1])
        self.brains = new_brains
        for _ in range(self.count // direct.MUTATION_RATE):
            self.brains[randint(0, self.count - 1)].mutate()

    def export_epochs(self):
        return self.best_brain_in_epoch
