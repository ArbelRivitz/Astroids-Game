from screen import *
import math

NORMALIZATION_NUM_1 = 10
NORMALIZATION_NUM_2 = -5


class Asteroid:
    def __init__(self, x, y, x_speed, y_speed, size):
        self.__x_loc = x
        self.__y_loc = y
        self.__x_speed = x_speed
        self.__y_speed = y_speed
        self.__size = size
        self.__radius = (
                        self.get_size() * NORMALIZATION_NUM_1) - NORMALIZATION_NUM_2

    def get_x_loc(self):
        return self.__x_loc

    def get_y_loc(self):
        return self.__y_loc

    def get_x_sped(self):
        return self.__x_speed

    def get_y_sped(self):
        return self.__y_speed

    def set_x_loc(self, new_x_loc):
        self.__x_loc = new_x_loc

    def set_y_loc(self, new_y_loc):
        self.__y_loc = new_y_loc

    def set_x_sped(self, new_x_sped):
        self.__x_sped = new_x_sped

    def set_y_sped(self, new_y_sped):
        self.__y_sped = new_y_sped

    def get_size(self):
        return self.__size

    def set_size(self, size):
        self.__size = size

    def get_radius(self):
        return self.__radius

    def set_radius(self, radius):
        self.__radius = radius

    def has_intersection(self, obj):
        astr_x_loc = self.get_x_loc()
        astr_y_loc = self.get_y_loc()
        astr_rad = self.get_radius()
        obj_x = obj.get_x_loc()
        obj_y = obj.get_y_loc()
        obj_rad = obj.get_radius()
        distance = math.sqrt(
            ((obj_x - astr_x_loc) ** 2) + (obj_y - astr_y_loc) ** 2)
        if distance <= (astr_rad + obj_rad):
            return True
        return False
