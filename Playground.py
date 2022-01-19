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

Problem: how to move the ball with player, then AI
'''

score = NO_VELOCITY = speed = [0, 0]

# ! Setting up the main window
screen_width, screen_height = 1080, 768
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Soccer Pong Game')
half_screen = half_width, half_height = screen_width // 2, screen_height // 2
button_size, goal_size = [150, 50], [10, 150]
ball_size, player_size = 20, 25


# Draws a circle on the screen
class Circle:
    def __init__(self, position, circle_color, circle_size=player_size):
        self.position = list(position)
        self.color, self.size = circle_color, circle_size

    def draw(self, size=0):  # Additional size
        return pygame.draw.circle(screen, self.color, self.position, self.size, size)


class GoalPost:
    def __init__(self, goal_line, circle_color):
        self.color = circle_color
        self.object = pygame.Rect(list(goal_line), goal_size)

    def draw(self):
        pygame.draw.rect(screen, self.color, self.object)


player1 = Circle((half_width * .35, half_height * .95), WHITE, 25)
player2 = Circle((screen_width * .8, half_height * .95), GREEN, 25)

# ! Draws the goal post on both sides on the field
goal_xpos, goal_ypos = 10, half_height - 70
goal_posts = [GoalPost((goal_xpos - 8, goal_ypos), WHITE), GoalPost((screen_width - goal_xpos - 2, goal_ypos), WHITE)]

# Game Rectangles
ball = Circle(half_screen, RED, ball_size)


def isPressed(obj):
    return mouse.get_pressed(3)[0] and obj.collidepoint(mouse.get_pos())


# For player and AI use
class CheckMovement:
    def __init__(self, position, size):
        self.position, self.size = position, size

    def isLeftBound(self):
        return self.position[0] > self.size

    def isRightBound(self):
        return self.position[0] < screen_width - self.size

    def isUpperBound(self):
        return self.position[1] > 75 + self.size

    def isLowerBound(self):
        return self.position[1] < screen_height - self.size


class CheckUsersMovement(CheckMovement):
    def __init__(self, team, player, vel):
        super().__init__(player.position, player.size)
        self.keys, self.velocity = pygame.key.get_pressed(), vel
        soccer = SoccerTeamPlayers.Teams
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


def moveAllDirections(self):
    # The outer circle doesnt touch the left side, increment in x coordinate
    self.moveLeft()
    # Only to the right of the screen, decrement in x coordinate
    self.moveRight()
    # If below the scoreboard, increment in y coordinate
    self.moveUp()
    # if down arrow key is pressed, decrement in y coordinate
    self.moveDown()


def playingDefense(team_playing, selected_player):
    # playing_side = getTeam(team_playing)[selected_player]
    pass


def playingMiddle(team_playing, selected_player):
    pass


def playingOffense(team_playing, selected_player):
    pass


# Uses the team their on and which player player one has control
def playerControlMovement(play_team, teams):
    global p1_num, p2_num
    # stores keys pressed
    vel = 5

    # Creates a boost for the each player's velocity
    if pygame.key.get_pressed()[K_COLON] or pygame.key.get_pressed()[K_q]:
        vel = vel * 1.25

    soccer = SoccerTeamPlayers.Teams
    # Gets the correct circle and controls from the team side chosen
    num = {soccer.TEAM_ONE: p1_num, soccer.TEAM_TWO: p2_num}.get(play_team)
    moveAllDirections(CheckUsersMovement(play_team, teams[num], vel))


def robotMovement(team):  # TODO
    global ball
    place = 0
    # For defense
    position = SoccerTeamPlayers.MovingPosition.DEFENSE
    for x in range(position.value):
        playingDefense(team, place)
        place += 1

    # For middle
    for x in range(position.value):
        playingMiddle(team, place)
        place += 1

    # For forward
    for x in range(position.value):
        playingOffense(team, place)
        place += 1


def isGoal():
    global ball, goal_posts
    for index in range(len(goal_posts)):
        if goal_posts[index].object.collidepoint(ball.position):
            score[(index + 1) % 1] += 1

    MainGame()  # Should restart the original position


def inBounds(ply):
    return ply.position[0] in range(ply.size, screen_width - ply.size), \
           ply.position[1] in range(ply.size, screen_height - ply.size)


playersOption = allColors
# Removes the color already chosen by each player
playersOption.remove(player1.color)
playersOption.remove(player2.color)


def OptionPage():
    screen.fill(PAGE_COLOR)  # Clears the screen


def displayOptions():
    def makeOptions():
        # Collects all the colors available
        result, space = [], .4
        for color_choice in playersOption:
            new_player = Circle((half_width + space - 15, screen_height * .7), color_choice)
            result.append(new_player)
            space += 50
        return result

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


def displayBothControls():
    num_player = ["Player One", "Player Two"]
    controller = ["W", "S", "A", "D", "Q"], ["^", "v", "<", ">", "P"]
    instr = [" - move up", " - move down", " - move left", " - move right", " - boost"]

    # for player one instruction position
    instruct_position = [half_width * .5, half_height * .6]
    i = 0
    for num in num_player:
        screen.blit(default_label(num), instruct_position)
        instruct_position[1] += 30
        for x in range(len(controller[i])):
            screen.blit(default_label(controller[i][x] + instr[x]), instruct_position)
            instruct_position[1] += 30

        # for player two instruction position
        instruct_position = [half_width * 1.2, half_height * .6]
        i += 1


def displayStartPage():
    global player1, player2
    screen.fill(PAGE_COLOR)
    screen.blit(default_label("Welcome to Retro Soccer", 40), (half_width * 0.55, 30))
    displayPlayerTitle()
    player1.draw()
    displayOptions()
    player2.draw()
    displayBothControls()


def StartPage():
    global player1, player2

    # Creates a new button for the start button
    button_position = [half_width * .85, screen_height * .8]
    play_button = pygame.Rect(button_position, button_size)
    button_position[1] += 50
    option_button = pygame.Rect(button_position, button_size)
    button_position[1] -= 50

    while True:

        # Handling input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # If clicked on the button, it will start the game
        if isPressed(play_button):
            Main()
        if isPressed(option_button):
            OptionPage()

        displayStartPage()

        # Draws the rectangle button
        pygame.draw.rect(screen, WHITE, play_button)
        # Creates a text to go with the button
        play_label = default_label("Play", font_color=BLACK)
        button_position[0] = half_width * .95
        screen.blit(play_label, button_position)

        pygame.display.flip()


def GameOverPage():
    screen.fill(PAGE_COLOR)  # Clears the screen
    screen.blit(default_label("GAME OVER!", 100), half_screen)
    GameResult()


def displayScoreFinal():
    global score
    score_position = player_pos = [20, half_height]
    score_position[1] *= 1.05

    screen.blit(default_label("Player 1", 200), player_pos)
    player_pos[0] = screen_width - player_pos[0]
    screen.blit(default_label("Player 2", 200), player_pos)

    for player_score in [str(score[0]), "-", str(score[1])]:
        screen.blit(default_label(player_score, 200), score_position)


def chooseWinner():
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


def ScoreBoard():
    screen.fill(PAGE_COLOR)  # Clears the screen
    screen.blit(default_label("Score Board", 100), (half_width, 50))
    # TODO: (Optional) Create a Table


def displayScore():
    # ! Update scores
    # Displays the score board for both teams
    display_setup = ["Player 1", str(score[0]), "-", str(score[1]), "Player 2"]
    spacing, position = [150, 25, 25, 125, 0], [half_width - 250, 20]
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
    # Draws the lines parallel to the goal
    goal_line_vert, shift = 20, 8
    goal_side = [goal_line_vert - shift, start_point], [goal_line_vert - shift, screen_width]
    pygame.draw.aaline(screen, WHITE, list(goal_side[0]), list(goal_side[1]))

    # Makes the first element in each list the inverse of the whole screen width
    goal_side[0][0] = goal_side[1][0] = screen_width - goal_line_vert + shift
    pygame.draw.aaline(screen, WHITE, list(goal_side[0]), list(goal_side[1]))


def displayField(start_pos):
    # Draws a vertical line in the middle of the screen
    pygame.draw.aaline(screen, WHITE, (half_width, start_pos), (half_width, screen_width))
    # Draws a horizontal line in the middle of the screen
    pygame.draw.aaline(screen, WHITE, (0, start_pos), (screen_width, start_pos))
    # Draws the circle of the field
    Circle(half_screen, WHITE, 200).draw(3)


def displayLayout():
    global ball
    line_pos = 75
    displayField(line_pos)
    displayGoalSides(line_pos)
    displayTime()
    displayScore()

    # ! Red ball in the center
    ball.draw()


def displayGoalAndPlayers():
    global left_team, right_team, goal_posts
    # ! Draws the goal post, left and right players
    [goal.draw() for goal in goal_posts]

    for player_side in [left_team.players, right_team.players]:
        [player.draw() for player in player_side]


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


def hit(circle_player):
    rise = circle_player.position[1] - ball.position[1]
    run = circle_player.position[0] - ball.position[0]
    total_radius = (player_size // 2 + ball_size // 2)
    # Distance of the centers, radius of both circles
    return rise // run < total_radius


def getHit(player, ball):
    p, b = player.draw(), ball.draw()
    # If any player collides with the ball push the ball with its velocity
    # In the x direction
    if p.colliderect(b)[0]:
        return player.vel, 0
    # In the y direction
    if p.colliderect(b)[1]:
        return 0, player.vel

    if hit(p):
        return player.vel


def CheckCollide():
    global ball

    # Checks if in bounds for both x, y coordinates
    in_field = inBounds(ball)
    if in_field:
        # for both teams
        for player_side in [left_team.players, right_team.players]:
            for player in player_side and in_field:
                ball.position[1] += 1 # getHit() # TODO
        return

    if in_field[0]:  # Jumps back the left and right sides
        ball.position[0] = - ball.position[0]

    if in_field[1]:  # Jumps back the top to bottom sides
        ball.position[1] = - ball.position[1]


def initializeTeams():
    global left_team, right_team
    # ! Creates the players on the screen
    # Displays the players on the screen for Both Side
    # Saves and displays the players on both sides
    left_team = SoccerTeamPlayers.Team(SoccerTeamPlayers.Teams.TEAM_ONE, player1.color)
    right_team = SoccerTeamPlayers.Team(SoccerTeamPlayers.Teams.TEAM_TWO, player2.color)


def MainGame():
    global left_team, right_team, p1_num, p2_num

    initializeTeams()
    p1_num = p2_num = 1
    # TODO: Switches the player as it is pressed
    if pygame.key.get_pressed()[K_e]:
        p1_num += 1
    if pygame.key.get_pressed()[K_SLASH]:
        p2_num += 1

    while True:

        # Handling input
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                global counter
                counter -= 1
                if counter <= 1:
                    GameOverPage()
                    return

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        soccer = SoccerTeamPlayers.Teams
        playerControlMovement(soccer.TEAM_ONE, left_team.players)
        playerControlMovement(soccer.TEAM_TWO, right_team.players)
        # robotMovement(soccer.TEAM_ONE)  # For AI
        # robotMovement(soccer.TEAM_TWO)  # For AI

        CheckCollide()

        # Visuals
        screen.fill(PAGE_COLOR)
        displayGoalAndPlayers()
        displayLayout()

        # ! Updating the window
        # pygame.display.update()
        pygame.display.flip()
        clock.tick(60)


def Main():
    # InstructionPage()
    CountDownPage()
    MainGame()


if __name__ == '__main__':
    StartPage()
