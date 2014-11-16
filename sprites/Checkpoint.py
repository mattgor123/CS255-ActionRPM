import pygame


class Checkpoint(pygame.sprite.Sprite):
    up_img = None
    left_img = None
    right_img = None
    finish = None
    has_images = False

    def __init__(self, number, location):
        pygame.sprite.Sprite.__init__(self)
        if not Checkpoint.has_images:
            Checkpoint.set_images()
        if number == 1:
            self.image = Checkpoint.up_img
        if number == 2:
            self.image = Checkpoint.left_img
        if number == 3:
            self.image = Checkpoint.right_img
        if number == 4:
            self.image = Checkpoint.finish
        self.number = number
        self.rect = self.image.get_rect()
        self.rect.topleft = location
        self.x = location[0]
        self.y = location[1]

    @staticmethod
    def set_images():
        Checkpoint.up_img = pygame.image.load(
            "images/sprites/street/checkpoint.png")
        Checkpoint.left_img = pygame.image.load(
            "images/sprites/street/checkpoint_going_left.png")
        Checkpoint.right_img = pygame.image.load(
            "images/sprites/street/checkpoint_going_right.png")
        Checkpoint.finish = pygame.image.load(
            "images/sprites/street/finish.png")
        Checkpoint.has_images = True

    @staticmethod
    def get_strength(self):
        return -1
