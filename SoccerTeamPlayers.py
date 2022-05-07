from Constant import *
from abstractbrain import *
from physics import Circle


class Team:
    def __init__(self, team_num: Teams, player_color):
        self.team_number, self.team_color = team_num, player_color
        self.brain = None
        self.side = starting_position.get(team_num)

        # Adds to the list the new player, gets the initial value of the player
        # Uses same size, color and its specific position
        self.players = [Player(soccer_player, player_color) for soccer_player in self.side]

        # Gets the correct circle and controls from the team side chosen
        num = {Teams.TEAM_ONE: p1_num, Teams.TEAM_TWO: p2_num}.get(self.team_number)
        self.user = User(self.team_number, self.players[num], player_color)

        self.user_position = self.players[num].position

        # Removes the user from the player list
        self.players.remove(self.players[num])
        self.side.remove(self.side[num])

    def applyMoveToAllPlayers(self, move: np.array):
        self.brain.last_move = []
        for i in range(len(move)):
            normal_move = self.players[i].apply_move(move[i])
            self.brain.last_move.append(normal_move)

    def resetPosition(self):
        # Resets all players position
        for index in range(len(self.side)):
            self.players[index].position = np.array(self.side[index])

        # Reset user's positions
        self.user.position = self.user_position

    def positionMatrix(self):  # creates a matrix of players positions
        return np.array([p.position for p in self.players])

    def velocityMatrix(self):  # creates a matrix of players velocity
        return np.array([p.velocity for p in self.players])


class Player(Circle):
    def __init__(self, position: list, p_color):
        super().__init__(position, p_color)

    def apply_move(self, move: np.array):
        norm = np.linalg.norm(move)
        normal_move = move / norm if norm > 1 else move
        self.apply_acceleration(normal_move)
        return normal_move


# For player use
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
        self.velocity = [user_velocity, user_velocity]
        self.player_key = player_control.get(team)

    def moveLeft(self):
        if pygame.key.get_pressed()[self.player_key[0]] and self.isLeftBound():
            self.position[0] -= user_velocity

    def moveRight(self):
        if pygame.key.get_pressed()[self.player_key[1]] and self.isRightBound():
            self.position[0] += user_velocity

    def moveUp(self):
        if pygame.key.get_pressed()[self.player_key[2]] and self.isUpperBound():
            self.position[1] -= user_velocity

    def moveDown(self):
        if pygame.key.get_pressed()[self.player_key[3]] and self.isLowerBound():
            self.position[1] += user_velocity


class User(CheckUsersMovement, Player):
    def __init__(self, team, player, user_color):
        super().__init__(team, player)
        self.color = user_color

    def moveAllDirections(self):
        # The outer circle doesnt touch the left side, increment in x coordinate
        self.moveLeft()
        # Only to the right of the screen, decrement in x coordinate
        self.moveRight()
        # If below the scoreboard, increment in y coordinate
        self.moveUp()
        # if down arrow key is pressed, decrement in y coordinate
        self.moveDown()
