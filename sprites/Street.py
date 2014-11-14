import pygame

import Tile


class Street(Tile.Tile):
    h_img = None
    v_img = None
    o_img = None
    p_img = None
    l_img = None
    sc_img = None
    e_img = None
    has_images = False

    def __init__(self, x, y, type):
        Tile.Tile.__init__(self, -1)
        # initialize street image
        if not Street.has_images:
            Street.set_images()

        if type == "horizontal":
            self.image = Street.h_img
        elif type == "vertical":
            self.image = Street.v_img
        elif type == "l":
            self.image = Street.l_img
        elif type == ";":
            self.image = Street.sc_img
        elif type == "o":
            self.image = Street.o_img
        elif type == "p":
            self.image = Street.p_img
        elif type == "empty":
            self.image = Street.e_img

        self.rect = self.image.get_rect()
        # self.rect.center = location
        self.x = x
        self.y = y

    def __str__(self):
        return 's'

    @staticmethod
    def set_images():
        Street.h_img = pygame.image.load(
            "images/sprites/street/horizontal_street.png").convert_alpha()
        Street.v_img = pygame.image.load(
            "images/sprites/street/vertical_street.png").convert_alpha()
        Street.l_img = pygame.image.load(
            "images/sprites/street/l_street.png").convert_alpha()
        Street.sc_img = pygame.image.load(
            "images/sprites/street/semicolon_street.png").convert_alpha()
        Street.o_img = pygame.image.load(
            "images/sprites/street/o_street.png").convert_alpha()
        Street.p_img = pygame.image.load(
            "images/sprites/street/p_street.png").convert_alpha()
        Street.e_img = pygame.image.load(
            "images/sprites/street/empty_street.png").convert_alpha()
        Street.has_images = True
