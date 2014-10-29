import pygame
import Tile


class Wall(Tile.Tile):
    wall_0_img = None
    wall_1_img = None
    wall_2_img = None
    wall_3_img = None
    wall_4_img = None
    wall_5_img = None
    wall_6_img = None
    wall_7_img = None
    wall_8_img = None
    wall_9_img = None
    has_images = False

    def __init__(self, x, y, num):
        Tile.Tile.__init__(self, 3)

        # initialize wall image
        if not Wall.has_images:
            Wall.set_images()

        if num == 0:
            self.image = Wall.wall_0_img
        elif num == 1:
            self.image = Wall.wall_1_img
        elif num == 2:
            self.image = Wall.wall_2_img
        elif num == 3:
            self.image = Wall.wall_3_img
        elif num == 4:
            self.image = Wall.wall_4_img
        elif num == 5:
            self.image = Wall.wall_5_img
        elif num == 6:
            self.image = Wall.wall_6_img
        elif num == 7:
            self.image = Wall.wall_7_img
        elif num == 8:
            self.image = Wall.wall_8_img
        elif num == 9:
            self.image = Wall.wall_9_img

        self.rect = self.image.get_rect()
        # self.rect.center = location
        self.x = x
        self.y = y

    def __str__(self):
        return 'w'

    @staticmethod
    def set_images():
        Wall.wall_0_img = pygame.image.load(
            "images/sprites/buildings/building_0.png").convert_alpha()
        Wall.wall_1_img = pygame.image.load(
            "images/sprites/buildings/building_1.png").convert_alpha()
        Wall.wall_2_img = pygame.image.load(
            "images/sprites/buildings/building_2.png").convert_alpha()
        Wall.wall_3_img = pygame.image.load(
            "images/sprites/buildings/building_3.png").convert_alpha()
        Wall.wall_4_img = pygame.image.load(
            "images/sprites/buildings/building_4.png").convert_alpha()
        Wall.wall_5_img = pygame.image.load(
            "images/sprites/buildings/building_5.png").convert_alpha()
        Wall.wall_6_img = pygame.image.load(
            "images/sprites/buildings/building_6.png").convert_alpha()
        Wall.wall_7_img = pygame.image.load(
            "images/sprites/buildings/building_7.png").convert_alpha()
        Wall.wall_8_img = pygame.image.load(
            "images/sprites/buildings/building_8.png").convert_alpha()
        Wall.wall_9_img = pygame.image.load(
            "images/sprites/buildings/building_9.png").convert_alpha()
        Wall.has_images = True
