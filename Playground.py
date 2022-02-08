import pygame
import sys
from pygame import *
# General setup
import SoccerTeamPlayers
from AI import direction, robotMovement, inBounds, distance

WHITE = (255, 255, 255)
PAGE_COLOR = BLACK = (0, 0, 0)
LIGHT_GREY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
playersOption = [LIGHT_GREY, RED, GREEN, WHITE, BLACK]

# Creates a new pygame
pygame.init()

# Creates a new clock timer
clock = pygame.time.Clock()
pygame.time.set_timer(pygame.USEREVENT, 1000)
MINS = 5
counter = 60 * MINS  # 5 mins

left_team = right_team = 0
walls = []


# Creates a label with default font or custom size
def default_label(string, font_size=50, font_color=WHITE):
    default_font = pygame.font.SysFont("Comic Sans MS", int(font_size))
    return default_font.render(str(string), True, font_color)


'''
Trying to work the layout of the game
Looks like this is a good idea of the digital layout
Problem: how to move the ball with player, then AI
'''

# ! Setting up the main window
screen_width, screen_height = 1080, 768
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Soccer Pong Game')

# Creates global variables
score, vel = [0, 0], 5
half_screen = half_width, half_height = screen_width // 2, screen_height // 2
button_size, ball_size, player_size = [150, 50], 20, 25
p1_num = p2_num = 0


# Draws a circle on the screen
class Circle:
    def __init__(self, position, circle_color, circle_size=player_size):
        self.position = list(position)
        self.color, self.size = circle_color, circle_size
        self.velocity = vel

    def getLocation(self):
        return self.position

    def draw(self, size=0):  # Additional size
        return pygame.draw.circle(screen, self.color, self.position, self.size, size)


def playerContact(circle_player):
    # Distance of the centers, radius of both circles
    return distance(circle_player, ball) <= ball_size * 2


class Ball(Circle):
    def __init__(self, position, circle_color, circle_size):
        super().__init__(position, circle_color, circle_size)

    def getSize(self):
        return self.size

    def placeAndRestBall(self, new_position):
        self.position, self.velocity = new_position, 0

    def setHorizontalMovement(self, change):
        self.position[0] += change

    def setVerticalMovement(self, change):
        self.position[1] += change


class GoalPost:
    def __init__(self, goal_line, circle_color, number):
        self.color, self.goal_number = circle_color, number
        self.goal_size = [10, 150]
        self.object = pygame.Rect(list(goal_line), self.goal_size)

    def getLen(self):
        return self.goal_size[1]

    def getGoalCenter(self):
        return self.object.center

    def getLeftSide(self):
        return self.object.top if bool(self.goal_number) else self.object.bottom

    def getRightSide(self):
        return self.object.top if not bool(self.goal_number) else self.object.bottom

    def draw(self):
        pygame.draw.rect(screen, self.color, self.object)

    def isScored(self):
        if self.object.collidepoint(ball.position):
            score[self.goal_number] += 1
            resetAllPositions()


# Creates both circles for the intro, the initial choice
player1 = Circle((half_width * .35, screen_height * .6), WHITE)
player2 = Circle((screen_width * .8, screen_height * .6), GREEN)

# ! Draws the goal post on both sides on the field
goal_xpos, goal_ypos = 10, half_height - 70
goal_posts = [GoalPost((goal_xpos * .2, goal_ypos), WHITE, 0),
              GoalPost((screen_width - (goal_xpos * .8) - 3, goal_ypos), WHITE, 1)]

# The primary ball to score on
ball = Ball(half_screen, RED, ball_size)


# Checks if the mouse is clicked and inbound of the button
def isPressed(obj):
    return mouse.get_pressed(3)[0] and obj.collidepoint(mouse.get_pos())


def moveAllDirections(current_team, currentPlayer):
    self = SoccerTeamPlayers.CheckUsersMovement(current_team, currentPlayer)
    # The outer circle doesnt touch the left side, increment in x coordinate
    self.moveLeft()
    # Only to the right of the screen, decrement in x coordinate
    self.moveRight()
    # If below the scoreboard, increment in y coordinate
    self.moveUp()
    # if down arrow key is pressed, decrement in y coordinate
    self.moveDown()


