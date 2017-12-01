import pygame


class Grid:
    def __init__(self, row, col, grid_pixel_size=40, ticks_per_second=5):
        # initialize the grid to be a 2D, row by col, matrix filled with None (python's version of null)
        self.grid = [[None for i in range(col)] for i in range(row)]
        self.row = row
        self.col = col
        self.grid_pixel_size = grid_pixel_size
        self.pixel_width = col * grid_pixel_size
        self.pixel_height = row * grid_pixel_size
        self.surface = pygame.display.set_mode((self.pixel_width, self.pixel_height))
        self.clock = pygame.time.Clock()
        self.step = 0
        self.ticks_per_second = ticks_per_second
        self.actors = []

    def start(self):
        pygame.init()
        pygame.display.set_caption("Grid World")
        running = True
        while running:
            # print("step")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.act_actors()
            self.draw()
            self.clock.tick(self.ticks_per_second)
            self.step += 1

    def act_actors(self):
        for row in range(0, len(self.grid)):
            for col in range(0, len(self.grid[row])):
                actor = self.grid[row][col]
                if not actor is None and actor.step <= self.step:
                    actor.act()
                    actor.step += 1
                    self.grid[row][col] = None
                    self.grid[actor.location.row][actor.location.col] = actor

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
                if not actor is None:
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
        pygame.display.update()

    def add_actor(self, actor):
        """Adds an actor to the grid at location row, col"""
        if self.grid[actor.location.row][actor.location.col] is not None:
            self.actors.remove(self.grid[actor.location.row][actor.location.col])
        self.grid[actor.location.row][actor.location.col] = actor
        self.actors.append(actor)
        actor.grid = self

    def remove_actor(self, location):
        """Removes the actor at location. Returns False if there is no actor at location"""
        if self.grid[location.row][location.col] is None:
            return False
        else:
            self.actors.remove(self.grid[location.row][location.col])
            self.grid[location.row][location.col] = None
            return True

    def is_valid(self, location):
        """Returns true if the location is inside the grid"""
        return location.row >= 0 and location.row < self.row and location.col >= 0 and location.col < self.col

    def is_empty(self, location):
        """Returns true if the location is empty"""
        return self.grid[location.row][location.col] is None

    def rotate_around_center(image, angle):
        """rotate an image while keeping its center and size"""
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image
