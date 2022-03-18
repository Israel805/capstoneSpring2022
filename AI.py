import random
from math import sqrt

import Constant
import Playground
import SoccerTeamPlayers
from Ball import pass_ball, shoot


# Function to calculate the distance between two objects
def distance(obj1, obj2):
    r1, r2 = direction(obj1, obj2)
    # Distance formula
    return sqrt(r1 ** 2 + r2 ** 2)


# Calculates the direction on where it is going
def direction(obj1, obj2):
    # Finds the position in the objects
    if type(obj1) is not list:
        obj1 = obj1.position

    if type(obj2) is not list:
        obj2 = obj2.position

    x1, y1 = obj1
    x2, y2 = obj2

    # vertical, horizontal movement
    return [x2 - x1, y2 - y1]


''' Ideas that could work '''


def distanceToOpponentGoal(start_point, team):
    return Playground.distance(start_point, team.scoringGoal)


def getTeammates(number):
    return {SoccerTeamPlayers.Teams.TEAM_ONE: team_one,
            SoccerTeamPlayers.Teams.TEAM_TWO: team_two}.get(number)


def pressBall(team, player):
    touchedAndSameTeam = Playground.distance(player, Playground.ball) < 10 and team is player.team.team_number
    # Check if distance is short and player is in control
    player.velocity = 5 * (
        1.2 if touchedAndSameTeam and distanceToOpponentGoal(player, team) else 1.6)  # max speed w/ or w/o ball


# ?
def closeByOpponents(current_player, opponents):
    for opp in opponents:
        # calculate distance to the player. If opponent is in front of the player, return true
        if Playground.distance(current_player, opp) ** 2 < 60:  # good distance
            return True
    return False


# test
def isSafeToPassForward(current_player):
    team = current_player.team

    for other_players in team.players:
        if other_players.position[0] <= current_player[0]:
            continue

        # Get other players around them
        # Get list of players to see if they ar close to opponent
        other_players.isSafeToReceive()


def isPassSafe(sender, receiver, opp, force, playerReceiving=None):
    localPosOpp = ToTarget = [receiver.position[x] - sender.position[x] for x in range(len(sender))]

    #  if opponent is behind the kicker then pass is considered okay(this is
    #   based on the assumption that the ball is going to be kicked with a
    #   velocity greater than the opponent's max velocity)
    if localPosOpp[0] < 0:
        return True

    # if the opponent is further away than the target we need to consider if
    #   the opponent can reach the position before the receiver.
    if Playground.distance(sender, receiver) < Playground.distance(opp, sender):
        if playerReceiving:
            return Playground.distance(receiver, opp) > Playground.distance(receiver, playerReceiving)
        return True


def isPassSafeFromAll(sender, receiver, force):
    opponentsTeam = team_one if sender.team is SoccerTeamPlayers.Teams.TEAM_ONE else team_two
    for opponents in opponentsTeam:
        if not isPassSafe(sender, receiver, opponents, force):
            return False
    return True


def determineBestSpot(currentPlayer):
    # Resets the best spot
    bestSpot = None

    currentBestSpot = 0.0
    for other_players in currentPlayer.teammates:
        if closeByOpponents(other_players, currentPlayer.opponents):
            continue


# Needs work
def getAvailableSpots(team):
    result = None
    for players in team:
        if players.isSafeToReceive:
            result = players

    return result


''' Ideas that could work \ end '''


# Similar to user movement, have them able to move freely
def moveAllDirectionsAI(currentPlayer):
    self = SoccerTeamPlayers.CheckAIMovement(currentPlayer.position, Playground.player_size)

    # The outer circle doesnt touch the left side, increment in x coordinate
    self.moveLeft()
    # Only to the right of the screen, decrement in x coordinate
    self.moveRight()
    # If below the scoreboard, increment in y coordinate
    self.moveUp()
    # if down arrow key is pressed, decrement in y coordinate
    self.moveDown()


def player_update(player):
    # player.addClosePlayer()
    pass


# Objective: defend the ball from getting into the goal post
def playingDefense(team_playing, selected_player, bounds=None):
    team_one_region = lambda x: x in range(20, Playground.half_width)
    team_two_region = lambda x: x in range(Playground.half_width, Playground.screen_width - 20)

    team_one = selected_player.team is SoccerTeamPlayers.Teams.TEAM_ONE

    if team_playing is not selected_player.team:
        original_pos, ball = selected_player.position, Playground.ball
        while ball.position is not selected_player.position and bounds:
            selected_player.move()  # to the ball

        # if ball in possession pass to teammate
        if Playground.playerContact(selected_player):
            pass_ball(selected_player, getTeammates(team_playing))

        # Returns to its original position from player
        while selected_player.position is not original_pos:
            selected_player.move()  # to original position

    # Occasionally move up a bit
    if random.randint(0, 101) < 10:
        selected_player.move()  # [10 * (1 if team_one else -1), 0]


# Objective: get the ball from defender and push forward,
# get the ball from opponent if not in possession
def playingMiddle(team_playing, selected_player, bounds):
    if team_playing is selected_player.team:
        if Playground.playerContact(selected_player):
            # pass to other player
            pass_ball(selected_player, getTeammates(team_playing))
        else:
            temp = (1 if selected_player.team is SoccerTeamPlayers.Teams.TEAM_ONE else -1)
            selected_player.move()  # [10 * (1 if team_one else -1), 0]

        return
    # playingDefense(team_playing, selected_player,
    #                selected_player.position[0] in range(Playground.screen_width * .25, Playground.screen_width * .75))


# Objective: score into the goal post
def playingOffenseForTeamOne(team_playing, selected_player, bounds, counter=0):
    while Playground.ball.getPossession() is team_playing:
        moveForward = bounds.moveLeft()
        # selected_player.
        # while distanceToOpponentGoal(selected_player.position,selected_player.team):

        # pass to other player or shoot
        if Playground.playerContact(selected_player):
            if random.randint(0, 101) < random.randint(0, 101):
                pass_ball(selected_player, getTeammates(team_playing))
            else:
                shoot(selected_player)
        return

    # if the player with possession is not our team, play defensively to get the ball
    playingDefense(team_playing, selected_player, bounds)

    # if the ball is back into possession, try to keep scoring
    if counter < 3:  # tries for 3 times until give up
        playingOffenseForTeamOne(team_playing, selected_player, bounds, counter + 1)


# def playingOffenseForTeamTwo()


def initializeTeammates(team_number, team):
    positioning = Constant.TeamPosition
    for eachPlayer in team:
        bounds = SoccerTeamPlayers.CheckAIMovement(eachPlayer.position, Playground.player_size)
        if eachPlayer.team_position is positioning.STRIKER:
            playingOffenseForTeamOne(team_number, eachPlayer, bounds)
            continue

        if eachPlayer.team_position is positioning.MIDDLE:
            playingMiddle(team_number, eachPlayer, bounds)
            continue

        if eachPlayer.team_position is positioning.DEFENSE:
            playingDefense(team_number, eachPlayer, bounds)


def robotMovement(team_number, team: list):  # TODO
    global team_one, team_two

    if team_number is SoccerTeamPlayers.Teams.TEAM_ONE:
        team_one = team
    else:
        team_two = team

    initializeTeammates(team_number, team)
