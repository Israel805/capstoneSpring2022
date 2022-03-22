from random import random
from abstractbrain import *


class RandomWalk(AbstractBrain):
    def do_move(self) -> np.array:
        # actions = [[0] * 2] * 5
        actions = []
        for i in range(5):
            actions.append([random() - 0.5, random() - 0.5])
        return np.array(actions)
