from random import shuffle, random
import numpy as np
from pygame import *

# General setup
import SoccerTeamPlayers
from AI import direction, distance
from Constant import *
from brains.BehindAndTowards import BehindAndTowards
from brains.DefendersAndAttackers import DefendersAndAttackers


# Draws a circle on the screen
class Circle:
    def __init__(self, position, circle_color, circle_size=player_size):
        self.position = np.array(position)
        self.color, self.size = circle_color, circle_size
        self.velocity = self.acceleration = np.array(ZERO_MATRIX)

    def getLocation(self):  # returns the position of the circle
        return self.position

    def draw(self, size=0):  # Additional size
        return pygame.draw.circle(screen, self.color, self.position, self.size, size)

    def move(self):  # Adds the velocity to the position
        self.position = np.add(self.position, self.velocity)

    def set_pos_vel(self, body):  # sets the position and the velocity
        self.position = body.position
        self.velocity = body.velocity

    # Applies the acceleration and adds it to the velocity
    def apply_acceleration(self, acceleration: np.array):
        self.acceleration = acceleration
        self.velocity = np.add(self.velocity, self.acceleration)

    def normal_velocity(self):  # makes velocity normalized
        return np.linalg.norm(self.velocity)

    # Checks if circle is hitting the wall and bounce off the wall
    def bounce_wall(self):
        check = SoccerTeamPlayers.CheckMovement(list(self.position), self.size)
        leftBound = check.isLeftBound() and self.velocity[0] < 0
        right_bound = check.isRightBound() and self.velocity[0] > 0
        if leftBound or right_bound:
            self.velocity[0] = -self.velocity[0]

        upperBound = check.isUpperBound() and self.velocity[1] < 0
        lowerBound = check.isLowerBound() and self.velocity[1] > 0
        if upperBound or lowerBound:
            self.velocity[1] = -self.velocity[1]

    # Finds any detection from the overlap and if it is towards
    def detect_collision(self, obj):
        posDiff = np.subtract(self.position, obj.position)
        dist_squared = np.dot(posDiff, posDiff)
        overlap = dist_squared <= (self.size + obj.size) ** 2

        posPlusVel1, posPlusVel2 = np.add(self.position, self.velocity), np.add(obj.position, obj.velocity)
        dist2 = np.linalg.norm(np.subtract(posPlusVel1, posPlusVel2))
        towards = dist2 ** 2 < dist_squared

        return overlap and towards

    # Calculates the collision (uses detect_collision)
    def calculate_collision(self, thing2):
        thing1 = self
        if not thing1.detect_collision(thing2):
            return thing1

        pos1, pos2 = thing1.position, thing2.position
        vel1, vel2 = thing1.velocity, thing2.velocity
        mass1, mass2 = thing1.size ** 2, thing2.size ** 2

        posDiff, velDiff = np.subtract(pos1, pos2), np.subtract(vel1, vel2)

        dot_product = np.dot(velDiff, posDiff)
        norm_squared = np.inner(posDiff, posDiff)

        thing1.velocity = vel1 - (2 * mass2 / (mass1 + mass2)) * (dot_product / norm_squared * posDiff)
        return thing1


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
        self.object = pygame.Rect(list(goal_line), goal_size)

    def getGoalCenter(self):
        return self.object.center

    def getLeftSide(self):
        return self.object.top if bool(self.goal_number) else self.object.bottom

    def getRightSide(self):
        return self.object.top if not bool(self.goal_number) else self.object.bottom

    def draw(self):
        pygame.draw.rect(screen, self.color, self.object)

    def isScored(self):
        def resetAllPositions():
            global left_team, right_team
            ball.placeAndRestBall([half_width, half_height])

            # Goes though each team and player to return to their original position
            for team in [left_team, right_team]:
                team.resetPosition()
                team.setState(SoccerTeamPlayers.States.WAITING)

        if self.object.collidepoint(ball.position):
            score[self.goal_number] += 1
            resetAllPositions()


# Creates both circles for the intro, the initial choice
player1 = Circle((half_width * .35, screen_height * .6), WHITE)
player2 = Circle((screen_width * .8, screen_height * .6), GREEN)

# ! Draws the goal post on both sides on the field
goal_posts = [GoalPost((goal_xpos * .2, goal_ypos), WHITE, 0), GoalPost((screen_width -
                                                                         (goal_xpos * .8) - 3, goal_ypos), WHITE, 1)]

# The primary ball to score on
ball = Ball(half_screen, RED, ball_size)

''' Brain Functions'''


def start(listOfPlayers):
    for player_side in [left_team.players, right_team.players]:
        for player in player_side:
            listOfPlayers.append(player)
    listOfPlayers.append(ball)


