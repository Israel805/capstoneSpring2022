import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
screen_size = (width, height) = (800, 400)

default_button_size = (150, 50)

default_font = 'Comic Sans MS'
default_text_size = 40


class ScreenDetails:
    def __init__(self, screen, string, size, color, text_position):
        self.screen = screen
        self.string = string
        self.text_size = int(size) + default_text_size
        self.color = color
        self.position = text_position


# Creates a new screen with given size, caption, and background color
def createScreen(caption, background_color):
    result = pygame.display.set_mode(screen_size)
    pygame.display.set_caption(str(caption))
    result.fill(background_color)
    return result


# Creates a new text in the screen with default font and text size
def createTextToScreen(details):
    txt = outputText(str(details.string), details.text_size, details.color)
    details.screen.blit(txt, details.position)


def createButton(screen, color, position):
    return pygame.draw.rect(screen, color, (position, default_button_size))


# Returns the text with details
def outputText(text, size, color):
    my_font = pygame.font.SysFont(default_font, size)
    return my_font.render(text, True, color)


# Checks if the user clicked within the boundaries
def checkButtonBounds(user, button):
    x1, x2 = button.centerx - button.width, button.centerx + button.width
    y1, y2 = button.centery - button.height, button.centery + button.height
    return x1 <= user[0] <= x2 and y1 <= user[1] <= y2
