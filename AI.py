import random
from math import sqrt
import pygame
from pygame import *
import Playground
import SoccerTeamPlayers


# Function to calculate the distance between two objects
def distance(obj1, obj2):
    r1, r2 = direction(obj1, obj2)
    # Distance formula
    return sqrt(r1 ** 2 + r2 ** 2)


def direction(obj1, obj2):
    x1, y1 = obj1.position
    x2, y2 = obj2.position

    # vertical, horizontal movement
    return [x2 - x1, y2 - y1]


def move(playr, dest, velocity=1):  # For AI
    for index in range(len(dest.position)):
        if dest.position[index] > playr.position[index]:
            playr.position[index] += velocity

        if dest.position[index] < playr.position[index]:
            playr.position[index] -= velocity


def shoot(player):
    ball = Playground.ball
    left_side = player.team is SoccerTeamPlayers.Teams.TEAM_ONE
    res = K_SPACE if left_side else K_x

    # pushes the ball to either side to make it 'shoot' in the goal
    if pygame.key.get_pressed()[res] and Playground.playerContact(player):
        ball.position[0] += 3 + random.randint(0, 3)
        ball.position[1] += (5 + random.randint(-3, 2)) * (1 if left_side else -1)


def getClosestPlayer(team, current_player):
    closest = None
    # Looks for each player in their team to pass to
    for player in team.players:
        if closest is None or distance(current_player, player) < distance(current_player, closest):
            closest = player
    return closest


def pass_ball(p1, p_n):
    if Playground.playerContact(p1):
        move(Playground.ball, getClosestPlayer(p_n, p1), 3)


# Objective: defend the ball from getting into the goal post
def playingDefense(team_playing, selected_player, other_players, bounds=None):
    if bounds is None:
        team_one = selected_player.team is SoccerTeamPlayers.Teams.TEAM_ONE
        bounds = selected_player.position[0] < Playground.half_width if team_one else \
            selected_player.position[0] > Playground.half_width

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
def playingMiddle(team_playing, selected_player, other_players):
    if team_playing is selected_player.team:
        # pass to other player
        pass_ball(selected_player, other_players)
        return
    playingDefense(team_playing, selected_player,
                   selected_player.position[0] in range(Playground.half_width - 100, Playground.half_width + 100))


# Objective: score into the goal post
def playingOffense(team_playing, selected_player, other_players):
    if team_playing is selected_player.team:
        # pass to other player or shoot
        pass_ball(selected_player, other_players) if random.randint(0, 101) < 40 else shoot(selected_player)
        return

    team_one = selected_player.team is SoccerTeamPlayers.Teams.TEAM_ONE
    bound = selected_player[0] > Playground.half_width if team_one else selected_player[0] < Playground.half_width
    playingDefense(team_playing, selected_player, bound)


def robotMovement(team, players):  # TODO
    global ball
    place = 0
    # For forward
    position = SoccerTeamPlayers.MovingPosition

    for x in range(position.FORWARD.value):
        playingOffense(team, players.players[place], players)
        place += 1

    # For middle
    for x in range(position.MIDDLE.value):
        playingMiddle(team, players.players[place], players)
        place += 1

    # For defense
    for x in range(position.DEFENSE.value):
        playingDefense(team, players.players[place], players)
        place += 1
