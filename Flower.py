from Actor import Actor


class Flower(Actor):
    def __init__(self, location, grid):
        Actor.__init__(self, location, grid, icon="car.png")

    def act(self):
        pass