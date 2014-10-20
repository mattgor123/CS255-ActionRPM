import pygame


class Health(pygame.sprite.Sprite):
    Health_img = None

    def __init__(self, loc):
        pygame.sprite.Sprite.__init__(self)
        # initialize wall image
        if Health.Health_img is None:
            Health.Health_img = pygame.image.load(
                "images/sprites/health/health.png").convert_alpha()
        self.image = Health.Health_img
        self.rect = self.image.get_rect()
        self.rect.center = loc
        # self.rect.center = location

    def update(self, loc):
        self.rect.center = loc
