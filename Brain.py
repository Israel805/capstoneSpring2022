from random import shuffle
import numpy as np

import SoccerTeamPlayers
from Constant import *

ticks: int = 0


def negateAll(arr: list, extra=0):
    result = arr.copy()
    for i in range(len(arr)):
        result[i][0] = (- 1 * arr[i][0]) + extra
    return result


def game_time_complete():
    return float(counter)


def flip_pos(positions):
    if positions.ndim == 2:
        return negateAll(positions, screen_width)

    result = positions.copy()
    result[0] = screen_width - 1 - positions[0]
    return result


def flip_vel(velocities):
    if velocities.ndim == 2:
        return negateAll(velocities)

    result = velocities.copy()
    result[0] = -1 * velocities[0]

    return result


def flip_acc(accelerations):
    if accelerations.ndim == 2:
        return negateAll(accelerations)

    return accelerations.copy()


class Brain:
    def __init__(self, t1, t2, ball):
        self.team_one, self.team_two = t1, t2
        self.ball = ball

    def run_brains(self):
        # Collects all the positions and velocities of each player for each team
        p1_pos, p1_vel = self.team_one.positionMatrix(), self.team_one.velocityMatrix()
        p2_pos, p2_vel = self.team_two.positionMatrix(), self.team_two.velocityMatrix()

        # Saves the ball velocity and position
        ball_pos, ball_vel = self.ball.position, self.ball.velocity

        game_time = game_time_complete()

        # Saves the brain of both teams
        t1_brain, t2_brain = self.team_one.brain, self.team_two.brain

        # Makes the move according to the brain with all the information saved
        t1_move = t1_brain.move(p1_pos, p1_vel, p2_pos, p2_vel, ball_pos, ball_vel, score[0], score[1], game_time)

        # Applies the move to team one
        self.team_one.applyMoveToAllPlayers(t1_move)

        # Translate team's 2 positions and velocities so that both brains
        # think that they are playing from left (0, y) to right (MAX_X,y)
        t2_move = t2_brain.move(flip_pos(p2_pos), flip_vel(p2_vel), flip_pos(p1_pos), flip_vel(p1_vel),
                                flip_pos(ball_pos), flip_vel(ball_vel), score[1], score[0], game_time)
        t2_move = flip_acc(t2_move)

        # Applies the move to team one
        self.team_two.applyMoveToAllPlayers(t2_move)

    def limit_velocities(self):
        def checkVelocity(obj, num: int):
            max_vel = [max_ball_velocity, max_player_velocity]
            obj_vel = obj.normal_velocity()
            if obj_vel > max_vel[num]:
                obj.velocity = np.multiply(obj.velocity, max_vel[num] / obj_vel)

        checkVelocity(self.ball, 0)

        # Checks if the player velocity is over the max velocity
        for t in [self.team_one, self.team_two]:
            [checkVelocity(p, 1) for p in t.players]


def updates(list_input: list):
    global ticks
    ticks = ticks + 1

    new_bodies = []
    for b1 in list_input:
        new_body = b1
        for b2 in list_input:
            if b1 != b2:
                new_body = new_body.calculate_collision(b2)
        new_body.bounce_wall()
        new_bodies.append(new_body)
        if type(new_body) is not SoccerTeamPlayers.User:
            new_body.move()

    for i in range(len(list_input)):
        list_input[i].set_pos_vel(new_bodies[i])

    shuffle(list_input)
