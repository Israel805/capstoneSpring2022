import sys

from Constant import *
from Playground import Main
from physics import Circle

# Creates both circles for the intro, the initial choice
player1 = Circle((half_width * .35, screen_height * .6), WHITE)
player2 = Circle((screen_width * .8, screen_height * .6), GREEN)
ball = Circle(half_screen, RED, ball_size)

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


def startPageDisplay():
    def displayInstruct(ctrl, pos):
        for x in range(len(ctrl)):
            screen.blit(default_label(ctrl[x] + instr[x]), pos)
            pos[1] += 30

    def displayBothControls():
        # for player one instruction position
        instruct_position = [half_width * .2, half_height * .6]
        for num in range(len(num_player)):
            # Creates the player number label
            screen.blit(default_label(num_player[num]), instruct_position)
            instruct_position[1] += 30
            displayInstruct(controller[num], instruct_position)

            # for player two instruction position
            instruct_position = [half_width * 1.4, half_height * .6]

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


''' Start of Page Functions '''


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


def StartPage():
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
        both_playr_colors = [player1.color, player2.color]
        if isPressed(play_button):
            if player1.color is not player2.color:
                if ball.color not in both_playr_colors:
                    CountDownPage()
                    Main(both_playr_colors, ball.color, counter)
        warning()

        startPageDisplay()
        timeOption(button_position)
        ballOptions()

        # Draws the rectangle button
        pygame.draw.rect(screen, WHITE, play_button)

        # Creates a text to go with the button
        play_label = default_label("Play", font_color=BLACK)
        button_position[0] = half_width * .95
        screen.blit(play_label, button_position)

        pygame.display.flip()


if __name__ == '__main__':
    StartPage()