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


def move(playr, dest, velocity=3):  # For AI
    for index in range(len(dest.position)):
        if dest.position[index] > playr.position[index]:
            playr.position[index] += velocity

        if dest.position[index] < playr.position[index]:
            playr.position[index] -= velocity


# def getHit(player):
#     # If any player collides with the ball push the ball with its velocity
#     ball = Playground.ball
#     arr = direction(player, ball)
#     for i in range(len(arr)):
#         if arr[i] > 1:
#             arr[i] = 1
#
#         if arr[i] < -1:
#             arr[i] = -1
#
#     return [5 * arr[x] for x in range(len(arr))] if Playground.playerContact(player) else [0, 0]


def shoot(player):
    ball = Playground.ball
    left_side = player.team is SoccerTeamPlayers.Teams.TEAM_ONE
    res = K_SPACE if left_side else K_x

    # pushes the ball to either side to make it 'shoot' in the goal
    if pygame.key.get_pressed()[res] and Playground.playerContact(player):
        ball.position[0] += 3 + random.randint(0, 3)
        ball.position[1] += (5 + random.randint(-3, 2)) * (1 if left_side else -1)


def pass_ball(p1, p_n):
    def getClosestPlayer(team, current_player):
        closest = None
        # Looks for each player in their team to pass to
        if type(team) is SoccerTeamPlayers.Team:
            team = team.players

        for player in team:
            if closest is None or distance(current_player, player) < distance(current_player, closest):
                closest = player
        return closest

    if Playground.playerContact(p1):
        Playground.ball.move(getClosestPlayer(p_n, p1))


# Objective: defend the ball from getting into the goal post
def playingDefense(team_playing, selected_player, other_players, bounds=None):
    team_one = selected_player.team is SoccerTeamPlayers.Teams.TEAM_ONE

    # Assigns a bound to each player or assigns the default
    if bounds is None:
        bounds = selected_player.position[0] < Playground.half_width if team_one else \
            selected_player.position[0] > Playground.half_width

    if team_playing is not selected_player.team:
        original_pos, ball = selected_player.position, Playground.ball
        withinBounds = SoccerTeamPlayers.inBounds(ball) and SoccerTeamPlayers.inBounds(selected_player)
        while ball.position is not selected_player.position and withinBounds and bounds:
            if SoccerTeamPlayers.inBounds(selected_player):
                selected_player.move(ball.position)

        # if ball in possession pass to teammate
        if Playground.playerContact(selected_player):
            pass_ball(selected_player, other_players)

        # Returns to its original position from player
        while selected_player.position is not original_pos:
            selected_player.move(original_pos)

    # Occasionally move up a bit
    if random.randint(0, 101) < 10:
        selected_player.move([10 * (1 if team_one else -1), 0])


# Objective: get the ball from defender and push forward,
# get the ball from opponent if not in possession
def playingMiddle(team_playing, selected_player, other_players):
    if team_playing is selected_player.team:
        if Playground.playerContact(selected_player):
            # pass to other player
            pass_ball(selected_player, other_players.players)
        else:
            move(selected_player, other_players.players[0])

        return
    playingDefense(team_playing, selected_player,
                   selected_player.position[0] in range(Playground.half_width - 100, Playground.half_width + 100))


# Objective: score into the goal post
def playingOffense(team_playing, selected_player, other_players):
    if team_playing is selected_player.team:
        # pass to other player or shoot
        if Playground.playerContact(selected_player):
            pass_ball(selected_player, other_players) if random.randint(0, 101) < 40 else shoot(selected_player)
        else:
            move(selected_player, Playground.ball)
        return

    team_one = selected_player.team is SoccerTeamPlayers.Teams.TEAM_ONE
    bound = selected_player[0] > Playground.half_width if team_one else selected_player[0] < Playground.half_width
    playingDefense(team_playing, selected_player, bound)


def robotMovement(team, players):  # TODO
    global ball
    position, place = SoccerTeamPlayers.MovingPosition, 0

    # For forward
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
