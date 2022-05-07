import copy
import numpy as np
from Constant import *


class CheckAIMovement:
    def __init__(self, position: list, size: int):
        self.position, self.size = position, size

    def isLeftBound(self) -> bool:
        return self.position[0] < self.size + sides[0]

    def isRightBound(self) -> bool:
        return self.position[0] > screen_width - self.size - sides[0]

    def isUpperBound(self) -> bool:
        return self.position[1] < self.size + sides[1]

    def isLowerBound(self) -> bool:
        return self.position[1] > screen_height - self.size


class Circle:
    def __init__(self, position: list, circle_color, circle_size: int = player_size):
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
        check = CheckAIMovement(self.position, self.size)
        if check.isLeftBound() and self.velocity[0] < 0:
            self.velocity[0] = -self.velocity[0]

        if check.isRightBound() and self.velocity[0] > 0:
            self.velocity[0] = -self.velocity[0]

        if check.isUpperBound() and self.velocity[1] < 0:
            self.velocity[1] = -self.velocity[1]

        if check.isLowerBound() and self.velocity[1] > 0:
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

        # if no collision is detected
        if not thing1.detect_collision(thing2):
            return thing1

        # Saves information about both objets
        pos1, pos2 = thing1.position, thing2.position
        vel1, vel2 = thing1.velocity, thing2.velocity
        mass1, mass2 = thing1.size ** 2, thing2.size ** 2

        # Subtracts both the velocity and the positions of both players
        posDiff, velDiff = np.subtract(pos1, pos2), np.subtract(vel1, vel2)

        # Creates the dot product of the difference in position and velocity
        dot_product = np.dot(velDiff, posDiff)
        norm_squared = np.inner(posDiff, posDiff)  # normalizes the position difference

        # Sets the new velocity
        thing1.velocity = vel1 - (2 * mass2 / (mass1 + mass2)) * (dot_product / norm_squared * posDiff)
        return thing1
