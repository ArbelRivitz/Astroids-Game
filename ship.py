from screen import *
#from asteroids_main import *
import math

class Ship:
    def __init__(self,x_loc,x_sped,y_loc,y_sped,heading):
        self.__x_loc = x_loc
        self.__y_loc = y_loc
        self.__x_sped = x_sped
        self.__y_sped = y_sped
        self.__heading = heading
        self.__radius = 1

    def get_x_loc (self):
        return self.__x_loc

    def get_y_loc (self):
        return self.__y_loc

    def get_x_sped (self):
        return self.__x_sped

    def get_y_sped (self):
        return self.__y_sped

    def get_heading (self):
        return self.__heading

    def get_radius (self):
        return self.__radius

    def set_x_loc (self,new_x_loc):
        self.__x_loc = new_x_loc

    def set_y_loc (self,new_y_loc):
        self.__y_loc = new_y_loc

    def set_x_sped (self,new_x_sped):
        self.__x_sped = new_x_sped

    def set_y_sped (self,new_y_sped):
        self.__y_sped = new_y_sped

    def set_heading (self,new_heading):
        self.__heading = new_heading




