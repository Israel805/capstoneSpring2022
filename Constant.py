# The display
from enum import Enum
from math import sqrt

import pygame

# Screen format
from pygame import mouse, DOUBLEBUF

''' Display Format/Size '''
screen_width, screen_height = 1080, 768
half_screen = half_width, half_height = screen_width // 2, screen_height // 2
button_size, ball_size, player_size = [150, 50], 20, 25
goal_size = [10, 150]
goal_xpos, goal_ypos = 10, half_height - 70

''' String Variables '''
MAIN_TITLE: str = 'Soccer Pong Game'
TITLE: str = 'Welcome to Retro Soccer'
options: list = ["5 mins", "10 mins", "15 mins", "20 mins", "25 mins"]
P1, P2 = "Player 1", "Player 2"
# Creates both instruction controls for both teams
num_player = ["Player One", "Player Two"]
controller = ["W", "S", "A", "D", "Q"], ["^", "v", "<", ">", "P"]
instr = [" - move up", " - move down", " - move left", " - move right", " - boost"]

''' Time Counter '''
MINS = 5
counter = 60 * MINS  # 5 mins

# All the colors
WHITE = (255, 255, 255)
PAGE_COLOR = BLACK = (0, 0, 0)
LIGHT_GREY = (200, 200, 200)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
ALL_COLORS = [LIGHT_GREY, RED, GREEN, YELLOW, BLUE, WHITE, BLACK]


# Creates a label with default font or custom size
def default_label(string, font_size=30, font_color=WHITE):
    default_font = pygame.font.SysFont("Comic Sans MS", int(font_size))
    return default_font.render(str(string), True, font_color)


# Checks if the mouse is clicked and inbound of the button
def isPressed(obj):
    return mouse.get_pressed(3)[0] and obj.collidepoint(mouse.get_pos())


# AI Variables
friction = -0.05

''' Global Variables '''
NUM_PLAYERS = 6
p1_num = p2_num = 0
sides = 20, 75
max_ball_velocity, user_velocity = 8, 5
max_player_velocity = max_ball_velocity // 2

''' Main Start of Pygame '''
# Creates a new pygame
pygame.init()

# Creates a new clock timer
clock = pygame.time.Clock()
pygame.time.set_timer(pygame.USEREVENT, 1000)

left_team = right_team = 0
flags = DOUBLEBUF
# ! Setting up the main window
screen = pygame.display.set_mode((screen_width, screen_height), flags, 16)
pygame.display.set_caption(MAIN_TITLE)

# Creates global variables
score = [0, 0]

''' All Classes '''


class Teams(Enum):
    TEAM_ONE, TEAM_TWO = 0, 1


w, h = half_screen

StartPositionRight = [[w * 1.4, h], [w * 1.7, h * .4], [w * 1.9, h],
                      [w * 1.6, h * .8], [w * 1.6, h * 1.5], [w * 1.9, h * .5], [w * 1.8, h * .8]]

# Initial position for left side team
StartPositionLeft = [[w * .6, h], [w * .5, h * 1.25], [w * .5, h * .75], [w * .5, h], [w * .4, h * 1.6],
                     [w * .2, h * .6], [w * .2, h * 1.2]]

''' Team-Based Selection Variables '''
player_control = {
    Teams.TEAM_ONE: [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s],
    Teams.TEAM_TWO: [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]
}

starting_position = {Teams.TEAM_ONE: StartPositionLeft, Teams.TEAM_TWO: StartPositionRight}


# Function to calculate the distance between two objects
def distance(obj1, obj2):
    r1, r2 = direction(obj1, obj2)
    # Distance formula
    return sqrt(r1 ** 2 + r2 ** 2)


# Calculates the direction on where it is going
def direction(obj1, obj2):
    # Finds the position in the objects
    if type(obj1) is not list:
        obj1 = obj1.position

    if type(obj2) is not list:
        obj2 = obj2.position

    x1, y1 = obj1
    x2, y2 = obj2

    # vertical, horizontal movement
    return [x2 - x1, y2 - y1]
