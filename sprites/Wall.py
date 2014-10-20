import pygame
import Tile


class Wall(Tile.Tile):
    wall_img = None

    def __init__(self, x, y):
        Tile.Tile.__init__(self, 10)

        # initialize wall image
        if Wall.wall_img is None:
            Wall.wall_img = pygame.image.load(
                "images/sprites/wall/h_wall.png").convert_alpha()
        self.image = Wall.wall_img
        self.rect = self.image.get_rect()
        # self.rect.center = location
        self.x = x
        self.y = y

    def __str__(self):
        return 'w'
