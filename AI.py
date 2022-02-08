import random
from math import sqrt
import Playground
import SoccerTeamPlayers
from Ball import pass_ball, shoot

friction = -0.015

# global variables for both AI
receiving = closestToTheBALL = None


# Function to calculate the distance between two objects
def distance(obj1, obj2):
    r1, r2 = direction(obj1, obj2)
    # Distance formula
    return sqrt(r1 ** 2 + r2 ** 2)


def direction(obj1, obj2):
    if type(obj1) is not list:
        obj1 = obj1.position

    if type(obj2) is not list:
        obj2 = obj2.position

    x1, y1 = obj1
    x2, y2 = obj2

    # vertical, horizontal movement
    return [x2 - x1, y2 - y1]


''' Ideas that could work '''


def distanceToOpponentGoal(team):
    pass


def pressBall(team, player):
    touchedAndSameTeam = distance(player, Playground.ball) < 10 and team is player.team.team_number
    # Check if distance is short and player is in control
    player.velocity = 5 * (
        1.2 if touchedAndSameTeam and distanceToOpponentGoal(player, team) else 1.6)  # max speed w/ or w/o ball


# ?
def closeByOpponents(current_player, opponents):
    for opp in opponents:
        # calculate distance to the player. If opponent is in front of the player, return true
        if distance(current_player, opp) ** 2 < 60:  # good distance
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
    if distance(sender, receiver) < distance(opp, sender):
        if playerReceiving:
            return distance(receiver, opp) > distance(receiver, playerReceiving)
        return True


def isPassSafeFromAll(sender, receiver, force):
    opponentsTeam = team_one if sender.team is SoccerTeamPlayers.Teams.TEAM_ONE else team_two
    for opponents in opponentsTeam:
        if not isPassSafe(sender, receiver, opponents, force):
            return False
    return True


def determineBestSpot():
    # Resets the best spot
    bestSpot = None

    currentBestSpot = 0.0
    # for


# Needs work
def getAvailableSpots(team):
    result = None
    for players in team:
        if players.isSafeToReceive:
            result = players

    return result


''' Ideas that could work \ end '''


def inBounds(ply):
    if type(ply) is list:
        return ply[0] in range(75, (Playground.half_width * 2) - 75), \
               ply[1] in range(75, (Playground.half_height * 2))

    check = SoccerTeamPlayers.CheckMovement(ply.position, ply.size)
    return check.isLeftBound() and check.isRightBound(), check.isUpperBound() and check.isLowerBound()


def move(playr, dest, velocity=3):  # For AI
    if type(dest) is list:
        for x in range(len(dest)):
            if dest[x] > 0:
                if dest[x] > playr.position[x]:
                    playr.position[x] += velocity
                if dest[x] > playr.position[x]:
                    playr.position[x] -= velocity

                dest[x] -= velocity
        return

    for index in range(len(dest.position)):
        horiz, vert = inBounds(playr)
        if dest.position[index] > playr.position[index]:
            playr.position[index] = (playr.position[index] + velocity) if horiz else 0
        if dest.position[index] < playr.position[index]:
            playr.position[index] = (playr.position[index] - velocity) if vert else 0
        # else make it bounce off specific wall


# Objective: defend the ball from getting into the goal post
def playingDefense(team_playing, selected_player, other_players, bounds=None):
    team_one_region = lambda x: x in range(20, Playground.half_width)
    team_two_region = lambda x: x in range(Playground.half_width, Playground.screen_width - 20)

    team_one = selected_player.team is SoccerTeamPlayers.Teams.TEAM_ONE

    # Assigns a bound to each player or assigns the default
    if bounds is None:
        bounds = selected_player.position[0] < Playground.half_width if team_one else \
            selected_player.position[0] > Playground.half_width

    if team_playing is not selected_player.team:
        original_pos, ball = selected_player.position, Playground.ball
        while ball.position is not selected_player.position and bounds:
            if inBounds(selected_player):
                move(selected_player, ball)

        # if ball in possession pass to teammate
        if Playground.playerContact(selected_player):
            pass_ball(selected_player, other_players)

        # Returns to its original position from player
        while selected_player.position is not original_pos:
            move(selected_player, original_pos)

    # Occasionally move up a bit
    if random.randint(0, 101) < 10:
        move(selected_player, [10 * (1 if team_one else -1), 0])


# Objective: get the ball from defender and push forward,
# get the ball from opponent if not in possession
def playingMiddle(team_playing, selected_player, other_players):
    if team_playing is selected_player.team:
        if Playground.playerContact(selected_player):
            # pass to other player
            pass_ball(selected_player, other_players.players)
        else:
            temp = (1 if selected_player.team is SoccerTeamPlayers.Teams.TEAM_ONE else -1)
            move(selected_player, [random.randint(1, 10) * temp, random.randint(-1, 1)])

        return
    # playingDefense(team_playing, selected_player,
    #                selected_player.position[0] in range(Playground.screen_width * .25, Playground.screen_width * .75))


# Objective: score into the goal post
def playingOffense(team_playing, selected_player, other_players):
    if team_playing is selected_player.team:
        # pass to other player or shoot
        if Playground.playerContact(selected_player):
            if random.randint(0, 101) < 40:
                pass_ball(selected_player, other_players)
            else:
                shoot(selected_player)
        return

    team_one = selected_player.team is SoccerTeamPlayers.Teams.TEAM_ONE
    bound = selected_player[0] > Playground.half_width if team_one else selected_player[0] < Playground.half_width
    # playingDefense(team_playing, selected_player, bound)


def robotMovement(team, players):  # TODO
    global team_one, team_two
    team_one = Playground.left_team
    team_two = Playground.right_team

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
