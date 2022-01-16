from enum import Enum
import keyboard
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
    DEFENSE = FORWARD = 3
    MIDDLE = 2


class FieldSide(Enum):
    LEFT_SIDE, RIGHT_SIDE = 0, 1


w, h = Playground.half_width, Playground.half_height


class StartPositionRight(Enum):
    # Initial position for right side team
    FORWARD = (w * 1.4, h)
    MIDDLE, MIDDLE_BACK = (w * 1.7, h), (w * 1.9, h)
    MIDDLE_LEFT, MIDDLE_RIGHT = (w * 1.6, h * .65), (w * 1.6, h * 1.15)
    # BACK_LEFT, BACK_LEFT_RIGHT = (w * 1, h // 2), (w * 3, h * 2)
    # BACK_RIGHT, BACK_RIGHT_LEFT = (w * 1.5, h * 2.5), (w * 1.5, h * 3 + 30)

    # BACK_TOP = (w * 1.5, h + 60)
    # BACK_BOTTOM = (w * 1.5, h - 60)


class StartPositionLeft(Enum):
    # Initial position for left side team
    FORWARD = (w * .6, h)
    MIDDLE, MIDDLE_BACK = (w * .5, h * 1.25), (w * .5, h * .75)
    MIDDLE_LEFT, MIDDLE_RIGHT = (w * .4, h * 1.35), (w * .4, h * 1.3)
    # BACK_LEFT, BACK_LEFT_RIGHT = (w // 1.15, h // 2), (w // 1.15, h * 2)
    # BACK_RIGHT, BACK_RIGHT_LEFT = (w // (1.15 * 2), h * 2.5), (w // (1.15 * 2), h * 3 + 30)

    # BACK_TOP = (w // (1.15 * 2), h + 60)
    # BACK_BOTTOM = (w // (1.15 * 2), h - 60)


# Creates one team (Max = 2)
class Team:
    def __init__(self, color, side):
        self.players = []
        self.color, self.side = color, FieldSide(side)  # Cast as FieldSide
        self.team = {StartPositionLeft: Teams.TEAM_ONE, StartPositionRight: Teams.TEAM_TWO}.get(side)
        self.numberOfPlayers = 5

        # Creates the number of players (initializes)
        for x in range(0, self.numberOfPlayers):
            self.players.append(Player(self.team, 1 + x, States.WAITING, StartPositionLeft.FORWARD))  # ?: Speed


class Player:
    def __init__(self, team, number, action, place):
        self.team = Teams(team)
        self.number = number
        self.action, self.place = States(action), place

    def switchPlayer(self):
        if keyboard.is_pressed(
                "Q" if self.team == Teams.TEAM_ONE else "/"):
            return  # closestPlayer(self)

    def strike(self):
        key, power = ' ' if self.team == Teams.TEAM_ONE else 'F', 0
        while keyboard.is_pressed(key):
            power += 1
        return power

    def controls(self):
        key = ("W", "S", "A", "D") if self.team == Teams.TEAM_ONE else \
            (pygame.K_UP, pygame.KEYDOWN, pygame.K_LEFT, pygame.K_RIGHT)

        # if not Gameplay.isOffField(self.place):
        #     if keyboard.is_pressed(key[0]):
        #         Player.moveUp(self)
        #     elif keyboard.is_pressed(key[1]):
        #         Player.moveDown(self)
        #     elif keyboard.is_pressed(key[2]):
        #         Player.moveLeft(self)
        #     elif keyboard.is_pressed(key[3]):
        #         Player.moveRight(self)

    def moveUp(self):
        return self.place[self.place[0]][self.place[1] + 1]

    def moveDown(self):
        return self.place[self.place[0]][self.place[1] - 1]

    def moveLeft(self):
        return self.place[self.place[0] - 1][self.place[1]]

    def moveRight(self):
        return self.place[self.place[0] + 1][self.place[1]]
