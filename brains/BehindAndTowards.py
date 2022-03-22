from brains.BaseBrainUtils import *


class BehindAndTowards(BaseBrainUtils):
    def do_move(self) -> np.array:
        actions = [[0] * 2] * 5
        for i in range(5):
            actions[i] = (self.run_towards(i, self.ball_pos)) if self.is_behind_ball(i) else (run_back())

        return np.array(actions)
