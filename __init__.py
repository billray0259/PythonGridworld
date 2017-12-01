from Grid import Grid
from Actor import Actor
from Bug import Bug
from Location import Location
from Rock import Rock
from Robot import Robot

import random

width = 15
height = 15
grid = Grid(height, width, grid_pixel_size = 50, ticks_per_second = 4)

# for i in range(100):
#     grid.add_actor(Rock(Location(random.randint(0, height - 1), random.randint(0, width - 1)), grid))


grid.add_actor(Robot(Location(0, 0), grid, "instructions.txt"))
# grid.add_actor(Bug(Location(6, 2), grid))


grid.start()