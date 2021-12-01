# from pygame.cursors import ball
import sys, pygame


(width, height) = (200, 300)

# class Ball:
#
#     def Ball(ballSize):
#         ball = Ball(ballSize, ballSize, ballSize, ballSize)
#         ball.center = width / 2, height / 2
#         ball.color = "white"
#
#     def getBallPosition():
#         return [ball.positionX(),ball.positionY]
#
#
#     def ballMove(x, y):
#         ball.direction = x, y
#
#     def ballSpeed(speed):
#         ball.speed = speed
#
#     def draw():
#         screen.clear()
#         screen.draw.filled_circle(ball, ball.color)
#
#
#     def bounceBack(dx,dy):
#         # Bounce the ball off the left or right walls
#         if ball.right >= width or ball.left <= 0:
#             ball.direction = -dx, dy
#
#         # Bounce the ball off the top or bottom walls
#         # (We'll remove this later when the bat and the
#         # bricks are in place)
#         #
#         if ball.bottom >= height or ball.top <= 0:
#             ball.direction = dx, -dy
#
#     def update():
#         ballMove(1,1)
#         dx,dy = ball.direction
#         ball.move_ip(ball.speed * dx, ball.speed * dy)
#         bounceBack(dx,dy)


