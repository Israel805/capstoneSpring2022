import pygame
import Gameplay
import ScreenCreation
from ScreenCreation import checkButtonBounds, WHITE, BLACK, \
    width, height, createTextToScreen, ScreenDetails

'''
    This is the second page that allows user to choose which avatar
    they an choose and also make the total number of players
'''


def main():
    # initializing imported module
    pygame.init()

    # Displaying a window of width and height
    screen = ScreenCreation.createScreen("Choose Player", WHITE)
    running = True
    clicked = False

    # Keep game running till running is true
    while running:

        # Saves the mouse's position
        mouse = pygame.mouse.get_pos()

        # Displays text on its position
        upper_middle = (width * .32, 50)
        createTextToScreen(ScreenDetails(screen, 'Choose Your Players', 0, BLACK, upper_middle))

        left_side = (width * .15, height * .65)
        createTextToScreen(ScreenDetails(screen, 'Player 01', -10, BLACK, left_side))

        right_side = (width * .75, height * .65)
        createTextToScreen(ScreenDetails(screen, 'Player 02', -10, BLACK, right_side))

        # Creates a button with corresponding text
        play_button = ScreenCreation.createButton(screen, BLACK, (width * .4 + 10, height * .75))

        bottom_middle = (width * .46, height * .78)
        createTextToScreen(ScreenDetails(screen, 'Start', 0, WHITE, bottom_middle))

        # Check for event if user has pushed any event in queue
        for event in pygame.event.get():
            # If event is of type quit then set
            running = event.type != pygame.QUIT
        pygame.display.update()

        if not clicked and checkButtonBounds(mouse, play_button):
            print("It was clicked")
            Gameplay.main()
            clicked = True  # Thinking of making it stop after the game is done


if __name__ == '__main__':
    main()
