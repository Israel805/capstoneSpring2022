from random import random
from abstractbrain import *


class RandomWalk(AbstractBrain):
    def do_move(self) -> np.array:
        # Randomly goes wherever
        # actions = [[0] * 2] * 5
        return np.array([[(random() - 0.5), (random() - 0.5)] for _ in range(5)])
