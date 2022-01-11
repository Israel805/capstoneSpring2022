import pygame
import sys
from pygame import *
# General setup
import SoccerTeamPlayers

WHITE = (255, 255, 255)
PAGE_COLOR = BLACK = (0, 0, 0)
LIGHT_GREY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
allColors = [LIGHT_GREY, RED, GREEN, WHITE, BLACK]

pygame.init()
clock = pygame.time.Clock()
pygame.time.set_timer(pygame.USEREVENT, 1000)


# Creates a label with default font or custom size
def default_label(string, font_size=30, font_color=WHITE):
    default_font = pygame.font.SysFont("Comic Sans MS", int(font_size))
    return default_font.render(str(string), True, font_color)


MINS = 5
counter = 60 * MINS  # 5 mins

'''
Trying to work the layout of the game
Looks like this is a good idea of the digital layout

Problem: how to get the players and the ball to move, then AI
'''

score, NO_VELOCITY = [0, 0], [0, 0]
speed = NO_VELOCITY

# ! Setting up the main window
screen_width, screen_height = 1080, 768
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Soccer Pong Game')
half_width, half_height = screen_width // 2, screen_height // 2


# Draws a circle on the screen
class Circle:
    def __init__(self, pos_x, pos_y, circle_color, player_size):
        self.pos_x, self.pos_y = pos_x, pos_y
        self.color, self.size = circle_color, (player_size if type(player_size) is int else 0)

    def draw(self, size=0):
        return pygame.draw.circle(screen, self.color, (self.pos_x, self.pos_y), self.size, size)

    def moveBall(self, direction, velocity):
        while inBounds(self) and velocity > 0:
            direction += velocity
            velocity -= 1


class GoalPost:
    def __init__(self, x_pos, y_pos, circle_color):
        self.color, goal_position = circle_color, (10, 150)
        self.object = pygame.Rect(x_pos, y_pos, goal_position[0], goal_position[1])

    def draw(self):
        pygame.draw.rect(screen, self.color, self.object)


player1 = Circle(half_width * .35, half_height * .95, WHITE, 25)
player2 = Circle(screen_width * .8, half_height * .95, GREEN, 25)


def isPressed(obj):
    return mouse.get_pressed(3)[0] and obj.collidepoint(mouse.get_pos())


class CheckMovement:
    def __init__(self, team, player):
        self.keys, soccer = pygame.key.get_pressed(), SoccerTeamPlayers.Teams
        self.player = player
        self.player_key = {
            soccer.TEAM_ONE: [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN],
            soccer.TEAM_TWO: [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s]
        }.get(team)

    def isLeftBound(self):
        return self.keys[self.player_key[0]] and self.player.pos_x > self.player.size

    def isRightBound(self):
        return self.keys[self.player_key[1]] and self.player.pos_x < screen_width - self.player.size

    def isUpperBound(self):
        return self.keys[self.player_key[2]] and self.player.pos_y > 75 + self.player.size

    def isLowerBound(self):
        return self.keys[self.player_key[3]] and self.player.pos_y < screen_height - self.player.size


# Uses the team their on and which player player one has control
def playerControlMovement(teams, player_num=0):
    # stores keys pressed
    soccer, vel = SoccerTeamPlayers.Teams, 5

    # Gets the correct circle and controls from the team side chosen
    player = {soccer.TEAM_ONE: playerCircleL, soccer.TEAM_TWO: playerCircleR}.get(teams)[player_num]
    check = CheckMovement(teams, player)

    # if left arrow key is pressed and the outer circle doesnt touch the left side
    if check.isLeftBound():
        # increment in x co-ordinate
        player.pos_x -= vel

    # if right arrow key is pressed and only to the right of the screen
    if check.isRightBound():
        # increment in x co-ordinate
        player.pos_x += vel

    # if up arrow key is pressed
    if check.isUpperBound():
        # decrement in y co-ordinate
        player.pos_y -= vel

    # if down arrow key is pressed
    if check.isLowerBound():
        # increment in y co-ordinate
        player.pos_y += vel


def isGoal():
    global ball, goal_posts

    for index in range(len(goal_posts)):
        if goal_posts[index].object.collidepoint(ball.pos_x, ball.pos_y):
            score[(index + 1) % 1] += 1

    MainGame()  # Should restart the original position


