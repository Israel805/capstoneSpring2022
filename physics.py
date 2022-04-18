import copy
from random import shuffle
import numpy as np
from Constant import *


class Circle:
    def __init__(self, position, circle_color, circle_size=player_size):
        self.position = np.array(position)
        self.color, self.size = circle_color, circle_size
        self.velocity = self.acceleration = np.array([0, 0])

    def draw(self, size=0):  # Additional size
        return pygame.draw.circle(screen, self.color, list(self.position), self.size, size)

    def move(self):  # Adds the velocity to the position
        self.position = np.add(self.position, self.velocity)

    def set_pos_vel(self, body):  # sets the position and the velocity
        self.position, self.velocity = np.array(body.position), np.array(body.velocity)

    # Applies the acceleration and adds it to the velocity
    def apply_acceleration(self, acceleration: np.array):
        self.acceleration, self.velocity = acceleration, np.add(self.velocity, self.acceleration)

    def normal_velocity(self):  # makes velocity normalized
        return np.linalg.norm(self.velocity)

    # Checks if circle is hitting the wall and bounce off the wall
    def bounce_wall(self):
        maxX, maxY = screen_width, screen_height

        if self.position[0] < self.size + sides[0] and self.velocity[0] < 0:
            self.velocity[0] = -self.velocity[0]

        if self.position[0] > maxX - self.size - sides[0] and self.velocity[0] > 0:
            self.velocity[0] = -self.velocity[0]

        if self.position[1] < self.size + sides[1] and self.velocity[1] < 0:
            self.velocity[1] = -self.velocity[1]

        if self.position[1] > screen_height - self.size and self.velocity[1] > 0:
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
        thing1 = copy.deepcopy(self)
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
