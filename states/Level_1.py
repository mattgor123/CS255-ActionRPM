import pygame
import pygame.display as display
import random
import pickle
import states.State as State
import sprites.Label as Label
import sprites.Player as Player
import sprites.Enemy as Enemy
import sprites.HUD as HUD
import sprites.Speedometer as Speedometer
#import map.Map as Map
import Level_2
import NewHigh
import GameEnded
import Menu
import sprites.EZPass as EZPass
import sprites.TollBooth as TollBooth
from Constants import Constants
from map import Map


#This is the state for playing the game
class Level_1(State.State):
    health = Constants.PLAYER_STARTING_HEALTH
    time = 0
    tiles = None
    START_SCORE = None
    SCORE_TIME = 0
    END_SCORE = 0

    #Code to initialize a new game instance
    def __init__(self):
        super(Level_1, self).__init__()
        #making global sprite groups so we can call them from other methods
        global players, labels, background, map, key, score_label,\
            enemies, items, hud
        #Set score variables
        self.START_SCORE = 1000
        self.SCORE_TIME = 0
        #Flags whether or not we already have the ezpass
        self.is_beatable = False
        #Create global map for players to use
        global map
        map = Map.Map("map.txt", 3)
        #Create sprite groups to hold players and enemies
        players = pygame.sprite.Group()
        enemies = pygame.sprite.Group()
        #Holds current map tiles to be rendered
        Level_1.tiles = pygame.sprite.Group()

        #Sprite groups for miscellaneous
        key = pygame.sprite.Group()
        score_label = pygame.sprite.Group()
        items = pygame.sprite.Group()
        speedometer = pygame.sprite.Group()

        #Background surface
        background = pygame.Surface(Constants.SCREEN.get_size())

        #Fill screen with black
        Constants.SCREEN.fill((0, 0, 0))

        #Make labels
        labels = pygame.sprite.Group()
        labels.add(Label.Label("health", "Health: 100%", (10, 10)))
        labels.add(Label.Label("score", "Score: ", (10, 34)))

        #Create enemies and add them to our sprite group
        enemies.add(Enemy.Enemy([39, 3.1], [
            Constants.WIDTH, Constants.HEIGHT], 5, "down",
            ["d4", "r2.9", "u4", "l2.9"]))
        enemies.add(Enemy.Enemy([40.4, 17.5],
                                [Constants.WIDTH, Constants.HEIGHT],
            5, "down", ["d12.5", "l16", "u12.5", "r16"]))

        #Create miscellaneous shit
        items.add(EZPass.EZPass("ezpass", 38, 19))

        player1 = Player.Player([8, 6], [
            Constants.WIDTH, Constants.HEIGHT])
        players.add(player1)
        hud = HUD.HUD()

        self.time = 0.00

    #Function to draw the sprite groups
    def draw(self):
        #Clear the sprite groups from the screen
        players.clear(Constants.SCREEN, background)
        enemies.clear(Constants.SCREEN, background)
        Level_1.tiles.clear(Constants.SCREEN, background)
        # enemies.clear(Constants.SCREEN, background)
        labels.clear(Constants.SCREEN, background)
        score_label.clear(Constants.SCREEN, background)
        items.clear(Constants.SCREEN, background)
        hud.clear(Constants.SCREEN)
        # walls.clear(Constants.SCREEN, background)

        if self.health <= 0:
            #labels.clear(Constants.SCREEN,background)
            labels.draw(Constants.SCREEN)
            display.update()
            game_over(self, True)

        else:
            # enemies.draw(Constants.SCREEN)
            #self.set_tiles()
            Level_1.tiles.draw(Constants.SCREEN)
            labels.draw(Constants.SCREEN)
            score_label.draw(Constants.SCREEN)
            key.draw(Constants.SCREEN)
            players.draw(Constants.SCREEN)
            enemies.draw(Constants.SCREEN)
            items.draw(Constants.SCREEN)
            hud.draw(Constants.SCREEN)
            # walls.draw(Constants.SCREEN)
            display.update()

    def set_tiles(self):
        for player in players.sprites():
            Level_1.tiles = map.render(player.x, player.y)
            player.rect.topleft = map.get_topleft(player.x, player.y)
        for enemy in enemies.sprites():
            enemy.rect.topleft = map.get_topleft(enemy.x, enemy.y)
        for item in items.sprites():
            item.rect.topleft = map.get_topleft(item.x, item.y)

    def keyEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                game_over(self, False)
            elif event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                Constants.STATE = Menu.Menu()

    #Code to update all of the sprite groups and clear them from the screen
    def update(self, time):
        #1 point per 1/Constants.INTERVAL cycles
        self.time += time

        self.set_tiles()
        #Update the player
        #Initially we assume the player coordinates are 0,0
        #Until it is updated
        player_coordinates = [0,0]
        for player in players:
            player.update(Constants.INTERVAL)
            player_coordinates = player.get_coordinates()
            #Check if player has EZPass, if so, open the TollBooth
            if not self.is_beatable:
                if "ezpass" in player.inventory:
                    #Very hackish way to do this; the score should be
                    #  on the player, so when we collect collectables
                    #  or collide, we can easily update the score.
                    # But we have more pressing things to do now.
                    self.START_SCORE += 50
                    self.is_beatable = True
                    for openable in map.openables:
                        if openable.__str__() == "t":
                            openable.open()

            if player.has_beaten_level(0):
                    game_over(self, False)
            self.health = player.calculate_health()

            #Iterate through items and check if they are colliding
            #With the player
            for c in items.sprites():
                if c.rect.colliderect(player.rect):
                    player.add_to_inventory(c)
                    c.collect()

            collidables_on_screen = map.get_tiles(player.x, player.y)
            for enemy in enemies:
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
                    if (r.rect.collidepoint(player.rect.midbottom)):
                        damage_to_do = r.get_strength()
                        player.rect.bottom = r.rect.top
                        collision_fixed = True
                        player.speed = Constants.PLAYER_MIN_SPEED
                        player.y -= .01

                    if (r.rect.collidepoint(player.rect.midleft)):
                        damage_to_do = r.get_strength()
                        player.rect.left = r.rect.right
                        collision_fixed = True
                        player.speed = Constants.PLAYER_MIN_SPEED
                        player.x += .01

                    if (r.rect.collidepoint(player.rect.midright)):
                        damage_to_do = r.get_strength()
                        player.rect.right = r.rect.left
                        collision_fixed = True
                        player.speed = Constants.PLAYER_MIN_SPEED
                        player.x -= .01

                    if (r.rect.collidepoint(player.rect.midtop)):
                        damage_to_do = r.get_strength()
                        player.rect.top = r.rect.bottom
                        collision_fixed = True
                        player.speed = Constants.PLAYER_MIN_SPEED
                        player.y += .01

                    #These collision if statements are to fix hitting corners
                    #Only happens if there wasnt a collision with a
                    #center of the car
                    if (not collision_fixed and r.rect.collidepoint(
                            player.rect.topright)):
                        damage_to_do = r.get_strength()
                        collision_fixed = True
                        player.rect.right = r.rect.left
                        player.speed = Constants.PLAYER_MIN_SPEED
                        player.x -= .01

                    if (not collision_fixed and r.rect.collidepoint(
                            player.rect.bottomright)):
                        damage_to_do = r.get_strength()
                        collision_fixed = True
                        player.rect.right = r.rect.left
                        player.speed = Constants.PLAYER_MIN_SPEED
                        player.x -= .01

                    if (not collision_fixed and r.rect.collidepoint(
                            player.rect.topleft)):
                        damage_to_do = r.get_strength()
                        collision_fixed = True
                        player.rect.left = r.rect.right
                        player.speed = Constants.PLAYER_MIN_SPEED
                        player.x += .01
                    if (not collision_fixed and r.rect.collidepoint(
                            player.rect.bottomleft)):
                        damage_to_do = r.get_strength()
                        collision_fixed = True
                        player.rect.left = r.rect.right
                        player.speed = Constants.PLAYER_MIN_SPEED
                        player.x += .01

                if collision_fixed:
                    #This if statement tells us that the player hit the
                    #Boss and it should inflict damage on the boss
                    if(damage_to_do == 0 and type(r) is Enemy.Boss_1):
                        r.hurt(3)

                    #Do the damage as prescribed by the collided box
                    player.damage += damage_to_do
                    #Play that terrible crash sound
                    player.crash.play()
                    #If we hit an enemy, make the enemy stop
                    if type(r) is Enemy.Enemy:
                        r.stop()
                    #Only do one collision per cycle
                    break

        for label in labels.sprites():
            if label.name == "health":
                label.update(self.health)
            elif label.name == "score":
                self.END_SCORE = self.START_SCORE - (self.time * 10)
                if self.END_SCORE <= 0:
                    game_over(self, True)
                label.update(self.END_SCORE)
        for s in score_label.sprites():
            delta = self.time - self.SCORE_TIME
            if delta > 1.2:
                score_label.remove(s)
            else:
                s.set_score_pos((126, 38 - (delta * 4)))

        for enemy in enemies:
            enemy.update(Constants.INTERVAL, player_coordinates)

        hud.update(players.sprites()[0].speed)


# Function to determine if the current score was a high score
def is_new_high_score(self):
    is_high = False
    f = open(Constants.HIGH_SCORE_FILE, "rb")
    try:
        scores = pickle.load(f)
    except:
        scores = []
    f.close()
    if len(scores) < 10:
        return True
    else:
        min_high_score = min(b for (a, b) in scores)
        if self.time > min_high_score:
            return True
    return False


# Define function to allow a user to restart if their health reaches 0%
def game_over(self, died):
    if died:
        Constants.STATE = GameEnded.GameEnded("GAME OVER")
    else:
        #Constants.STATE = Level_2.Level_2()
        Constants.Levels[1] = Level_2.Level_2()
        Constants.STATE = Constants.Levels[1]
        Level_1.map = None

