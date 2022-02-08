import random
from math import sqrt
from pygame import *
import Playground
import SoccerTeamPlayers
import AI


def shoot(player):
    left_side = player.team is SoccerTeamPlayers.Teams.TEAM_ONE
    res = K_SPACE if left_side else K_x

    AI.getAvailableSpots()
    opponentsGoalPost = player.scoringGoal
    # Finds how many spots the ball can fit in order to score correctly
    numAttempts = opponentsGoalPost.getLen() // (Playground.ball_size * 2)
    while numAttempts > 0:
        target = list(opponentsGoalPost.getGoalCenter())
        # pushes the ball to either side to make it 'shoot' in the goal
        the_ball = Playground.ball
        # Randomizes between the space available to score in the opponents goal
        minYValue = maxYValue = (-1 if left_side else -1)
        minYValue *= opponentsGoalPost.getLeftSide() + the_ball.getSize()
        maxYValue *= opponentsGoalPost.getRightSide() - the_ball.getSize()
        target[1] = random.randint(minYValue, maxYValue)
        numAttempts -= 1

    # if pygame.key.get_pressed()[res] and playerContact(player) and inBounds(the_ball):


# From both teams, will determine who exactly is the closest
def closestToBall():
    closest_to_the_ball = None

    for player in [teams for teams in [Playground.left_team, Playground.right_team]]:
        # calculate the dist,using squared value
        dist = AI.distance(player, Playground.ball) ** 2

        # Records the distance for each player
        player.setDistanceToBall(dist)

        if closest_to_the_ball is None or dist < closest_to_the_ball:
            closest_to_the_ball = player
    # returns who is actually the closest
    return closest_to_the_ball


def bestSupportAttacker():
    closest = bestPlayer = None

    # Already know that the first two are the attackers(strikers)
    # for num in range(SoccerTeamPlayers.MovingPosition.FORWARD.value):
    #     if team_one[num]:


def TimeCoverDistance(pos1, pos2, force):
    # the velocity of the ball in the next time step *if*
    #  the player was to make the pass.
    speed = force / 4

    # calculate s (the distance between the two positions)
    coveredDist = AI.distance(pos1, pos2)
    term = speed ** 2 + float(2 * coveredDist * AI.friction)

    # it IS possible for the ball to reach B and we know its speed when it
    #   gets there, so now it's easy to calculate the time using the equation
    return -1 if term <= 0.0 else ((sqrt(term) - speed) / AI.friction)


def getBestPassToReceive(current_player, player, target, power):
    time = TimeCoverDistance(Playground.ball.position, player.position, power)

    if time < 0: return False

    interceptRange = time * player.max_speed
    interceptRange *= 0.3  # scalar factor
    interceptPoint1 = interceptPoint2 = []
    AI.getTangentPoints(player.position, interceptRange, Playground.ball.position, )


def pass_ball(p1, p_n):
    def getClosestPlayer(current_player, receiver, passTarget, power, minPassDistance):
        closestToGoal = target = None
        # Looks for each player in their team to pass to
        team = Playground.left_team if current_player.teams is SoccerTeamPlayers.Teams.TEAM_ONE else Playground.left_team
        for player in team:
            if player is not current_player and \
                    AI.distance(current_player, player) > minPassDistance ** 2:
                if getBestPassToReceive(current_player, player, target, power):

                    distanceToGoal = abs(target[0] - current_player.getGoalCenter()[0])
                    if closestToGoal is None or distanceToGoal < closestToGoal:
                        closestToGoal = distanceToGoal
                        receiver = player
                        passTarget = target

        return False if receiver is None else True

        # return closestToGoal

    # if playerContact(p1):
    #     move(Playground.ball, getClosestPlayer(p_n, p1))