# Uses the team their on and which player player one has control
def playerControlMovement(play_team, teams):
    global p1_num, p2_num, vel

    # Creates a boost for the each player's velocity
    if pygame.key.get_pressed()[K_COLON] or pygame.key.get_pressed()[K_q]:
        vel = vel * 1.25

    # Gets the correct circle and controls from the team side chosen
    soccer = SoccerTeamPlayers.Teams
    num = {soccer.TEAM_ONE: p1_num, soccer.TEAM_TWO: p2_num}.get(play_team)
    moveAllDirections(play_team, teams[num])


def resetAllPositions():
    global left_team, right_team
    ball.placeAndRestBall([half_width, half_height])

    for team in [left_team, right_team]:
        team.resetPosition()
        team.setState(SoccerTeamPlayers.States.WAITING)


def displayStartPage():
    def displayOptions():
        for player in [player1, player2]:
            position = [player.position[0] - 35, player.position[1] + 50]
            for color_choice in playersOption:
                # Creates a new circle to display in intro, with specific color options
                new_player = Circle(position, color_choice, 15)
                # Makes sure its pressed and swaps the
                if isPressed(new_player.draw()):
                    player.color, new_player.color = new_player.color, player.color
                position[0] += 35

    def displayBothControls():
        def displayInstruct(ctrl):
            for x in range(len(ctrl)):
                screen.blit(default_label(ctrl[x] + instr[x]), instruct_position)
                instruct_position[1] += 30

        # Creates both instruction controls for both teams
        num_player = ["Player One", "Player Two"]
        controller = ["W", "S", "A", "D", "Q"], ["^", "v", "<", ">", "P"]
        instr = [" - move up", " - move down", " - move left", " - move right", " - boost"]

        # for player one instruction position
        instruct_position = [half_width * .3, half_height * .6]
        i = 0
        for num in num_player:
            screen.blit(default_label(num), instruct_position)
            instruct_position[1] += 30
            displayInstruct(controller[i])

            # for player two instruction position
            instruct_position = [half_width * 1.3, half_height * .6]
            i += 1

    global player1, player2
    screen.fill(PAGE_COLOR)  # Makes background

    # Displays the title
    screen.blit(default_label("Welcome to Retro Soccer", 60), (half_width * 0.55, 30))

    # Draws out both p1, p2 and other available options
    player1.draw()
    displayOptions()
    player2.draw()
    displayBothControls()


def StartPage():
    global player1, player2

    # Creates a new button for the start button
    button_position = [half_width * .85, screen_height * .8]
    play_button = pygame.Rect(button_position, button_size)

    while True:

        # Handling input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # If clicked on the button, it will start the game
        if isPressed(play_button):
            if player1.color is not player2.color:
                Main()
            else:
                msg = "Can't have both teams with same colors"
                label = default_label(msg, font_color=RED)
                position = [half_width, screen_height * .7]
                screen.blit(label, position)

        displayStartPage()

        # Draws the rectangle button
        pygame.draw.rect(screen, WHITE, play_button)
        # Creates a text to go with the button
        play_label = default_label("Play", font_color=BLACK)
        button_position[0] = half_width * .92
        screen.blit(play_label, button_position)

        pygame.display.flip()


def displayScoreFinal():
    global score
    score_position = player_pos = [20, half_height]
    score_position[1] *= 1.05

    # Displays the score sheet on the top of the screen
    screen.blit(default_label("Player 1", 200), player_pos)
    player_pos[0] = screen_width - player_pos[0]
    screen.blit(default_label("Player 2", 200), player_pos)

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
        screen.blit(default_label("Player 1" if score[0] > score[1] else "Player 2", 300), title_position)

    displayScoreFinal()


def GameResult():
    screen.fill(PAGE_COLOR)  # Clears the screen
    chooseWinner()
    # Creates a new button for the start button
    button_pos = [half_width * .85, screen_height - 145]
    button = pygame.Rect(button_pos, button_size)

    while True:
        # Handling input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # If clicked on the button, it will start the game
        if isPressed(button):
            return

        # Draws the rectangle button
        pygame.draw.rect(screen, WHITE, button)
        # Creates a text to go with the button
        play_label = default_label("Continue", font_color=BLACK)
        button_pos[0] = half_width * .95
        screen.blit(play_label, button_pos)