def tick(list_input):
    global ticks
    ticks = ticks + 1

    new_bodies = []
    for b1 in list_input:
        new_body = b1
        for b2 in list_input:
            if b1 != b2:
                new_body = new_body.calculate_collision(b2)
        new_body.bounce_wall()
        new_bodies.append(new_body)
        new_body.move()

    for i in range(len(list_input)):
        list_input[i].set_pos_vel(new_bodies[i])

    shuffle(list_input)


def limit_velocities():
    ball_velocity = ball.normal_velocity()

    if ball_velocity > max_ball_velocity:
        ball.velocity = np.multiply(ball.velocity, max_ball_velocity / ball_velocity)

    for t in [left_team, right_team]:
        for p in t.players:
            player_velocity = p.normal_velocity()
            if player_velocity > max_ball_velocity:
                p.velocity = np.multiply(p.velocity, max_ball_velocity / player_velocity)


def game_time_complete():
    return float(ticks) / float(counter)


def flip_pos(positions):
    result = positions

    if positions.ndim == 2:
        for i in range(len(positions)):
            result[i][0] = screen_width - 1 - positions[i][0]

    if positions.ndim == 1:
        result[0] = screen_width - 1 - positions[0]

    return result


def flip_vel(velocities):
    result = velocities

    if velocities.ndim == 2:
        for i in range(len(velocities)):
            result[i][0] = -1 * velocities[i][0]

    if velocities.ndim == 1:
        result[0] = -1 * velocities[0]

    return result


def flip_acc(accelerations):
    result = accelerations

    if accelerations.ndim == 2:
        for i in range(len(accelerations)):
            result[i][0] = -1 * accelerations[i][0]

    return result


def run_brains():
    p1_pos = left_team.positionMatrix()
    p1_vel = left_team.velocityMatrix()

    p2_pos = right_team.positionMatrix()
    p2_vel = right_team.velocityMatrix()

    ball_pos, ball_vel = ball.position, ball.velocity

    game_time = game_time_complete()

    t1_brain = left_team.brain
    t2_brain = right_team.brain

    t1_move = t1_brain.move(p1_pos, p1_vel, p2_pos, p2_vel,
                            ball_pos, ball_vel, score[0], score[1], game_time)
    left_team.applyMoveToAllPlayers(t1_move)

    # TODO: translate red positions and velocities
    #       so that both brains think that they are playing from left (0,y) to right (MAX_X,y)
    t2_move = t2_brain.move(flip_pos(p2_pos), flip_vel(p2_vel),
                            flip_pos(p1_pos), flip_vel(p1_vel),
                            flip_pos(ball_pos), flip_vel(ball_vel),
                            score[1], score[0], game_time)
    t2_move = flip_acc(t2_move)
    right_team.applyMoveToAllPlayers(t2_move)


''' End of brain Functions'''

''' Start of Display Functions '''


def colorOptions(circle, position):
    num, original_x = 0, position[0]
    for color_choice in ALL_COLORS:
        # Creates a new circle to display in intro, with specific color options
        new_player = Circle(position, color_choice, 15)
        # Adds special format
        if (num + 1) % 4 == 0:
            position = [original_x, position[1] + 35]
        # Makes sure its pressed and swaps the
        if isPressed(new_player.draw()):
            circle.color, new_player.color = new_player.color, circle.color
        position[0] += 35
        num += 1


def startPage():
    def displayBothControls():
        def displayInstruct(ctrl):
            for x in range(len(ctrl)):
                screen.blit(default_label(ctrl[x] + instr[x]), instruct_position)
                instruct_position[1] += 30

        # for player one instruction position
        instruct_position = [half_width * .2, half_height * .6]
        i = 0
        for num in num_player:
            # Creates the player number label
            screen.blit(default_label(num), instruct_position)
            instruct_position[1] += 30
            displayInstruct(controller[i])

            # for player two instruction position
            instruct_position = [half_width * 1.4, half_height * .6]
            i += 1

    global player1, player2
    screen.fill(PAGE_COLOR)  # Makes background

    # Displays the title
    screen.blit(default_label(TITLE, 60), (half_width * .4, 30))

    # Draws out both p1, p2 and other available options
    player1.draw()

    # Displays the coloring options for both players
    for player in [player1, player2]:
        position = [player.position[0] - 70, player.position[1] + 50]
        colorOptions(player, position)

    player2.draw()
    displayBothControls()


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


