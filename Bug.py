from Actor import Actor
from Flower import Flower
from Location import Location


class Bug(Actor):
    def __init__(self, location, grid):
        Actor.__init__(self, location, grid, icon="Bug.gif")

    def act(self):
        if self.can_move(self.direction):
            self.forward()
        else:
            self.turn_left()