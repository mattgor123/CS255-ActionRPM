import pygame
import Tile


class Wall(Tile.Tile):
    wall_img = None

    def __init__(self, map_x, map_y):
        Tile.Tile.__init__(self, True)

        # initialize wall image
        if Wall.wall_img is None:
            Wall.wall_img = pygame.image.load(
                "images/sprites/wall/h_wall.png").convert_alpha()
        self.image = Wall.wall_img
        self.rect = pygame.Rect(map_x, map_y, 10, 10)
        # self.rect.center = location

    def __str__(self):
        return 'w'