def inBounds(ply):
    return ply.size < ply.pos_x < screen_width - ply.size and \
           ply.size < ply.pos_y < screen_height - ply.size


# def robotMovement(teams, player_num=0):  # TODO
#     player = {
#         SoccerTeamPlayers.Teams.TEAM_ONE: playerCircleL,
#         SoccerTeamPlayers.Teams.TEAM_TWO: playerCircleR
#     }.get(teams)[player_num]
#
#     direction = 1
#     while True:
#         while inBounds(player):
#             player.pos_x += direction
#         direction = -direction


playersOption = allColors
# Removes the color already chosen by each player
playersOption.remove(player1.color)
playersOption.remove(player2.color)


def makeOptions():
    # Collects all the colors available
    result, space = [], .4
    for color_choice in playersOption:
        new_player = Circle((half_width + space - 15, screen_height * .7), color_choice, 15)
        result.append(new_player)
        space += 50

    return result


def OptionPage():
    screen.fill(PAGE_COLOR)  # Clears the screen


def displayOptions():
    global player1, player2
    for other_colors in makeOptions():
        color = other_colors.draw()
        # Makes sure its pressed and swaps the
        if isPressed(color):
            if isPressed(player1.draw()):
                player1.color, other_colors = other_colors, player1.color
                print("Player 1 changed with " + other_colors)

            if isPressed(player2.draw()):
                player2.color, other_colors = other_colors, player2.color
                print("Player 2 changed with " + other_colors)


def displayPlayerTitle():
    prob = .25
    cir_size = [half_width * prob, screen_height * .6]
    # Creates a lambda function to insert new string with same format
    screen.blit(default_label("Player 01"), cir_size)
    cir_size[0] = screen_width * (1 - prob)
    screen.blit(default_label("Player 02"), cir_size)


def displayStartPage():
    global player1, player2
    screen.fill(PAGE_COLOR)
    screen.blit(default_label("Welcome to Retro Soccer", 40), (half_width * 0.55, 30))
    player1.draw()
    displayOptions()
    player2.draw()


def StartPage():
    global player1, player2

    # Creates a new button for the start button
    button_width, button_height = half_width * .85, screen_height * .8
    button_vert, button_horiz = 50, 150
    play_button = pygame.Rect(button_width, button_height, button_horiz, button_vert)
    option_button = pygame.Rect(button_width, button_height + 50, button_horiz, button_vert)

    while True:

        # Handling input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # If clicked on the button, it will start the game
        if isPressed(play_button):
            MainGame()
        if isPressed(option_button):
            OptionPage()

        displayStartPage()

        # Draws the rectangle button
        pygame.draw.rect(screen, WHITE, play_button)
        # Creates a text to go with the button
        play_label = default_label("Play", font_color=BLACK)
        screen.blit(play_label, (half_width * .95, button_height))

        pygame.display.flip()


def GameOverPage():
    screen.fill(PAGE_COLOR)  # Clears the screen
    screen.blit(default_label("GAME OVER!", 100), (half_width, half_height))

    GameResult()


def displayScoreFinal():
    screen.blit(default_label("Player 1", 200), (20, half_height))
    screen.blit(default_label(str(score[0]), 200), (20, half_height * 1.05))
    screen.blit(default_label("-", 200), (20, half_height * 1.05))
    screen.blit(default_label("Player 2", 200), (screen_width - 20, half_height))
    screen.blit(default_label(str(score[1]), 200), (20, half_height * 1.05))


def chooseWinner():
    if score[0] == score[0]:
        screen.blit(default_label("Draw", 200), (half_width, 50))
    else:
        screen.blit(default_label("Winner", 200), (half_width, 50))
        screen.blit(default_label("Player 1" if score[0] > score[1] else "Player 2", 300), (half_width, 150))

    displayScoreFinal()


def GameResult():
    screen.fill(PAGE_COLOR)  # Clears the screen
    chooseWinner()
    # Creates a new button for the start button
    button_width, button_height = half_width * .85, screen_height - 145
    button_vert, button_horiz = 50, 150
    button = pygame.Rect(button_width, button_height, button_horiz, button_vert)

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
        screen.blit(play_label, (half_width * .95, button_height))


def ScoreBoard():
    screen.fill(PAGE_COLOR)  # Clears the screen
    screen.blit(default_label("Score Board", 100), (half_width, 50))
    # TODO: (Optional) Create a Table


