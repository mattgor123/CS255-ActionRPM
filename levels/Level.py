import pygame
import sprites.Enemy as Enemy
from states.Constants import Constants
import map.Map as Map


# Must overwrite self.set_tiles()
# Must overwrite self.game_over()
class Level(object):

    def __init__(self, player):
        self.map = None
        self.enemies = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.player = player

    def update(self, interval):
        #Check the health to see if we are done
        if self.player.health <= 0:
            #labels.clear(Constants.SCREEN,background)
            pygame.display.update()
            self.game_over(True)

        #Set the tiles for what we need right now
        self.set_tiles()

        #This code does the player collision and returns the player coordinates
        player_coordinates = self.player_collision()

        #Update our stuff
        for enemy in self.enemies:
            enemy.update(interval, player_coordinates)

    # draws the enemies and items
    # does not need a display update since Play calls that
    def draw(self, background):
        self.enemies.clear(Constants.SCREEN, background)
        self.items.clear(Constants.SCREEN, background)

        self.enemies.draw(Constants.SCREEN)
        self.items.draw(Constants.SCREEN)

    def player_collision(self):
            player_coordinates = self.player.get_coordinates()
            #Check if player has EZPass, if so, open the TollBooth
            if not self.is_beatable:
                if "ezpass" in self.player.inventory:
                    #Very hackish way to do this; the score should be
                    #  on the player, so when we collect collectables
                    #  or collide, we can easily update the score.
                    # But we have more pressing things to do now.
                    self.player.score += 50
                    self.is_beatable = True
                    for openable in self.map.openables:
                        if openable.__str__() == "t":
                            openable.open()

            self.health = self.player.calculate_health()

            #Iterate through items and check if they are colliding
            #With the player
            for c in self.items.sprites():
                if c.rect.colliderect(self.player.rect):
                    self.player.add_to_inventory(c)
                    c.collect()

            collidables_on_screen = self.map.get_tiles(self.player.x,
                                                       self.player.y)
            for enemy in self.enemies:
                collidables_on_screen.append(enemy)

            #Here goes collision
            collision_fixed = False
            #Go through all of the collidable rects around the player
            for r in collidables_on_screen:
                #A strength >= 0 indicates a collidable object
                #  -1 isnt collidable
                if r.get_strength() >= 0:
                    #This same if statement is repeated for all midpoints
                    #Checking if the midpoint of the car is in the other rect
                    #This midpoint check tells us how to fix the car's position
                    if (r.rect.collidepoint(self.player.rect.midbottom)):
                        damage_to_do = r.get_strength()
                        self.player.rect.bottom = r.rect.top
                        collision_fixed = True
                        self.player.speed = Constants.PLAYER_MIN_SPEED
                        self.player.y -= .01

                    if (r.rect.collidepoint(self.player.rect.midleft)):
                        damage_to_do = r.get_strength()
                        self.player.rect.left = r.rect.right
                        collision_fixed = True
                        self.player.speed = Constants.PLAYER_MIN_SPEED
                        self.player.x += .01

                    if (r.rect.collidepoint(self.player.rect.midright)):
                        damage_to_do = r.get_strength()
                        self.player.rect.right = r.rect.left
                        collision_fixed = True
                        self.player.speed = Constants.PLAYER_MIN_SPEED
                        self.player.x -= .01

                    if (r.rect.collidepoint(self.player.rect.midtop)):
                        damage_to_do = r.get_strength()
                        self.player.rect.top = r.rect.bottom
                        collision_fixed = True
                        self.player.speed = Constants.PLAYER_MIN_SPEED
                        self.player.y += .01

                    #These collision if statements are to fix hitting corners
                    #Only happens if there wasnt a collision with a
                    #center of the car
                    if (not collision_fixed and r.rect.collidepoint(
                            self.player.rect.topright)):
                        damage_to_do = r.get_strength()
                        collision_fixed = True
                        self.player.rect.right = r.rect.left
                        self.player.speed = Constants.PLAYER_MIN_SPEED
                        self.player.x -= .01

                    if (not collision_fixed and r.rect.collidepoint(
                            self.player.rect.bottomright)):
                        damage_to_do = r.get_strength()
                        collision_fixed = True
                        self.player.rect.right = r.rect.left
                        self.player.speed = Constants.PLAYER_MIN_SPEED
                        self.player.x -= .01

                    if (not collision_fixed and r.rect.collidepoint(
                            self.player.rect.topleft)):
                        damage_to_do = r.get_strength()
                        collision_fixed = True
                        self.player.rect.left = r.rect.right
                        self.player.speed = Constants.PLAYER_MIN_SPEED
                        self.player.x += .01
                    if (not collision_fixed and r.rect.collidepoint(
                            self.player.rect.bottomleft)):
                        damage_to_do = r.get_strength()
                        collision_fixed = True
                        self.player.rect.left = r.rect.right
                        self.player.speed = Constants.PLAYER_MIN_SPEED
                        self.player.x += .01

                if collision_fixed:
                    #This if statement tells us that the player hit the
                    #Boss and it should inflict damage on the boss
                    if(damage_to_do == 0 and type(r) is Enemy.Boss_1):
                        r.hurt(3)

                    #Do the damage as prescribed by the collided box
                    self.player.damage += damage_to_do
                    #Play that terrible crash sound
                    #player.crash.play()
                    #If we hit an enemy, make the enemy stop
                    if type(r) is Enemy.Enemy:
                        r.stop()
                    #Only do one collision per cycle
                    return player_coordinates

    def game_over(self, died):
        print "Super Level Game Over"

