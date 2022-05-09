from random import random

import numpy as np
from pygame import *

# General setup
from SoccerTeamPlayers import Team
from Brain import Brain, updates
from Constant import *
from brains.DefendersAndAttackers import DefendersAndAttackers
from physics import Circle


class Ball(Circle):
    def __init__(self, position: list, circle_color):
        super().__init__(position, circle_color, ball_size)

    def rest(self):  # resets the ball to the original position (center of the screen)
        self.position, self.velocity = np.array(half_screen), np.array([0, 0])

    def initialize(self):  # Initialize the ball to move slightly
        self.velocity = np.array([random() - 0.5, random() - 0.5])


class GoalPost:
    def __init__(self, goal_line: tuple, circle_color, number: int):
        # Assigns the color, and the team associated to the goal
        self.color, self.goal_number = circle_color, number

        # Creates the Rectangle object
        self.object = pygame.Rect(goal_line, goal_size)

    def draw(self):  # Draws a rectangle
        pygame.draw.rect(screen, self.color, self.object)

    def isScored(self):
        global left_team, right_team, ball
        x, y = ball.position

        def insideGoal():
            return self.object.top < y < self.object.bottom

        # Checks if the x, y positions are within the goal
        if insideGoal() and (x < sides[0] + 20 or x > screen_width - sides[0] - 20):
            # Increments the score
            score[self.goal_number] += 1
            ball.rest()  # Resets the ball position

            # Goes though each team and player to return to their original position
            [team.resetPosition() for team in [left_team, right_team]]

            # Initialize the ball to move slightly
            ball.initialize()
            return True
        return False


# ! Draws the goal post on both sides on the field
goal_posts = [GoalPost((goal_xpos * .2, goal_ypos), WHITE, 0),
              GoalPost((screen_width - (goal_xpos * .8) - 3, goal_ypos), WHITE, 1)]

# The primary ball to score on
ball = Ball(half_screen, RED)

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
        [[player.draw() for player in player_side] for player_side in [left_team.players, right_team.players]]

        # Draws the user on both teams
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
        # Displays the time for the Game, in minutes and seconds
        mins, sec = str(counter // 60), counter % 60
        sec = ('0' if sec < 10 else '') + str(sec)
        screen.blit(default_label("Time: " + mins + ":" + sec), (50, 20))

    def displayGoalSides():
        # Draws the lines parallel to the goal
        goal_line_vert, shift = 20, 8
        goal_side1, goal_side2 = [goal_line_vert - shift, line_pos], [goal_line_vert - shift, screen_width]
        pygame.draw.aaline(screen, WHITE, goal_side1, goal_side2)

        # Makes the first element in each list the inverse of the whole screen width
        goal_side1[0] = goal_side2[0] = screen_width - goal_line_vert + shift
        pygame.draw.aaline(screen, WHITE, goal_side1, goal_side2)

    def displayField():
        # Draws a vertical line in the middle of the screen
        pygame.draw.aaline(screen, WHITE, (half_width, line_pos), (half_width, screen_width))

        # Draws a horizontal line in the middle (top) of the screen
        start_pos, end_pos = [0, line_pos], [screen_width, line_pos]
        pygame.draw.aaline(screen, WHITE, start_pos, end_pos)

        start_pos[1] = end_pos[1] = screen_height
        pygame.draw.aaline(screen, WHITE, start_pos, end_pos)

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


def getAllCircles():
    circles = []
    # Collects all the players on both teams, adds to the list
    [[circles.append(player) for player in player_side] for player_side in [left_team.players, right_team.players]]

    # Adds the users to the update
    [circles.append(users) for users in [left_team.user, right_team.user]]

    # Finally adds the ball to the list at the end
    circles.append(ball)
    return circles


def AIController():
    global left_team, right_team
    brain = Brain(left_team, right_team, ball)
    brain.run_brains()
    brain.limit_velocities()


def MainFunction():
    global left_team, right_team, vel

    # Creates a boost for the each player's velocity
    if pygame.key.get_pressed()[K_COLON] or pygame.key.get_pressed()[K_q]:
        vel = vel * 1.25

    # Controller for player 1
    left_team.user.moveAllDirections()

    # Controller for player 2
    right_team.user.moveAllDirections()

    # Check if the ball is in the goal
    for x in range(len(goal_posts)):
        if goal_posts[x].isScored():
            return

    AIController()

    updates(getAllCircles())


def MainGame():
    global left_team, right_team, counter
    while True:

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
            # GameResult()  # not working
            return

        # Visuals
        screen.fill(PAGE_COLOR)
        Layout()

        # ! Updating the window
        pygame.display.flip()
        pygame.display.update()
        clock.tick(60)


def initializeGame(player1_color, player2_color, ball_color, time_option):
    global left_team, right_team, ball, counter
    # ! Creates the players on the screen
    # Displays the players on the screen for Both Side

    # Saves and displays the players on both sides
    left_team = Team(Teams.TEAM_ONE, player1_color)
    right_team = Team(Teams.TEAM_TWO, player2_color)

    # Creates a game tactic where the AI can play with
    left_team.brain = right_team.brain = DefendersAndAttackers(ball)

    # Saves the color of the ball and the time clock
    ball.color, counter = ball_color, time_option

    ball.initialize()


def Main(colors: list, ball_color, time_option):
    initializeGame(colors[0], colors[1], ball_color, time_option)
    MainGame()
