from enum import Enum

import pygame

import Playground


class Teams(Enum):
    TEAM_ONE, TEAM_TWO = 0, 1


class States(Enum):
    WAITING = 0
    DEFENDING = 1
    ATTACKING = 2
    ASSISTING = 3


class MovingPosition(Enum):
    DEFENSE = 3
    MIDDLE = FORWARD = 2


class FieldSide(Enum):
    LEFT_SIDE, RIGHT_SIDE = 0, 1


w, h = Playground.half_width, Playground.half_height


class StartPositionRight(Enum):
    # Initial position for right side team
    FORWARD = (w * 1.4, h)
    MIDDLE, MIDDLE_BACK = (w * 1.7, h * .4), (w * 1.9, h)
    SIDE_LEFT, SIDE_RIGHT = (w * 1.6, h * .8), (w * 1.6, h * 1.5)
    BACK_LEFT, BACK_RIGHT = (w * 1.9, h * .5), (w * 1.8, h * .8)


class StartPositionLeft(Enum):
    # Initial position for left side team
    FORWARD = (w * .6, h)
    MIDDLE, MIDDLE_BACK = (w * .5, h * 1.25), (w * .5, h * .75)
    SIDE_LEFT, SIDE_RIGHT = (w * .5, h), (w * .4, h * 1.6)
    BACK_LEFT, BACK_RIGHT = (w * .2, h * .6), (w * .2, h * 1.2)


class Team:
    def __init__(self, team_num, player_color):
        self.team_number = Teams(team_num)
        self.side = {Teams.TEAM_ONE: StartPositionLeft,
                     Teams.TEAM_TWO: StartPositionRight}.get(team_num)
        self.team_color = player_color

        # Adds to the list the new player
        # Gets the initial value of the player
        # Uses same size, color and its specific position
        self.players = [Player(self.team_number, soccer_player.value, player_color)
                        for soccer_player in self.side]


class Player(Playground.Circle):
    def __init__(self, team, position, circle_color):
        super().__init__(position, circle_color)
        self.team = team


# For player and AI use
class CheckMovement:
    def __init__(self, position, size):
        self.position, self.size = position, size

    def isLeftBound(self):
        return self.position[0] > self.size

    def isRightBound(self):
        return self.position[0] < Playground.screen_width - self.size

    def isUpperBound(self):
        return self.position[1] > 75 + self.size

    def isLowerBound(self):
        return self.position[1] < Playground.screen_height - self.size


class CheckUsersMovement(CheckMovement):
    def __init__(self, team, player):
        super().__init__(player.position, player.size)
        self.keys, self.velocity = pygame.key.get_pressed(), Playground.vel
        soccer = Teams
        self.player_key = {
            soccer.TEAM_ONE: [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s],
            soccer.TEAM_TWO: [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]
        }.get(team)

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