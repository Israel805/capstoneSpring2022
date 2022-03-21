from Playground import *
from AI import distance
from Constant import *

from abstractbrain import *


class Team:
    def __init__(self, team_num, player_color, homeGoal, opponent_Goal):
        self.team_number = Teams(team_num)
        self.brain = None
        self.state = States.WAITING
        self.side = starting_position.get(team_num)
        self.team_color = player_color
        self.ownGoal, self.scoringGoal = homeGoal, opponent_Goal

        # Adds to the list the new player, gets the initial value of the player
        # Uses same size, color and its specific position
        self.players = [Player(self.team_number, soccer_player.value, player_color, homeGoal, opponent_Goal)
                        for soccer_player in self.side]

    def applyMoveToAllPlayers(self, move: np.array):
        self.brain.last_move = []
        for i in range(len(move)):
            normal_move = self.players[i].apply_move(move[i])
            self.brain.last_move.append(normal_move)

    def setState(self, state):  # other way to set all players to be the same state
        # Sets the global state of the whole team
        self.state = state
        [self.players[i].setState(state) for i in range(len(self.players))]

    def resetPosition(self):
        index = 0
        for default_pos in self.side:
            self.players[index].position = list(default_pos.value)
            self.players[index].velocity = 0
            index += 1

    def positionMatrix(self):  # creates a matrix of players positions
        return np.array([p.position for p in self.players])

    def velocityMatrix(self):  # creates a matrix of players velocity
        return np.array([p.velocity for p in self.players])

    def changeStateForTeam(self):
        state = States.ATTACKING if self.state is States.DEFENDING else States.DEFENDING
        self.setState(state)

    def ballWithinRangeForInterception(self) -> bool:
        return distance(self.ownGoal, ball) < interceptionRange


class Player(Circle):
    def __init__(self, team, position, p_color, homeGoal, opponent_Goal):
        super().__init__(position, p_color)
        self.team = team
        self.max_speed = self.velocity * 1.5
        self.state = States.WAITING
        self.distanceToBall, self.closePlayers = -1, []
        self.ownGoal, self.scoringGoal = homeGoal, opponent_Goal

    def getGoalCenter(self):
        return self.scoringGoal.getGoalCenter()

    def setState(self, new_state):
        self.state = new_state

    def kick(self, velocity=vel):  # adds a velocity to the object to move it
        self.velocity = np.add(self.velocity, velocity)

    def setDistanceToBall(self, new_distance):
        self.distanceToBall = new_distance

    def addClosePlayer(self, player):
        self.closePlayers.append(player)

    def isSafeToReceive(self) -> bool:
        length = len(self.closePlayers)
        # if length of the list of close players is empty
        if length == 0:
            return True
        for x in range(length):
            if self.closePlayers[x].team is not self.team:
                return False
        return True

    # def update(self):
    def pressBall(self):
        temp = distance(self, ball.position) < 10
        self.velocity *= (1.2 if temp else 1.6)

    def changeStateForPlayer(self):
        state = States.ATTACKING if self.state is States.DEFENDING else States.DEFENDING
        self.setState(state)

    def apply_move(self, move: np.array):
        norm = np.linalg.norm(move)
        normal_move = move / norm if norm > 1 else move

        self.apply_acceleration(normal_move)
        return normal_move


# For player and AI use
class CheckMovement:
    def __init__(self, position: list, size: int):
        self.position, self.size = position, size

    def isLeftBound(self) -> bool:
        goal_post = goal_posts[0]  # Assume both is the same vertical range
        return self.position[1] not in range(goal_post.getLeftSide(), goal_post.getRightSide()) \
               and self.position[0] > self.size

    def isRightBound(self) -> bool:
        goal_post = goal_posts[0]  # Assume both is the same vertical range
        return self.position[1] not in range(goal_post.getLeftSide(), goal_post.getRightSide()) and \
               self.position[0] < screen_width - self.size

    def isUpperBound(self) -> bool:
        return self.position[1] > self.size + sides[1]

    def isLowerBound(self) -> bool:
        return self.position[1] < screen_height - self.size


class CheckAIMovement(CheckMovement):
    def __init__(self, position: list, size):
        super().__init__(position, size)

    def moveLeft(self):
        if self.isLeftBound():
            self.position[0] -= vel

    def moveRight(self):
        if self.isRightBound():
            self.position[0] += vel

    def moveUp(self):
        if self.isUpperBound():
            self.position[1] -= vel

    def moveDown(self):
        if self.isLowerBound():
            self.position[1] += vel


class CheckUsersMovement(CheckMovement):
    def __init__(self, team, player):
        super().__init__(player.position, player.size)
        self.keys, self.velocity = pygame.key.get_pressed(), vel
        self.player_key = player_control.get(team)

    def moveLeft(self):
        if self.keys[self.player_key[0]] and self.isLeftBound():
            self.position[0] -= self.velocity

    def moveRight(self):
        if self.keys[self.player_key[1]] and self.isRightBound():
            self.position[0] += self.velocity

    def moveUp(self):
        if self.keys[self.player_key[2]] and self.isUpperBound():
            self.position[1] -= self.velocity

    def moveDown(self):
        if self.keys[self.player_key[3]] and self.isLowerBound():
            self.position[1] += self.velocity


class User(CheckUsersMovement):
    def __init__(self, team, player):
        super().__init__(team, player)

    def moveAllDirections(self):
        # The outer circle doesnt touch the left side, increment in x coordinate
        self.moveLeft()
        # Only to the right of the screen, decrement in x coordinate
        self.moveRight()
        # If below the scoreboard, increment in y coordinate
        self.moveUp()
        # if down arrow key is pressed, decrement in y coordinate
        self.moveDown()
