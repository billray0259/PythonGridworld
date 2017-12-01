from Actor import Actor

class Rock(Actor):
    def __init__(self, location, grid):
        Actor.__init__(self, location, grid, icon="rock.png")

    def act(self):
        pass