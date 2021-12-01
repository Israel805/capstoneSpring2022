import sys, pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
# from pygame.examples.headless_no_windows_needed import screen
#
# WIDTH = 640
# HEIGHT = 480
#
#
# class ZRect:
#     pass
#
#
# class Ball(ZRect): pass
#
#
# #
# # The ball is a red square halfway across the game screen
# #
# #ball = Ball(0, 0, 30, 30)
# ball.center = WIDTH / 2, HEIGHT / 2
# ball.colour = "red"
# #
# # The ball moves one step right and one step down each tick
# #
# ball.direction = 1, 1
# #
# # The ball moves at a speed of 3 steps each tick
# #
# ball.speed = 3
#
#
# def draw():
#     #
#     # Clear the screen and place the ball at its current position
#     #
#     screen.clear()
#     screen.draw.filled_rect(ball, ball.colour)
#
#
# def update():
#     #
#     # Move the ball along its current direction at its current speed
#     #
#     dx, dy = ball.direction
#     ball.move_ip(ball.speed * dx, ball.speed * dy)
#
#     #
#     # Bounce the ball off the left or right walls
#     #
#     if ball.right >= WIDTH or ball.left <= 0:
#         ball.direction = -dx, dy
#
#     #
#     # Bounce the ball off the top or bottom walls
#     # (We'll remove this later when the bat and the
#     # bricks are in place)
#     #
#     if ball.bottom >= HEIGHT or ball.top <= 0:
#         ball.direction = dx, -dy
# Code that works
def ballTesting():
    pygame.init()
    # Size of the display
    size = width, height = 800, 400
    speed = [1, 1]
    position = [50, 50]
    background = WHITE
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Bouncing ball")
    ball = pygame.image.load("ball.jpg")
    draw = pygame.draw.circle(screen, BLACK, position, 15)
    ballrect = draw

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        ballrect = ballrect.move(speed)

        # Makes it bounce from the edge
        if ballrect.left < 0 or ballrect.right > width:
            speed[0] = -speed[0]
        if ballrect.top < 0 or ballrect.bottom > height:
            speed[1] = -speed[1]

        screen.fill(background)
        #screen.blit(ball, ballrect)
        pygame.display.flip()


if __name__ == '__main__':
    ballTesting()