import pygame


class Key(pygame.sprite.Sprite):
    key_img = None

    def __init__(self, loc):
        pygame.sprite.Sprite.__init__(self)
        # initialize wall image
        if Key.key_img is None:
            Key.key_img = pygame.image.load(
                "images/sprites/key/key.png").convert_alpha()
        self.image = Key.key_img
        self.rect = self.image.get_rect()
        self.rect.center = loc
        # self.rect.center = location

    def update(self, loc):
        self.rect.center = loc
