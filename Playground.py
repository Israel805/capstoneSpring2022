import sys
from random import random

import numpy as np
from pygame import *

# General setup
import SoccerTeamPlayers
from Brain import Brain, updates
from Constant import *
from brains.DefendersAndAttackers import DefendersAndAttackers
# Draws a circle on the screen
from physics import Circle


class Ball(Circle):
    def __init__(self, position, circle_color, circle_size):
        super().__init__(position, circle_color, circle_size)

    def placeAndRestBall(self, new_position):
        self.position, self.velocity = new_position, [0, 0]

    def setHorizontalMovement(self, change):
        self.position[0] += change

    def setVerticalMovement(self, change):
        self.position[1] += change


class GoalPost:
    def __init__(self, goal_line, circle_color, number):
        self.color, self.goal_number = circle_color, number
        self.object = pygame.Rect(list(goal_line), goal_size)

    def getGoalCenter(self):
        return self.object.center

    def getLeftSide(self):
        return self.object.top if bool(self.goal_number) else self.object.bottom

    def getRightSide(self):
        return self.object.top if not bool(self.goal_number) else self.object.bottom

    def draw(self):
        pygame.draw.rect(screen, self.color, self.object)

    def insideGoal(self):
        return self.object.top < ball.position[1] < self.object.bottom

    def isScored(self):

        def resetAllPositions():
            global left_team, right_team
            ball.placeAndRestBall([half_width, half_height])

            # Goes though each team and player to return to their original position
            for team in [left_team, right_team]:
                team.resetPosition()
                team.setState(SoccerTeamPlayers.States.WAITING)

        # if self.object.collidepoint(ball.position):
        x, y = ball.position
        if (x < sides[0] or x > screen_width - sides[0]) and self.insideGoal():
            score[self.goal_number] += 1
            resetAllPositions()


# ! Draws the goal post on both sides on the field
goal_posts = [GoalPost((goal_xpos * .2, goal_ypos), WHITE, 0), GoalPost((screen_width -
                                                                         (goal_xpos * .8) - 3, goal_ypos), WHITE, 1)]
# The primary ball to score on
ball = Ball(half_screen, RED, ball_size)

''' Start of Display Functions '''


def scoreFinal():
    global score
    score_position = player_pos = [20, half_height]
    score_position[1] *= 1.05

    # Displays the score sheet on the top of the screen
    screen.blit(default_label(P1, 200), player_pos)
    player_pos[0] = screen_width - player_pos[0]
    screen.blit(default_label(P2, 200), player_pos)

    for player_score in [str(score[0]), "-", str(score[1])]:
        screen.blit(default_label(player_score, 200), score_position)


def chooseWinner():
    # Determines a winner or a draw for the final income
    title_position = [half_width, 50]
    if score[0] == score[0]:
        screen.blit(default_label("Draw", 200), title_position)
    else:
        screen.blit(default_label("Winner", 200), title_position)
        title_position[1] += 100
        screen.blit(default_label(P1 if score[0] > score[1] else P2, 300), title_position)

    scoreFinal()


