from screen import Screen
import math
from random import randint
import torpedo
import ship
import asteroid
import sys

MOVE_RIGHT = -7
MOVE_LEFT = 7
DEFAULT_ASTEROIDS_NUM = 5
ACCELRRATION_FACTOR = 2
SIZE_ONE_AST_POINTS = 100
SIZE_TWO_AST_POINTS = 50
SIZE_THREE_AST_POINTS = 20
INIT_HEAD = 0
INIT_SPEED = 0
INIT_SIZE_AST = 3
MAX_SPEED_AST = 3
INIT_LIFE = 3
ERROR_INTERSECT_TITLE = "Be Aware!"
ERROR_INTERSECT_MSG = "You lost one life."
ERROR_LIFE = "You ran out of life."
END_OF_GAME = "The game is over."
QUIT = "You've pressed quit."
WIN = "You won!!! well done."


class GameRunner:
    """This class is the main class of the game and it runs the game.
    The feature of this class is asteroid amount.
    In addition there are some thongs that we already implement here:
    max x, max y, min x. min y, delta x, delta y, ship object, asteroids list,
    torpedo list, score and life
    """

    def __init__(self, asteroids_amnt):
        self.__asteroids_amnt = asteroids_amnt
        self._screen = Screen()
        self.screen_max_x = Screen.SCREEN_MAX_X
        self.screen_max_y = Screen.SCREEN_MAX_Y
        self.screen_min_x = Screen.SCREEN_MIN_X
        self.screen_min_y = Screen.SCREEN_MIN_Y
        self.__delta_x = Screen.SCREEN_MAX_X - Screen.SCREEN_MIN_X
        self.__delta_y = Screen.SCREEN_MAX_Y - Screen.SCREEN_MIN_Y
        x_loc_ship = randint(self.screen_min_x, self.screen_max_x)
        y_loc_ship = randint(self.screen_min_y, self.screen_max_y)
        self._ship = ship.Ship(x_loc_ship, INIT_SPEED, y_loc_ship, INIT_SPEED,
                               INIT_HEAD)
        self.__asteroids_lst = []
        self.asteroids_list()
        self.__torpedo_lst = []
        self.__score = 0
        self.__life = INIT_LIFE

    def score_get(self):
        """This func returns the score"""
        return self.__score

    def score_set(self, new_score):
        """This func updates the score"""
        self.__score = new_score

    def get_delta_x(self):
        """This func returns the x delta"""
        return self.__delta_x

    def get_delta_y(self):
        """This func returns the y delta"""
        return self.__delta_y

    def get_asteroids_amnt(self):
        """This func returns the asteroids amount"""
        return self.__asteroids_amnt

    def get_life(self):
        """This func returns the asteroid life"""
        return self.__life

    def set_life(self, new_life):
        """This func updates the asteroids life"""
        self.__life = new_life

    def get_torpedo_lst(self):
        """This func returns the torpedo list"""
        return self.__torpedo_lst

    def set_torpedo_lst(self, new_list):
        """This func updates the torpedoes list"""
        self.__torpedo_lst = new_list

    def get_asteroids_list(self):
        """This func returns the asteroids list"""
        return self.__asteroids_lst

    def set_asteroids_list(self, new_lst):
        """This func updates the asteroids list"""
        self.__asteroids_lst = new_lst

    def asteroids_list(self):
        """This function creates a list of asteroids, and for each one of the
        asteroids, it returns the new location according to the equotation"""
        for num in range(self.get_asteroids_amnt()):
            x_loc_ast = randint(self.screen_min_x, self.screen_max_x)
            y_loc_ast = randint(self.screen_min_y, self.screen_max_y)
            x_ast_speed = randint(-MAX_SPEED_AST, MAX_SPEED_AST)
            y_ast_speed = randint(-MAX_SPEED_AST, MAX_SPEED_AST)
            while self._ship.get_x_loc() == x_loc_ast or \
                            self._ship.get_y_loc() == y_loc_ast:
                if self._ship.get_x_loc() == x_loc_ast:
                    x_loc_ast = randint(self.screen_min_x, self.screen_max_x)
                else:
                    y_loc_ast = randint(self.screen_min_y, self.screen_max_y)
            asteroid1 = asteroid.Asteroid(x_loc_ast, y_loc_ast,
                                          x_ast_speed, y_ast_speed,
                                          INIT_SIZE_AST)
            self.__asteroids_lst.append(asteroid1)
            self._screen.register_asteroid(asteroid1, INIT_SIZE_AST)

    def run(self):
        """"This func starts the game"""
        self._do_loop()
        self._screen.start_screen()

    def _do_loop(self):
        """This func calls game loop"""
        # You don't need to change this method!
        self._game_loop()
        # Set the timer to go off again
        self._screen.update()
        self._screen.ontimer(self._do_loop, 5)

    def move_x(self, obj):
        """This function changes the location of coordinate X"""
        x = obj.get_x_loc()
        speed_x = obj.get_x_sped()
        new_x_cord = ((speed_x + x - Screen.SCREEN_MIN_X) %
                      (self.get_delta_x())) + Screen.SCREEN_MIN_X
        obj.set_x_loc(new_x_cord)

    def move_y(self, obj):
        """This function changes the location of coordinate Y"""
        y = obj.get_y_loc()
        speed_y = obj.get_y_sped()
        new_y_cord = ((speed_y + y - Screen.SCREEN_MIN_Y) %
                      (self.get_delta_y())) + Screen.SCREEN_MIN_Y
        obj.set_y_loc(new_y_cord)

    def change_direction(self):
        """This function changes the direction of the ship folloeing the user's
        presses"""
        cur_heading = self._ship.get_heading()
        if self._screen.is_right_pressed() is True:
            self._ship.set_heading(cur_heading + MOVE_RIGHT)
        elif self._screen.is_left_pressed() is True:
            self._ship.set_heading(cur_heading + MOVE_LEFT)

    def ship_acceleration(self):
        """This func accelerates the ship velocity, following the user's
        presses"""
        cur_speed_x = self._ship.get_x_sped()
        cur_speed_y = self._ship.get_y_sped()
        cur_heading = math.radians(self._ship.get_heading())
        new_x_speed = cur_speed_x + math.cos(cur_heading)
        new_y_speed = cur_speed_y + math.sin(cur_heading)
        self._ship.set_y_sped(new_y_speed)
        self._ship.set_x_sped(new_x_speed)

    def create_torpedo(self):
        """This func creates a torpedo list, and appends the new torpedo to a
        list"""
        x_loc = self._ship.get_x_loc()
        y_loc = self._ship.get_y_loc()
        x_ship_speed = self._ship.get_x_sped()
        y_ship_speed = self._ship.get_y_sped()
        heading = self._ship.get_heading()
        rad_head = math.radians(heading)
        x_speed = x_ship_speed + ACCELRRATION_FACTOR * math.cos(rad_head)
        y_speed = y_ship_speed + ACCELRRATION_FACTOR * math.sin(rad_head)
        torpedo1 = torpedo.Torpedo(x_loc, x_speed, y_loc, y_speed, heading)
        self.__torpedo_lst.append(torpedo1)
        self._screen.register_torpedo(torpedo1)

    def draw_ship(self):
        """"This func draws rhe ship in each iteration"""
        self.change_direction()
        self.move_x(self._ship)
        self.move_y(self._ship)
        x = self._ship.get_x_loc()
        y = self._ship.get_y_loc()
        heading = self._ship.get_heading()
        self._screen.draw_ship(x, y, heading)

    def draw_ast(self):
        """"This func draws rhe asteroid in each iteration"""
        for asteroid in self.__asteroids_lst:
            self.move_x(asteroid)
            self.move_y(asteroid)
            x_astr = asteroid.get_x_loc()
            y_astr = asteroid.get_y_loc()
            self._screen.draw_asteroid(asteroid, x_astr, y_astr)

    def create_splitted_asteroid(self, asteroid1, torpedo,new_size):
        """This function splits an asteroid to 2 asteroids, and then it adds
        the asteroids list"""
        x = asteroid1.get_x_loc()
        y = asteroid1.get_y_loc()
        x_speed_ast = asteroid1.get_x_sped()
        y_speed_ast = asteroid1.get_y_sped()
        x_speed_tor = torpedo.get_x_sped()
        y_speed_tor = torpedo.get_y_sped()
        new_x_speed = (x_speed_tor + x_speed_ast) / math.sqrt((x_speed_ast
                                                    ** 2) + (y_speed_ast) ** 2)
        new_y_speed = (y_speed_tor + y_speed_ast) / math.sqrt(((x_speed_ast)
                                                    ** 2) + (y_speed_ast) ** 2)
        new_ast_1 = asteroid.Asteroid(x, y, new_x_speed, new_y_speed, new_size)
        self.__asteroids_lst.append(new_ast_1)
        self._screen.register_asteroid(new_ast_1, new_size)
        new_x_speed = (x_speed_tor - x_speed_ast) / math.sqrt(((x_speed_ast)
                                                 ** 2) + ( y_speed_ast) ** 2)

        new_y_speed = (y_speed_tor - y_speed_ast) / math.sqrt(((x_speed_ast)
                                                ** 2) + (y_speed_ast) ** 2)
        new_ast_2 = asteroid.Asteroid(x, y, new_x_speed, new_y_speed,
                                    new_size)
        self.__asteroids_lst.append(new_ast_2)
        self._screen.register_asteroid(new_ast_2, new_size)

    def torpedo_asteroid_intersect(self, asteroid1, torpedo):
        """This function checks if the torpedo has intersection with a
        asteroid and scores the user by the game score rules """
        size = asteroid1.get_size()
        score = self.score_get()
        if size == 1:
            self.score_set(score + SIZE_ONE_AST_POINTS)
            self._screen.set_score(score + SIZE_ONE_AST_POINTS)
        elif size ==2:
            self.create_splitted_asteroid(asteroid1, torpedo,1)
            self.score_set(score + SIZE_TWO_AST_POINTS)
            self._screen.set_score(score + SIZE_TWO_AST_POINTS)
        elif size == 3:
            self.create_splitted_asteroid(asteroid1, torpedo,2)
            self.score_set(score + SIZE_THREE_AST_POINTS)
            self._screen.set_score(score + SIZE_THREE_AST_POINTS)


    def torpedo_run(self, torpedo):
        """"This function checks if the torpedo got a valid value of life. and
        if so- it moves and its fields change. Otherwise, it removes it from
         the list and unregisters the torpedo."""

        if torpedo.get_life() < 200:
            self.move_x(torpedo)
            self.move_y(torpedo)
            torpedo.increase_life()
            x_loc = torpedo.get_x_loc()
            y_loc = torpedo.get_y_loc()
            heading = torpedo.get_heading()
            self._screen.draw_torpedo(torpedo, x_loc, y_loc, heading)
        else:
            self.__torpedo_lst.remove(torpedo)
            self._screen.unregister_torpedo(torpedo)

    def ship_intersect(self):
        """This function checks if the shio has intersection with a
               asteroiid and removes the asteroid fron=m the list"""
        for asteroid in self.__asteroids_lst:
            if asteroid.has_intersection(self._ship):
                self._screen.show_message(ERROR_INTERSECT_TITLE,
                                          ERROR_INTERSECT_MSG)
                self._screen.remove_life()
                self.__life -= 1
                self._ship.set_x_sped(INIT_SPEED)
                self._ship.set_y_sped(INIT_SPEED)
                self._screen.unregister_asteroid(asteroid)
                self.__asteroids_lst.remove(asteroid)

    def torpedo_cycle(self):
        """This function is the cycle that each torpedo goes through during
                the gmae: for each torpedo in the torpedo list it cheks if there has
                been an intersection, and if so, it removes the torpedo from
                the screen"""
        for torpedo in self.__torpedo_lst:
            self.torpedo_run(torpedo)
            for asteroid in self.__asteroids_lst:
                if asteroid.has_intersection(torpedo):
                    self.torpedo_asteroid_intersect(asteroid, torpedo)
                    self._screen.unregister_asteroid(asteroid)
                    self.__asteroids_lst.remove(asteroid)

    def keys_pressed(self):
        """This func calls other functions that check the keys that were
                pressed by the user and calls the adequate functions"""
        if self._screen.is_up_pressed():
            self.ship_acceleration()
        if self._screen.is_space_pressed():
            if len(self.__torpedo_lst) <=14:
                self.create_torpedo()

    def end_game(self):
        """"This function cheks if the lives of the asteroids are gone, and if
                so it shows an end of the game message"""
        if self.__life < 1:
            self._screen.show_message(END_OF_GAME, ERROR_LIFE)
        elif len(self.__asteroids_lst) < 1:
            self._screen.show_message(END_OF_GAME, WIN)
        elif self._screen.should_end():
            self._screen.show_message(END_OF_GAME, QUIT)
        self._screen.end_game()
        sys.exit()

    def _game_loop(self):
        """This function is the main loop that runs the game"""
        if not self.__life < 1 and not len(self.__asteroids_lst) < 1 and not \
                self._screen.should_end():
            self.draw_ship()
            self.draw_ast()
            self.keys_pressed()
            self.ship_intersect()
            self.torpedo_cycle()
        else:
            self.end_game()


def main(amnt):
    runner = GameRunner(amnt)
    runner.run()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(DEFAULT_ASTEROIDS_NUM)
