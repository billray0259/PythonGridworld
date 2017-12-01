from Actor import Actor
import random

class SmellyMan(Actor):
    def __init__(self, location, grid):
        Actor.__init__(self, location, grid, icon="car.png")



    def act(self):
        if random.random() < 0.3 or not self.can_move(self.direction):
            if random.random() < 0.55:
                self.turn_right()
            else:
                self.turn_left()
        else:
            self.forward()
