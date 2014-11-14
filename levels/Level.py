"""Module that takes care of running the different levels"""

import pygame
import sprites.Enemy as Enemy
from states.Constants import Constants
import map.Map as Map
import states.GameEnded
import sprites.Fireball as Fireball
import sprites.Checkpoint as Checkpoint


# Must overwrite self.set_tiles()
# Must overwrite self.game_over()
class Level(object):

    def __init__(self, player):
        self.map = None
        self.enemies = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.player = player
        self.tiles = pygame.sprite.Group()

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
        self.enemy_collision(player_coordinates)
        #Update our stuff
        #for enemy in self.enemies:
        #wwwwww    enemy.update(interval, player_coordinates)

        return player_coordinates

    # draws the enemies and items
    # does not need a display update since Play calls that
    def draw(self, background):
        self.enemies.clear(Constants.SCREEN, background)
        self.items.clear(Constants.SCREEN, background)
        self.tiles.clear(Constants.SCREEN, background)

        self.tiles.draw(Constants.SCREEN)
        self.enemies.draw(Constants.SCREEN)
        self.items.draw(Constants.SCREEN)

    def set_tiles(self):
        self.tiles = self.map.render(self.player.x, self.player.y)
        self.player.rect.topleft = self.map.get_topleft(self.player.x,
                                                    self.player.y)
        for enemy in self.enemies.sprites():
            enemy.rect.topleft = self.map.get_topleft(enemy.x, enemy.y)
        for item in self.items.sprites():
            item.rect.topleft = self.map.get_topleft(item.x, item.y)

    def enemy_collision(self, player_coordinates):
        for enemy in self.enemies:
            enemy.update(Constants.INTERVAL, player_coordinates)
            all_tiles_in_enemy_range = self.map.get_tiles(enemy.x, enemy.y)
            if type(enemy) == Enemy.Racer and self.map != None:
                for checkpoint in self.enemies:
                    if type(checkpoint) == Checkpoint.Checkpoint:
                        if checkpoint.number == 4:
                            if checkpoint.rect.colliderect(enemy.rect):
                                if enemy.timer_on == False:
                                    print ("Enemy has beaten race!")
                                    enemy.start_timer()
            #Fireball collisions
            if type(enemy) == Fireball.Fireball and self.map != None:
                collidables_to_check = all_tiles_in_enemy_range
                for r in collidables_to_check:
                    if r.get_strength() >= 0:
                        if r.rect.collidepoint(enemy.rect.midbottom):
                            enemy.y -= .1
                            enemy.bounce(False)
                        elif r.rect.collidepoint(enemy.rect.midtop):
                            enemy.y += .1
                            enemy.bounce(False)
                        elif r.rect.collidepoint(enemy.rect.midleft):
                            enemy.x += .1
                            enemy.bounce(True)
                        elif r.rect.collidepoint(enemy.rect.midright):
                            enemy.x -= .1
                            enemy.bounce(True)
            #Boss 2 Collisions
            if type(enemy) == Enemy.Boss_1 and self.map != None:
                collidables_to_check = all_tiles_in_enemy_range
                collidables_to_check.append(self.player)
                #Here goes collision
                collision_fixed = False
                #Go through all of the collidable rects around the player
                for r in collidables_to_check:
                    #A strength >= 0 indicates a collidable object
                    #  -1 isnt collidable
                    if r.get_strength() >= 0:
                    #This same if statement is repeated for all midpoints
                    #Checking if the midpoint of the car is in the other rect
                    #This midpoint check tells us how to fix the car's position
                        if (r.rect.collidepoint(enemy.rect.midbottom)):
                            enemy.rect.bottom = r.rect.top
                            collision_fixed = True
                            enemy.speed = 0
                            enemy.y -= .01

                        if (r.rect.collidepoint(enemy.rect.midleft)):
                            enemy.rect.left = r.rect.right
                            collision_fixed = True
                            enemy.speed = 0
                            enemy.x += .01

                        if (r.rect.collidepoint(enemy.rect.midright)):
                            enemy.rect.right = r.rect.left
                            collision_fixed = True
                            enemy.speed = 0
                            enemy.x -= .01

                        if (r.rect.collidepoint(enemy.rect.midtop)):

                            enemy.rect.top = r.rect.bottom
                            collision_fixed = True
                            enemy.speed = 0
                            enemy.y += .01

                    #These collision if statements are to fix hitting corners
                    #Only happens if there wasnt a collision with a
                    #center of the car
                        if (not collision_fixed and r.rect.collidepoint(
                                enemy.rect.topright)):

                            collision_fixed = True
                            enemy.rect.right = r.rect.left
                            enemy.speed = 0
                            enemy.x -= .01

                        if (not collision_fixed and r.rect.collidepoint(
                                enemy.rect.bottomright)):

                            collision_fixed = True
                            enemy.rect.right = r.rect.left
                            enemy.speed = 0
                            enemy.x -= .01

                        if (not collision_fixed and r.rect.collidepoint(
                                enemy.rect.topleft)):

                            collision_fixed = True
                            enemy.rect.left = r.rect.right
                            enemy.speed = 0
                            enemy.x += .01
                        if (not collision_fixed and r.rect.collidepoint(
                                enemy.rect.bottomleft)):

                            collision_fixed = True
                            enemy.rect.left = r.rect.right
                            enemy.speed = 0
                            enemy.x += .01

    def player_collision(self):
        player_coordinates = self.player.get_coordinates()
        #Check if player has EZPass, if so, open the TollBooth
        if "ezpass" in self.player.inventory:
                #Very hackish way to do this; the score should be
                #  on the player, so when we collect collectables
                #  or collide, we can easily update the score.
                # But we have more pressing things to do now.
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
        #Go through all of the collidable rects around the playerssssss
        for r in collidables_on_screen:
            #A strength >= 0 indicates a collidable object
            #  -1 isnt collidable
            if type(r) == Checkpoint.Checkpoint:
                if r.rect.colliderect(self.player.rect):
                    self.enemy_collided(r, 0)
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
                self.enemy_collided(r, damage_to_do)
                break
        return player_coordinates

    def game_over(self, died):
        print "Super Level Game Over"