def displayLayout():
    def displayGoalAndPlayers():
        global left_team, right_team, goal_posts
        # ! Draws the goal post, left and right players
        [goal.draw() for goal in goal_posts]

        for player_side in [left_team.players, right_team.players]:
            [player.draw() for player in player_side]

    def displayScore():
        # ! Update scores
        # Displays the score board for both teams
        display_setup = ["Player 1", str(score[0]), "-", str(score[1]), "Player 2"]
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


def CountDownPage():
    countDown = 3
    # Starts a count down from 3 to start the game (starts at 'GO')
    while True:

        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                countDown -= 1
                if countDown == -1:
                    return

        screen.fill(PAGE_COLOR)  # Clears the screen
        pos = [half_width * .95, half_height * .75]

        # Displays number on the screen
        screen.blit(default_label(str(countDown), 100), pos)
        # Substitutes the Zero for 'GO!'
        if countDown == 0:
            screen.fill(PAGE_COLOR)  # Clears the screen
            pos[0] -= half_width * .05
            screen.blit(default_label("GO!", 100), pos)
        pygame.display.flip()
        clock.tick(60)


def getHit(player):
    # If any player collides with the ball push the ball with its velocity
    arr = direction(player, ball)
    for i in range(len(arr)):
        if arr[i] > 1:
            arr[i] = 1

        if arr[i] < -1:
            arr[i] = -1

    return [vel * arr[x] for x in range(len(arr))] if playerContact(player) else [0, 0]


# # Idea to use
def moveBall(time):
    # using scalar to vector formula x = ut + [(1/2 a t^2) = res]
    friction = -0.015
    ut = vel * float(time)
    half_res = .5 * friction * time ** 2
    # turn the scalar quantity into a vector by multiplying the value with
    #   the normalized velocity vector (because that gives the direction)
    scalar_to_vector = half_res * direction(0, vel)

    return ball.position + ut + scalar_to_vector
# # Idea to use \ end


def CheckCollide():
    global ball

    # Check if the ball is in the goal
    [goal_posts[x].isScored() for x in range(len(goal_posts))]

    # Checks if in bounds for both x, y coordinates
    in_field = inBounds(ball.position)
    if in_field:
        # for both teams
        for player_side in [left_team.players, right_team.players]:
            for player in player_side:
                # Saves the hit made and adds it to the balls position
                w, h = getHit(player)
                a, b = inBounds(ball)
                # if it hits the outer bounds it will stop from moving after it hits the bounds
                ball.setHorizontalMovement(w * (1 if a else -1))
                ball.setVerticalMovement(h * (1 if b else -1))
        return

    for i in range(len(in_field)):
        # hits back from going out of bounds
        if in_field[i]:
            ball.position[i] = - ball.position[i]


def MainGame():
    global left_team, right_team, p1_num, p2_num, counter
    while True:

        # Handling input
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                global counter
                counter -= 1

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        soccer = SoccerTeamPlayers.Teams

        # Controller for player 1
        playerControlMovement(soccer.TEAM_ONE, left_team.players)

        # Controller for player 2
        playerControlMovement(soccer.TEAM_TWO, right_team.players)

        # robotMovement(soccer.TEAM_ONE, left_team)  # For AI
        # robotMovement(soccer.TEAM_TWO, right_team)  # For AI

        CheckCollide()

        if counter == 0:
            screen.fill(PAGE_COLOR)  # Clears the screen
            screen.blit(default_label("GAME OVER!", 100), half_screen)
            GameResult()
            return

        # Visuals
        screen.fill(PAGE_COLOR)
        displayLayout()

        # ! Updating the window
        # pygame.display.update()
        pygame.display.flip()
        clock.tick(60)


def initializeTeams():
    global left_team, right_team
    # ! Creates the players on the screen
    # Displays the players on the screen for Both Side
    # Saves and displays the players on both sides
    teams = SoccerTeamPlayers.Teams
    left_team = SoccerTeamPlayers.Team(teams.TEAM_ONE, player1.color, goal_posts[0], goal_posts[1])
    right_team = SoccerTeamPlayers.Team(teams.TEAM_TWO, player2.color, goal_posts[1], goal_posts[0])


def Main():
    CountDownPage()
    initializeTeams()
    MainGame()


if __name__ == '__main__':
    StartPage()
