import pygame

import PlayersOption
import ScreenCreation
from ScreenCreation import WHITE, BLACK, width, height, ScreenDetails


def main():
    # initializing imported module
    pygame.init()

    # Displaying a window of width and height
    screen = ScreenCreation.createScreen("Welcome Soccer", WHITE)

    # Displays text on its position
    upper_middle = (width * .25, 50)
    ScreenCreation.createTextToScreen(ScreenDetails(screen, 'Welcome to Retro Soccer', 10, BLACK, upper_middle))

    # Creates a button with corresponding text
    start_button = ScreenCreation.createButton(screen, BLACK, (width * .4 + 10, height * .6))

    button_position = (width * .45 + 10, height * .65 - 10)
    ScreenCreation.createTextToScreen(ScreenDetails(screen, 'Play', 0, BLACK, button_position))

    running = True

    # Keep game running till running is true
    while running:

        # Saves the mouse's position
        mouse = pygame.mouse.get_pos()

        # Check for event if user has pushed any event in queue
        for event in pygame.event.get():
            # if event.type == pygame.MOUSEBUTTONDOWN:

            # If event is of type quit then set
            running = event.type != pygame.QUIT

            # Something is wrong with click
            if ScreenCreation.checkButtonBounds(mouse, start_button) and pygame.mouse.get_pressed()[0]:
                PlayersOption.main()

        pygame.display.update()


if __name__ == '__main__':
    main()