def displayScore():
    # ! Update scores
    # Displays the score board for both teams
    display_setup = ["Player 1", str(score[0]), "-", str(score[1]), "Player 2"]
    spacing, position = [200, 50, 50, 150, 0], [half_width - 250, 20]
    index = 0
    for score_setup in display_setup:
        screen.blit(default_label(score_setup), position)
        position[0] += spacing[index]


def displayTime():
    # Displays the time for the Game
    mins, sec = str(counter // 60), counter % 60
    sec = ('0' if sec < 10 else '') + str(sec)
    screen.blit(default_label("Time: " + mins + ":" + sec), (50, 20))


def displayGoalSides(start_point):
    goal_line_vert = 20
    pygame.draw.aaline(screen, WHITE, (goal_line_vert, start_point), (goal_line_vert, screen_width))
    goal_line_vert = screen_width - goal_line_vert + 10
    pygame.draw.aaline(screen, WHITE, (goal_line_vert, start_point), (goal_line_vert, screen_width))


def displayLayout(ball):
    line_pos, size = 75, 100
    # Draws a vertical line in the middle of the screen
    pygame.draw.aaline(screen, WHITE, (half_width, line_pos), (half_width, screen_width))

    # Draws a horizontal line in the middle of the screen
    pygame.draw.aaline(screen, WHITE, (0, line_pos), (screen_width, line_pos))

    # Draws the lines parallel to the goal
    displayGoalSides(line_pos)

    # Draws the circle of the field
    Circle(half_width, half_height, WHITE, size * 2).draw(3)

    displayTime()
    displayScore()

    # ! Red ball in the center
    ball.draw()


def StartUp():
    countDown = 3
    # Starts a count down from 3 to start the game (starts at 'GO')
    while True:

        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                countDown -= 1
                if countDown == -1:
                    return

        screen.fill(PAGE_COLOR)  # Clears the screen
        # Displays number on the screen
        screen.blit(default_label(str(countDown), 100), (half_width * .95, half_height * .75))
        # Substitutes the Zero for 'GO!'
        if countDown == 0:
            screen.fill(PAGE_COLOR)  # Clears the screen
            screen.blit(default_label("GO!", 100), (half_width * .9, half_height * .75))
        pygame.display.flip()
        clock.tick(60)


def addNewPlayer(side, player_color):
    res, circle_size = [], 25
    # Displays the players on the screen for Both Side
    for soccer_player in side:
        # Adds to the list the new player
        player = soccer_player.value
        # Uses same size, color and its specific position
        res.append(Circle(player[0], player[1], player_color, circle_size))
    return res


def displayAllPlayers():
    global player1, player2

    # ! Creates the players on the screen
    left_side, right_side = SoccerTeamPlayers.StartPositionLeft, SoccerTeamPlayers.StartPositionRight
    left_side_color, right_side_color = player1.color, player2.color

    # Player01 = SoccerTeamPlayers.Team(left_side, player1.color, )

    # Displays the players on the screen for Both Side
    return [addNewPlayer(left_side, left_side_color), addNewPlayer(right_side, right_side_color)]


def MainGame():
    global playerCircleL, playerCircleR
    StartUp()

    # Game Rectangles
    ball = Circle(half_width, half_height, RED, 20)

    # ! Draws the goal post on both sides on the field
    goal_xpos, goal_ypos = 10, half_height - 70
    goal_posts = [GoalPost(goal_xpos, goal_ypos, WHITE), GoalPost(screen_width - goal_xpos, goal_ypos, WHITE)]

    # Saves and displays the players on both sides
    playerCircleL, playerCircleR = displayAllPlayers()

    while True:

        # Handling input
        for event in pygame.event.get():

            if event.type == pygame.USEREVENT:
                global counter
                counter -= 1
                if counter == 0:
                    GameOverPage()
                    return

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        soccer = SoccerTeamPlayers.Teams

        playerControlMovement(soccer.TEAM_ONE, 1)
        playerControlMovement(soccer.TEAM_TWO, 1)
        #robotMovement(soccer.TEAM_ONE)

        # Visuals
        screen.fill(PAGE_COLOR)

        # ! Draws the goal post, left and right players
        for goal in goal_posts:
            goal.draw()

        for player_side in [playerCircleL, playerCircleR]:
            for player in player_side:
                player.draw()

        displayLayout(ball)

        # ! Updating the window
        # pygame.display.update()
        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    MainGame()
