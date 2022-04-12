from random import random

from brains.BaseBrainUtils import *


class DefendersAndAttackers(BaseBrainUtils):
    BASE_POS = [[100., 200.], [180., 600.], [600., 300.], [600., 500.]]

    def do_move(self) -> np.array:
        result = []

        for i in range(4):
            if 25 < self.distance_to_ball(i) < (i + 1) * 100:
                is_behind = self.is_behind_ball(i) and 0.8 > random()
                result.append((self.run_towards(i, self.ball_pos)) if is_behind else (run_back()))
                continue

            target = self.BASE_POS[i]

            if self.is_behind_ball(i):
                temp = target[0]
                target = temp - 15, self.calculate_ball_x_intersection(temp)
                result.append(self.run_towards(i, target))
                continue

            result.append((self.run_towards(i, target)) if self.is_ball_direction_forward() else (run_back()))

        result.append(self.run_towards(4, self.ball_pos) if self.is_behind_ball(4) else run_back())
        return np.array(result)


