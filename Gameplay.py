import pygame
import math
import keyboard
from enum import Enum
from random import random

import ScreenCreation

totalNumberOfPlayers = 5 if ScreenCreation.width == 800 and ScreenCreation.height == 400 else 2
TEAM_ONE = 0
TEAM_TWO = 1


class States(Enum):
    DEFENDING = 0
    ATTACKING = 1
    ASSISTING = 2
    WAITING = 3


def assignStateToPlayer(player1, player2):
    # This should be overview of what each team should try to know
    # Whether they are 

    player2 = States.DEFENDING if player1 == States.ATTACKING else States.ATTACKING
    # Set 3 - 4 players for player1 to state assist
    # call to defend or attack

    player1 = player1 = States.DEFENDING if player2 == States.ATTACKING else States.ATTACKING
    # Set 3 - 4 players for player2 to state assist


def probability(percent):
    return random.random() <= float(percent)


def isOffField(currentPos, size):
    return currentPos > math.sqrt(size)


def isGoal(currentPos, goalPostPosition):
    return goalPostPosition[0] < currentPos < goalPostPosition[1]


def isOpponentsBall(currentPos, goalPostPosition, size):
    return not isGoal(currentPos, goalPostPosition) and currentPos < math.sqrt(size)


def powerStrike():
    power = 0

    isPlayer1 = keyboard.is_pressed(' ')

    # use space with duration to determine power
    if isPlayer1:
        while keyboard.is_pressed(' '):
            power += 1

    # use 'F' with duration to determine power
    isPlayer2 = keyboard.is_pressed('F')

    if isPlayer2:
        while keyboard.is_pressed('F'):
            power += 1

    return power


'''''
After ball is out of bound, ball is given to the closest team side
def refGivesBall(ballPos):
if ballPos < 0:
ball position is given to the left side
'''''

player = [[]] * 2
player01 = 0
player02 = 0


# NEEDS WORK! All code here is from scratch, could use some touch up
def moveUp():
    pygame.mouse.set_pos(pygame.mouse.get_pos() + 1)


def moveDown():
    pos = pygame.mouse.get_pos()
    pygame.mouse.set_pos(pos - 1 if int(pos) < ScreenCreation.screen_size else 0)


def moveLeft():
    pygame.mouse.set_pos(pygame.mouse.get_pos() + 1)  # horizontally


def moveRight():
    pygame.mouse.set_pos(pygame.mouse.get_pos() + 1)  # horizontally


# def gameTime():
#     global timeLeft
#     if timeLeft <= 0:
#         return False
#     timeLeft -= 1
#     timelabel.config(text="Time Left: " + str(timeLeft))
#     timelabel.after(1000, countdown)
#     pass


def drawCircle():
    pass


def player1Controls():
    if keyboard.is_pressed("W"):
        moveUp()
    elif keyboard.is_pressed("S"):
        moveDown()
    elif keyboard.is_pressed("A"):
        moveLeft()
    elif keyboard.is_pressed("D"):
        moveRight()


def findBall():
    return


def closestPlayer(team):
    ballsPos = findBall()

    player01 = closestPlayer(ballsPos)

    # find any near by players near the ball
    closest = ballsPos - player[team][0]

    for x in range(1, totalNumberOfPlayers):
        # find the difference and compare to the ball
        if (ballsPos - player[team][x]) < closest:
            closest = player[x]

    return closest


def player1SwitchPlayer():
    # finds the closest player from TEAM_ONE
    if keyboard.is_pressed("Q"):
        player01 = closestPlayer(TEAM_ONE)


def player2SwitchPlayer():
    # finds the closest player from TEAM_TWO
    if keyboard.is_pressed("/"):
        player02 = closestPlayer(TEAM_TWO)


def player2Controls():
    if keyboard.is_pressed(pygame.KEYDOWN):
        if keyboard.is_pressed(pygame.K_UP):
            moveUp()
        elif keyboard.is_pressed(pygame.K_DOWN):
            moveDown()
        elif keyboard.is_pressed(pygame.K_LEFT):
            moveLeft()
        elif keyboard.is_pressed(pygame.K_RIGHT):
            moveRight()


def outline():
    global running
    while running:
        ev = pygame.event.get()

        for event in ev:
            if event.type == pygame.MOUSEBUTTONUP:
                drawCircle()
                pygame.display.update()

            if event.type == pygame.QUIT:
                running = False


def displayScoreBoard(screen, score_board):
    new_txt = ScreenCreation.ScreenDetails(screen, score_board[0], 0, ScreenCreation.BLACK, (50, 50))
    ScreenCreation.createTextToScreen(new_txt)

    new_txt.string = ' - '
    ScreenCreation.createTextToScreen(new_txt)

    new_txt.string = score_board[1]
    ScreenCreation.createTextToScreen(new_txt)


def main():
    score = [0, 0]
    # play()

    # initializing imported module
    pygame.init()
    # Displaying a window of width and height
    screen = ScreenCreation.createScreen('Soccer Game', ScreenCreation.WHITE)
    displayScoreBoard(screen, score)


    # Creating a bool value which checks if
    # game is running
    running = True

    # Keep game running till running is true
    while running:

        # Check for event if user has pushed
        # any event in queue
        for event in pygame.event.get():

            # If event is of type quit then set
            # running bool to false
            if event.type == pygame.QUIT:
                running = False

    pygame.display.update()


if __name__ == '__main__':
    main()