def Layout():
    global left_team, right_team, goal_posts

    def displayGoalAndPlayers():
        # ! Draws the goal post, left and right players
        [goal.draw() for goal in goal_posts]

        # Draws each player on both teams
        for player_side in [left_team.players, right_team.players]:
            [player.draw() for player in player_side]

        [user_side.draw() for user_side in [left_team.user, right_team.user]]

    def displayScore():
        # ! Update scores
        # Displays the score board for both teams
        display_setup = [P1, str(score[0]), "-", str(score[1]), P2]
        spacing, position = [200, 25, 25, 125, 0], [half_width - 200, 20]
        index = 0
        for score_setup in display_setup:
            screen.blit(default_label(score_setup), position)
            position[0] += spacing[index]
            index += 1

    def displayTime():
        # Displays the time for the Game
        mins, sec = str(counter // 60), counter % 60
        sec = ('0' if sec < 10 else '') + str(sec)
        screen.blit(default_label("Time: " + mins + ":" + sec), (50, 20))

    def displayGoalSides():
        # Appends the walls from both ends

        # Draws the lines parallel to the goal
        goal_line_vert, shift = 20, 8
        goal_side1, goal_side2 = [goal_line_vert - shift, line_pos], [goal_line_vert - shift, screen_width]
        walls.append(pygame.draw.aaline(screen, WHITE, goal_side1, goal_side2))

        # Makes the first element in each list the inverse of the whole screen width
        goal_side1[0] = goal_side2[0] = screen_width - goal_line_vert + shift
        walls.append(pygame.draw.aaline(screen, WHITE, goal_side1, goal_side2))

    def displayField():
        # Draws a vertical line in the middle of the screen
        pygame.draw.aaline(screen, WHITE, (half_width, line_pos), (half_width, screen_width))

        # Draws a horizontal line in the middle (top) of the screen
        start_pos, end_pos = [0, line_pos], [screen_width, line_pos]
        new_wall = pygame.draw.aaline(screen, WHITE, start_pos, end_pos)
        walls.append(new_wall)
        start_pos[1] = end_pos[1] = screen_height
        new_wall = pygame.draw.aaline(screen, WHITE, start_pos, end_pos)
        walls.append(new_wall)

        # Draws the circle of the field
        Circle(half_screen, WHITE, 200).draw(3)

    global ball
    line_pos = 75
    displayGoalAndPlayers()
    displayField()
    displayGoalSides()
    displayTime()
    displayScore()

    # ! Red ball in the center
    ball.draw()


''' End of all display functions '''

''' All Page Functions'''


def GameResult():
    screen.fill(PAGE_COLOR)  # Clears the screen
    chooseWinner()
    # Creates a new button for the start button
    button_pos = [half_width * .85, screen_height - 145]
    button = pygame.Rect(button_pos, button_size)

    while True:
        # If clicked on the button, it will start the game
        if isPressed(button):
            return

        # Draws the rectangle button
        pygame.draw.rect(screen, WHITE, button)
        # Creates a text to go with the button
        play_label = default_label("Continue", font_color=BLACK)
        button_pos[0] = half_width * .95
        screen.blit(play_label, button_pos)


''' End of All Page Functions'''


def playerContact(circle_player):
    # Distance of the centers, radius of both circles
    return distance(circle_player, ball) <= ball_size * 2


# Mode where ball would move if only touched by a player
def touchBallMode():
    def getHit(circle_player):
        # If any player collides with the ball push the ball with its velocity
        arr = direction(circle_player, ball)
        for i in range(len(arr)):
            if arr[i] > 1:
                arr[i] = 1

            if arr[i] < -1:
                arr[i] = -1

        return [vel * arr[x] for x in range(len(arr))] if playerContact(circle_player) else [0, 0]

    for player_side in [left_team.players, right_team.players]:
        for player in player_side:
            a, b = getHit(player)  # Checks if in bounds for both x, y coordinates for both teams
            check = SoccerTeamPlayers.CheckMovement(player.position, player_size)
            checkLeft, checkRight = check.isLeftBound(), check.isRightBound()
            checkUp, checkDown = check.isUpperBound(), check.isLowerBound()

            # if it hits the outer bounds it will stop from moving after it hits the bounds
            ball.setHorizontalMovement(a * (-1 if not (checkLeft and checkRight) else 1))
            ball.setVerticalMovement(b * (-1 if not (checkUp and checkRight) else 1))


def getAllCircles():
    circles = []
    for player_side in [left_team.players, right_team.players]:
        [circles.append(player) for player in player_side]
    circles.append(ball)
    return circles


def MainFunction():
    global ball, vel

    # Creates a boost for the each player's velocity
    if pygame.key.get_pressed()[K_COLON] or pygame.key.get_pressed()[K_q]:
        vel = vel * 1.25

    # Controller for player 1
    #left_team.user.moveAllDirections()

    # Controller for player 2
    #right_team.user.moveAllDirections()

    # Check if the ball is in the goal
    [goal_posts[x].isScored() for x in range(len(goal_posts))]

    brain = Brain(left_team, right_team, ball)
    brain.run_brains()
    brain.limit_velocities()
    updates(getAllCircles())

    # # Calculates collision for player 1 and the ball
    left_team.user.calculate_collision(ball)
    #
    # # Calculates collision for player 2 and the ball
    right_team.user.calculate_collision(ball)


def MainGame():
    global left_team, right_team, counter
    while True:

        # Creates a game tactic where the AI can play with
        left_team.brain = right_team.brain = DefendersAndAttackers(ball)

        # Handling input
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                counter -= 1

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        MainFunction()

        if counter == 0:
            screen.fill(PAGE_COLOR)  # Clears the screen
            screen.blit(default_label("GAME OVER!", 100), half_screen)
            # GameResult() # not working
            return

        # Visuals
        screen.fill(PAGE_COLOR)
        Layout()

        # ! Updating the window
        pygame.display.flip()
        pygame.display.update()
        clock.tick(60)


def initializeTeams(player1_color, player2_color, ball_color, time_option):
    global left_team, right_team, ball, counter
    # ! Creates the players on the screen
    # Displays the players on the screen for Both Side
    # Saves and displays the players on both sides
    teams = SoccerTeamPlayers.Teams
    left_team = SoccerTeamPlayers.Team(teams.TEAM_ONE, player1_color)
    right_team = SoccerTeamPlayers.Team(teams.TEAM_TWO, player2_color)

    ball.color = ball_color
    counter = time_option

    ball.velocity = np.array([random() - 0.5, random() - 0.5])


def Main(colors: list, ball_color, time_option):
    initializeTeams(colors[0], colors[1], ball_color, time_option)
    MainGame()
