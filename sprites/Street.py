import pygame


class Street(pygame.sprite.Sprite):
    street_img = None

    def __init__(self, location):
        pygame.sprite.Sprite.__init__(self)

        # initialize street image
        if Street.street_img is None:
            Street.wall_img = pygame.image.load(
                "images/sprites/street/w_wall.png").convert_alpha()
        self.image = Street.street_img
        self.rect = self.image.get_rect()
        self.rect.center = location
