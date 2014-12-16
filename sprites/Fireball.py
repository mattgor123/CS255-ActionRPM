import pygame
import sprites.Wall as Wall
import sprites.Enemy as Enemy
import Player


# This is the Racer's weapon
class Fireball(pygame.sprite.Sprite):
    image = None

    def __init__(self, speed, initial_direction, location, duration, strength, initial_map):
        pygame.sprite.Sprite.__init__(self)
        if Fireball.image is None:
            Fireball.image = pygame.image.load(
                "images/sprites/fireball.png").convert_alpha()
        self.image = Fireball.image
        self.x = location[0]
        self.y = location[1]
        self.rect = self.image.get_rect()
        self.rect.topleft = initial_map
        self.duration = duration
        self.direction = initial_direction
        self.speed = speed
        self.strength = strength

    def get_strength(self):
        return self.strength

    def update(self, interval, player_coordinates):
        self.duration -= 1
        if self.duration <= 0:
            self.kill()
        else:
            self.move(interval)

    def move(self, interval):
        if self.direction == "upleft":
            self.x -= self.speed * interval * .7071  # 1/Sqrt 2
            self.y -= self.speed * interval * .7071
        elif self.direction == "downleft":
            self.x -= self.speed * interval * .7071
            self.y += self.speed * interval * .7071
        elif self.direction == "upright":
            self.x += self.speed * interval * .7071
            self.y -= self.speed * interval * .7071
        elif self.direction == "downright":
            self.x += self.speed * interval * .7071
            self.y += self.speed * interval * .7071
        elif self.direction == "up":
            self.y -= self.speed * interval
        elif self.direction == "down":
            self.y += self.speed * interval
        elif self.direction == "left":
            self.x -= self.speed * interval
        elif self.direction == "right":
            self.x += self.speed * interval

    def bounce(self, is_vertical):
        #If you hit a vertical wall, you want to flip just horizontal direction
        if is_vertical:
            if self.direction == "upright":
                self.direction = "upleft"
            elif self.direction == "upleft":
                self.direction = "upright"
            elif self.direction == "downleft":
                self.direction = "downright"
            elif self.direction == "downright":
                self.direction = "downleft"
        #You hit a horizontal wall, you want to flip just vertical direction
        else:
            if self.direction == "upright":
                self.direction = "downright"
            elif self.direction == "upleft":
                self.direction = "downleft"
            elif self.direction == "downleft":
                self.direction = "upleft"
            elif self.direction == "downright":
                self.direction = "upright"

    def collide(self, source, object):
        if type(object) == Wall.Wall:
            self.kill()
        elif type(object) == Enemy.Keg:
            object.set_dead()
            object.kill()
            self.kill()

        if type(source) == Player.Player:
            if type(object) == Enemy.Keg:
                source.score += 100
