from Playground import *
from Constant import *
from abstractbrain import *
from physics import Circle


class Team:
    def __init__(self, team_num: Teams, player_color):
        self.team_number = Teams(team_num)
        self.brain = None
        self.side = starting_position.get(team_num)
        self.team_color = player_color

        # Adds to the list the new player, gets the initial value of the player
        # Uses same size, color and its specific position
        self.players = [Player(self.team_number, soccer_player.value, player_color)
                        for soccer_player in self.side]
        # Gets the correct circle and controls from the team side chosen
        num = {Teams.TEAM_ONE: p1_num, Teams.TEAM_TWO: p2_num}.get(self.team_number)
        self.user = User(self.team_number, self.players[num])

        # Removes the user from the player list
        self.players.remove(self.players[num])

    def applyMoveToAllPlayers(self, move: np.array):
        self.brain.last_move = []
        for i in range(len(move)):
            normal_move = self.players[i].apply_move(move[i])
            self.brain.last_move.append(normal_move)

    def resetPosition(self):
        for index in range(len(self.side)):
            self.players[index].position, self.players[index].velocity = list(self.side[index].value), [0, 0]

    def positionMatrix(self):  # creates a matrix of players positions
        return np.array([p.position for p in self.players])

    def velocityMatrix(self):  # creates a matrix of players velocity
        return np.array([p.velocity for p in self.players])


class Player(Circle):
    def __init__(self, team, position: list, p_color):
        super().__init__(position, p_color)
        self.team = team
        self.distanceToBall, self.closePlayers = -1, []

    def setDistanceToBall(self, new_distance):
        self.distanceToBall = new_distance

    def addClosePlayer(self, player):
        self.closePlayers.append(player)

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
        return self.position[0] > self.size - sides[0]

    def isRightBound(self) -> bool:
        return self.position[0] < screen_width - self.size

    def isUpperBound(self) -> bool:
        return self.position[1] > self.size + sides[1]

    def isLowerBound(self) -> bool:
        return self.position[1] < screen_height - self.size


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


class User(CheckUsersMovement, Player):
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


class CheckBallMovement(CheckMovement):
    def __int__(self):
        spacing = 50
        self.insideGoal: bool = self.position[1] in range(half_screen - spacing, half_screen + spacing)

    def moveLeft(self):
        return self.isLeftBound() and self.insideGoal

    def moveRight(self):
        return self.isRightBound() and self.insideGoal
