import pygame


class Wall(pygame.sprite.Sprite):
    wall_img = None

    def __init__(self, location):
        pygame.sprite.Sprite.__init__(self)

        # initialize wall image
        if Wall.wall_img is None:
            Wall.wall_img = pygame.image.load(
                "images/sprites/wall/h_wall.png").convert_alpha()
        self.image = Wall.wall_img
        self.rect = self.image.get_rect()
        self.rect.center = location
