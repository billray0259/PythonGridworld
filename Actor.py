import pygame
from Location import Location
import random
import math
import random

class Actor:
    def __init__(self, location, grid, icon="bug.gif"):
        self._location = location
        self._direction = 0
        self.grid = grid
        self._icon = pygame.image.load(icon)
        self._icon = pygame.transform.scale(self._icon,
                                            (int(grid.grid_pixel_size * 0.8), int(grid.grid_pixel_size * 0.8)))
        self.step = 0

    def act(self):
        self.forward()
        self.direction += random.randint(-45, 45)

    def put_self_in_grid(self, grid):
        grid.add_actor(self)
        self.grid = grid

    def remove_self_from_grid(self):
        self.grid.remove_actor()

    def forward(self):
        self.move_to(self.get_location_in_direction(self.direction))

    def move_to(self, location):
        if self.grid.is_valid(location):
            self.location = location

    def can_move(self, direction):
        location = self.get_location_in_direction(direction)
        return self.grid.is_valid(location) and self.grid.is_empty(
            location)

    def get_location_in_direction(self, direction):
        solid_direction = 45 * round(direction / 45) % 360
        row = self.location.row
        col = self.location.col
        if solid_direction == 0:
            col += 1
        elif solid_direction == 45:
            col += 1
            row -= 1
        elif solid_direction == 90:
            row -= 1
        elif solid_direction == 135:
            col -= 1
            row -= 1
        elif solid_direction == 180:
            col -= 1
        elif solid_direction == 225:
            col -= 1
            row += 1
        elif solid_direction == 270:
            row += 1
        elif solid_direction == 315:
            col += 1
            row += 1
        return Location(row, col)

    def get_empty_adjacent_locations(self):
        locs = []
        for i1 in range(3):
            for j1 in range(3):
                r = self.location.row + i1 - 1
                c = self.location.col + j1 - 1
                loc = Location(r, c)
                if self.grid.is_valid(loc) and self.grid.is_empty(loc):
                    locs.append(loc)
        return locs

    def get_direction_towards(self, target_loc):
        angle = math.degrees(math.atan2(target_loc.row - self.location.row, self.location.col - target_loc.col)) + 180
        return angle

    def turn(self, amount):
        self.direction += amount

    def turn_right(self):
        self.direction -= 45

    def turn_left(self):
        self.direction += 45

    @property
    def location(self):
        return self._location

    @property
    def direction(self):
        return self._direction

    @property
    def icon(self):
        return self._icon

    @direction.setter
    def direction(self, direction):
        self._direction = direction

    @location.setter
    def location(self, location):
        self._location = location

    @icon.setter
    def icon(self, icon):
        self._icon = icon

    def update_icon_path(self, path):
        self._icon = pygame.image.load(path)
        self._icon = pygame.transform.scale(self._icon, (self.grid.grid_pixel_size, self.grid.grid_pixel_size))
