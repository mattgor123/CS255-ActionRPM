import pygame
import pygame.display as display
import pickle
import states.State as State
import sprites.Label as Label
import sprites.Player as Player
import sprites.Enemy as Enemy
import sprites.HUD as HUD
import GameEnded
import Menu
import sprites.EZPass as EZPass
from Constants import Constants
from map import Map

#This shouldnt have to be imported once we
#get the level changer
import Level_2


#This is the state for playing the game
class Level_1(State.State):
    #This needs to be moved into the player
    health = Constants.PLAYER_STARTING_HEALTH

    #Code to initialize a new game instance
    def __init__(self):
        super(Level_1, self).__init__()
        #making global sprite groups so we can call them from other methods
        #Set score variables
        self.START_SCORE = 1000
        self.SCORE_TIME = 0

        #Flags whether or not we already have the ezpass
        self.is_beatable = False

        #Create global map for players to use
        self.map = Map.Map("level1.txt", 3)

        #Holds current map tiles to be rendered
        Level_1.tiles = pygame.sprite.Group()

        #Sprite groups for miscellaneous
        self.score_label = pygame.sprite.Group()

        #Background surface
        self.background = pygame.Surface(Constants.SCREEN.get_size())

        #Fill screen with black
        Constants.SCREEN.fill((0, 0, 0))

        #Initialize our sprite groups
        self.init_player()
        self.init_labels()
        self.init_enemies()
        self.init_items()

        #Initialize our HUD
        #TODO : Move this to the player; should not be on the level
        self.hud = HUD.HUD()

        self.time = 0.00

    def init_player(self):
        #Create sprite groups to hold players and enemies
        self.players = pygame.sprite.Group()
        player1 = Player.Player([8, 6], [
            Constants.WIDTH, Constants.HEIGHT])
        self.players.add(player1)

    def init_items(self):
        self.items = pygame.sprite.Group()
        #Create miscellaneous shit
        self.items.add(EZPass.EZPass("ezpass", 40, 19))

    def init_labels(self):
        #Make labels
        self.labels = pygame.sprite.Group()
        self.labels.add(Label.Label("health", "Health: 100%", (10, 10)))
        self.labels.add(Label.Label("score", "Score: ", (10, 34)))

    def init_enemies(self):
        #Create enemy sprite group
        self.enemies = pygame.sprite.Group()
        #Put in enemies
        #This enemy is by the EZpass exit
        self.enemies.add(Enemy.Enemy([39.2, 3.4], [
            Constants.WIDTH, Constants.HEIGHT], 5, "down",
            ["d3", "r1.8", "u3", "l1.8"]))
        #This enemy is driving around the bottom of the screen
        self.enemies.add(Enemy.Enemy([40.4, 17.5],
                                [Constants.WIDTH, Constants.HEIGHT],
                                5, "down", ["d12.5", "l16", "u12.5", "r16"]))
    #Function to draw the sprite groups
    def draw(self):
        #Clear the sprite groups from the screen
        self.players.clear(Constants.SCREEN, self.background)
        self.enemies.clear(Constants.SCREEN, self.background)
        Level_1.tiles.clear(Constants.SCREEN, self.background)
        self.labels.clear(Constants.SCREEN, self.background)
        self.score_label.clear(Constants.SCREEN, self.background)
        self.items.clear(Constants.SCREEN, self.background)
        self.hud.clear(Constants.SCREEN)

        Level_1.tiles.draw(Constants.SCREEN)
        self.labels.draw(Constants.SCREEN)
        self.score_label.draw(Constants.SCREEN)
        self.players.draw(Constants.SCREEN)
        self.enemies.draw(Constants.SCREEN)
        self.items.draw(Constants.SCREEN)
        self.hud.draw(Constants.SCREEN)
        # walls.draw(Constants.SCREEN)
        display.update()

    def set_tiles(self):
        for player in self.players.sprites():
            Level_1.tiles = self.map.render(player.x, player.y)
            player.rect.topleft = self.map.get_topleft(player.x, player.y)
        for enemy in self.enemies.sprites():
            enemy.rect.topleft = self.map.get_topleft(enemy.x, enemy.y)
        for item in self.items.sprites():
            item.rect.topleft = self.map.get_topleft(item.x, item.y)

    def keyEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                game_over(self, False)
            elif event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                Constants.STATE = Menu.Menu()
            #TODO : Move radio logic out of Levels
            elif event.key == pygame.K_LEFT:
                self.hud.radio.decrement_current_index_and_play()
            elif event.key == pygame.K_RIGHT:
                self.hud.radio.increment_current_index_and_play()
            elif event.key == pygame.K_KP0:
                self.hud.radio.play_random_song()
            elif event.key == pygame.K_o:
                self.hud.radio.toggle_radio()


    def player_collision(self):
        for player in self.players:
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
                    for openable in self.map.openables:
                        if openable.__str__() == "t":
                            openable.open()

            if player.has_beaten_level(0):
                    game_over(self, False)
            self.health = player.calculate_health()

            #Iterate through items and check if they are colliding
            #With the player
            for c in self.items.sprites():
                if c.rect.colliderect(player.rect):
                    player.add_to_inventory(c)
                    c.collect()

            collidables_on_screen = self.map.get_tiles(player.x, player.y)
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
                    #player.crash.play()
                    #If we hit an enemy, make the enemy stop
                    if type(r) is Enemy.Enemy:
                        r.stop()
                    #Only do one collision per cycle
                    return player_coordinates

    #Code to update all of the sprite groups and clear them from the screen
    def update(self, time):
        #Check the health to see if we are done
        if self.health <= 0:
            #labels.clear(Constants.SCREEN,background)
            self.labels.draw(Constants.SCREEN)
            display.update()
            game_over(self, True)

        #1 point per 1/Constants.INTERVAL cycles
        self.time += time

        #Set the tiles for what we need right now
        self.set_tiles()

        #This code does the player collision and returns the player coordinates
        player_coordinates = self.player_collision()

        #Update our stuff
        self.update_labels()
        self.update_enemies(player_coordinates)
        self.hud.update(self.players.sprites()[0].speed)

    def update_enemies(self, player_coordinates):
        for enemy in self.enemies:
            enemy.update(Constants.INTERVAL, player_coordinates)

    def update_labels(self):
        #TODO : Move Health Label to the HUD (or make it a bar, either way)
        for label in self.labels.sprites():
            if label.name == "health":
                label.update(self.health)
            elif label.name == "score":
                self.END_SCORE = self.START_SCORE - (self.time * 10)
                if self.END_SCORE <= 0:
                    game_over(self, True)
                label.update(self.END_SCORE)

        for s in self.score_label.sprites():
            delta = self.time - self.SCORE_TIME
            if delta > 1.2:
                self.score_label.remove(s)
            else:
                s.set_score_pos((126, 38 - (delta * 4)))

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
