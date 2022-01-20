# Objective: defend the ball from getting into the goal post
import random
import pygame
from pygame import K_SPACE, K_x

import Playground
import SoccerTeamPlayers


def move(playr, dest):  # For AI
    for index in range(len(dest)):
        if dest[index] > playr.position[index]:
            playr.position[index] += 1

        if dest[index] < playr.position[index]:
            playr.position[index] -= 1


def shoot(player):
    ball = Playground.ball
    res = player.team.team_number is SoccerTeamPlayers.Teams.TEAM_ONE

    # pushes the ball to the right side to make it 'shoot' in the goal
    if pygame.key.get_pressed()[K_SPACE] and res:
        ball.position[0] += 3 + random.randint(0, 3)
        ball.position[1] += 5 + random.randint(-3, 2)

    # pushes the ball to the left side to make it 'shoot' in the goal
    if pygame.key.get_pressed()[K_x] and not res:
        ball.position[0] += 3 + random.randint(0, 3)
        ball.position[1] += 5 + random.randint(0, 3)


def playingDefense(team_playing, selected_player, bounds=None):
    if bounds is None:
        bounds = selected_player[0] < Playground.half_width

    if team_playing is not selected_player.team:
        original_pos = selected_player.position
        ball = Playground.ball
        while ball.position is not selected_player.position and bounds:
            if Playground.inBounds(selected_player):
                move(selected_player, ball.position)

        # if ball in possession pass to teammate

        while selected_player.position is not original_pos:
            move(selected_player, original_pos)


# Objective: get the ball from defender and push forward,
# get the ball from opponent if not in possession
def playingMiddle(team_playing, selected_player):
    if team_playing is selected_player.team:
        # pass to other player
        return
    playingDefense(team_playing, selected_player, selected_player[0] in range(Playground.half_width - 100, Playground.half_width + 100))


# Objective: score into the goal post
def playingOffense(team_playing, selected_player):
    if team_playing is selected_player.team:
        if random.randint(0, 101) < 40:
            # pass to other player
            return
        else:
            # Shoot
            return

    playingDefense(team_playing, selected_player, selected_player[0] in range(Playground.half_width - 100, Playground.half_width + 100))