def timeOption(button_pos):
    global counter
    # Creates a label for time
    button = [button_pos[0] * 0.85, button_pos[1] * .8]
    screen.blit(default_label("Time: "), button)
    # Creates a label for different time options
    button[0] = button_pos[0] + 20
    screen.blit(default_label(str(counter // 60) + " mins"), button)
    button = [button_pos[0] * .6, button_pos[1] * .9]

    option_button = []  # Saves all the rect made

    # Displays each available time to
    for index in range(len(options)):
        option_button.append(pygame.Rect(button, [50, 20]))
        # If clicked on, then it will change the counter to be that time
        if isPressed(option_button[index]):
            new_time = 5 + (index * 5)
            counter = 60 * new_time

        # Draws new time option on the screen
        pygame.draw.rect(screen, BLACK, option_button[index])
        screen.blit(default_label(options[index], font_size=25), button)
        button[0] += 100


def warning():
    position = [half_width, screen_height * .85]
    screen.blit(default_label("Can't have both teams with same colors!", font_size=40, font_color=RED), position)


def ballOptions():
    # Creates a ball label
    pos = [ball.position[0] * .95, ball.position[1] * .75]
    screen.blit(default_label("Ball"), pos)
    # Draws out the ball on the screen
    ball.draw()
    # Displays the many color options it can be
    pos = [ball.position[0] * .9, screen_height * .55]
    colorOptions(ball, pos)


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
    def displayGoalAndPlayers():
        global left_team, right_team, goal_posts
        # ! Draws the goal post, left and right players
        [goal.draw() for goal in goal_posts]

        # Draws each player on both teams
        for player_side in [left_team.players, right_team.players]:
            [player.draw() for player in player_side]

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
        # Only if ball is not the player's colors or player1 color is player2 color
        if isPressed(play_button):
            if player1.color is not player2.color:
                if ball.color not in [player1.color, player2.color]:
                    Main()
        warning()

        startPage()
        timeOption(button_position)
        ballOptions()

        # Draws the rectangle button
        pygame.draw.rect(screen, WHITE, play_button)
        # Creates a text to go with the button
        play_label = default_label("Play", font_color=BLACK)
        button_position[0] = half_width * .95
        screen.blit(play_label, button_position)

        pygame.display.flip()


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
        # clock.tick(240)


''' End of All Page Functions'''


# Mode where ball would move if only touched by a player
def touchBallMode():
    def playerContact(circle_player):
        # Distance of the centers, radius of both circles
        return distance(circle_player, ball) <= ball_size * 2

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


def MainFunction():
    global ball

    # Check if the ball is in the goal
    [goal_posts[x].isScored() for x in range(len(goal_posts))]
    circles = []
    start(circles)
    ball.velocity = np.array([random() - 0.5, random() - 0.5])

    run_brains()
    limit_velocities()
    tick(circles)


def initializeTeams():
    global left_team, right_team
    # ! Creates the players on the screen
    # Displays the players on the screen for Both Side
    # Saves and displays the players on both sides
    teams = SoccerTeamPlayers.Teams
    left_team = SoccerTeamPlayers.Team(teams.TEAM_ONE, player1.color, goal_posts[0], goal_posts[1])
    right_team = SoccerTeamPlayers.Team(teams.TEAM_TWO, player2.color, goal_posts[1], goal_posts[0])

    # Creates a game tactic where the AI can play with
    right_team.brain = DefendersAndAttackers(ball)
    left_team.brain = BehindAndTowards(ball)


def MainGame():
    # Uses the team their on and which player player one has control
    def playerControlMovement(play_team, teams):
        global vel

        # Creates a boost for the each player's velocity
        if pygame.key.get_pressed()[K_COLON] or pygame.key.get_pressed()[K_q]:
            vel = vel * 1.25

        # Gets the correct circle and controls from the team side chosen
        num = {soccer.TEAM_ONE: p1_num, soccer.TEAM_TWO: p2_num}.get(play_team)

        return SoccerTeamPlayers.User(play_team, teams[num])

    global left_team, right_team, counter
    while True:

        # Handling input
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                counter -= 1

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        soccer = SoccerTeamPlayers.Teams

        # Controller for player 1
        playerControlMovement(soccer.TEAM_ONE, left_team.players).moveAllDirections()

        # Controller for player 2
        playerControlMovement(soccer.TEAM_TWO, right_team.players).moveAllDirections()

        # robotMovement(soccer.TEAM_ONE, left_team)  # For AI
        # robotMovement(soccer.TEAM_TWO, right_team)  # For AI

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
        # pygame.display.update()
        pygame.display.flip()
        clock.tick(60)


def Main():
    CountDownPage()
    initializeTeams()
    MainGame()


if __name__ == '__main__':
    StartPage()
