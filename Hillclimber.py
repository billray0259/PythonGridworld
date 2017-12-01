import pygame
from Grid import Grid
from Location import Location
from Robot import Robot
from SmellyMan import SmellyMan
from Rock import Rock
from Sniffer import Sniffer
from Bug import Bug
import random
import math
import time


class SmellyGrid(Grid):
    def __init__(self, row, col, grid_pixel_size=40, ticks_per_second=5):
        Grid.__init__(self, row, col, grid_pixel_size=grid_pixel_size, ticks_per_second=ticks_per_second)
        self.smells = {}

    def add_actor(self, actor):
        Grid.add_actor(self, actor)
        if type(actor) is not Rock and str(type(actor)) not in self.smells:
            self.smells[str(type(actor))] = [[0 for i in range(self.col)] for i in range(self.row)]

    def act_actors(self):
        Grid.act_actors(self)
        for i in range(1):
            self.update_smells()

    def update_smells(self):
        new_smells = {}
        for actor_type in self.smells:
            new_smells[actor_type] = [[0 for i in range(self.col)] for i in range(self.row)]
            for r in range(len(self.smells[actor_type])):
                for c in range(len(self.smells[actor_type][r])):
                    if self.is_empty(Location(r, c)):
                        total_adjacent_smell = 0
                        num_adjacent_smell = 9
                        for i1 in range(3):
                            for j1 in range(3):
                                i = i1 - 1
                                j = j1 - 1
                                sample_loc = Location(r + i, c + j)
                                if not self.is_valid(
                                        sample_loc) or (not self.is_empty(sample_loc) and type(self.grid[sample_loc.row][sample_loc.col]) is Rock):
                                    if self.is_valid(sample_loc):
                                        num_adjacent_smell -= 1
                                else:
                                    total_adjacent_smell += self.smells[actor_type][r + i][c + j]
                        if num_adjacent_smell != 0:
                            new_smells[actor_type][r][c] = total_adjacent_smell / num_adjacent_smell * 0.97
                        else:
                            new_smells[actor_type][r][c] = self.smells[actor_type][r][c] * 0.97
                            # new_smells[r][c] = new_smells[r][c] * 0.99
        for actor in self.actors:
            if type(actor) is not Rock:
                new_smells[str(type(actor))][actor.location.row][actor.location.col] = 1

        self.smells = new_smells

    def draw(self):
        self.surface.fill((255, 255, 255))
        # draw grid lines
        for col in range(0, len(self.grid[0])):
            pygame.draw.line(self.surface, (0, 0, 0), (col * self.grid_pixel_size, 0),
                             (col * self.grid_pixel_size, self.pixel_height))
        for row in range(0, len(self.grid)):
            pygame.draw.line(self.surface, (0, 0, 0), (0, row * self.grid_pixel_size),
                             (self.pixel_width, row * self.grid_pixel_size))

        # draw actors
        for row in range(0, len(self.grid)):
            for col in range(0, len(self.grid[row])):
                actor = self.grid[row][col]
                if actor is not None:
                    drawing_direction = 45 * round(actor.direction / 45) % 360 - 90
                    icon = pygame.transform.rotate(actor.icon, drawing_direction)
                    # I draw them kinda weirdly to make the icons line up in the grid boxes and
                    # not shift around too much when the images get rotated
                    if drawing_direction % 90 == 0:
                        self.surface.blit(icon,
                                          (col * self.grid_pixel_size + int(self.grid_pixel_size * 0.1),
                                           row * self.grid_pixel_size + int(self.grid_pixel_size * 0.1)))
                    else:
                        self.surface.blit(icon,
                                          (col * self.grid_pixel_size - int(self.grid_pixel_size * 0.05),
                                           row * self.grid_pixel_size - int(self.grid_pixel_size * 0.05)))
                smelly_tile = pygame.Surface((self.grid_pixel_size, self.grid_pixel_size))
                total_color = [0, 0, 0]
                for actor_type in self.smells:
                    smell = self.smells[actor_type][row][col]
                    color_intensity = 0
                    if smell > 0:
                        color_intensity = math.log10(10 * smell)
                    if color_intensity < 0:
                        color_intensity = 0

                    rand = random.Random(actor_type)
                    total_color[0] += color_intensity * int(rand.random() * 255)
                    total_color[1] += color_intensity * int(rand.random() * 255)
                    total_color[2] += color_intensity * int(rand.random() * 255)

                r = total_color[0] / len(self.smells)
                g = total_color[1] / len(self.smells)
                b = total_color[2] / len(self.smells)

                smelly_tile.set_alpha(225)

                # else:
                #     smelly_tile.set_alpha(0)
                # smelly_tile.set_alpha(200 * self.smells[row][col])
                # print(rgb)
                smelly_tile.fill((r, g, b))
                self.surface.blit(smelly_tile, (col * self.grid_pixel_size, row * self.grid_pixel_size))
        pygame.display.update()


width = 40
height = 20
grid = SmellyGrid(height, width, grid_pixel_size=40, ticks_per_second=30)

for i in range(round(width * height * 0.4)):
    loc = Location(random.randint(0, height - 1), random.randint(0, width - 1))
    grid.add_actor(Rock(loc, grid))

for j in range(4):
    grid.add_actor(SmellyMan(Location(random.randint(0, height - 1), random.randint(0, width - 1)), grid))
    grid.add_actor(Bug(Location(random.randint(0, height - 1), random.randint(0, width - 1)), grid))
    grid.add_actor(Sniffer(Location(random.randint(0, height - 1), random.randint(0, width - 1)), grid, "instructions.txt"))
grid.start()

# When I left off I had just started testing things. when I run this there is no smellyman or smells... not sure why
