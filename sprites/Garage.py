import pygame


class Garage(pygame.sprite.Sprite):
    g_img_closed = None
    g_img_opened = None
    is_opened = None

    def __init__(self, loc):
        pygame.sprite.Sprite.__init__(self)
        # initialize wall image
        if Garage.g_img_closed is None:
            Garage.g_img_closed = pygame.image.load(
                "images/sprites/garage/garage_closed.png").convert_alpha()
        if Garage.g_img_opened is None:
            Garage.g_img_opened = pygame.image.load(
                "images/sprites/garage/garage_opened.png").convert_alpha()
        self.image = Garage.g_img_closed
        self.rect = self.image.get_rect()
        self.rect.center = loc
        Garage.is_opened = False
        # self.rect.center = location

    def isOpened(self):
        return self.is_opened

    def isCollidable(self):
        return not self.is_opened

    def open_door(self):
        self.image = Garage.g_img_opened
        self.rect = self.image.get_rect()
        self.is_opened = True

    def update(self, loc):
        self.rect.center = loc
