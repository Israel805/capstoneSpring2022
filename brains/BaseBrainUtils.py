import Constant
from abstractbrain import *


def run_back():
    return [-1, 0]


class BaseBrainUtils(AbstractBrain, ABC):
    def __init__(self, ball):
        super().__init__()
        self.ball = ball

    def run_towards(self, player_index, position, scale_factor=1):
        acceleration = np.subtract(position, self.my_players_pos[player_index])
        if scale_factor > 1:
            acceleration = np.divide(acceleration, scale_factor)

        return acceleration

    def is_behind_ball(self, player_index):
        return self.my_players_pos[player_index][0] < self.ball.position[0] - 5

    def is_ball_direction_forward(self):
        return self.ball.velocity[0] > 0

    def calculate_ball_x_intersection(self, x):
        ball_x, ball_y = self.ball.position
        ball_dx, ball_dy = self.ball.velocity

        t = abs((ball_x - x) / ball_dx)
        y = ball_y + t * ball_dy
        y_multiples = int(y // Constant.screen_height)

        return y % Constant.screen_height if (y_multiples % 2) == 0 else \
            Constant.screen_height - (y % Constant.screen_height)

    def distance_to_ball(self, i):
        return np.linalg.norm(np.subtract(self.ball_pos, self.my_players_pos[i]))
