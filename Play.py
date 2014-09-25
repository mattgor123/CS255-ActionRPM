import pygame
import pygame.display as display
import random
import State
import Label
import Player
import Enemy
from Constants import Constants


#This is the state for playing the game
class Play(State.State):
    health = Constants.PLAYER_STARTING_HEALTH

    #Code to initialize a new game instance
    def __init__(self):
        super(Play, self).__init__()
        global players, enemies, labels, background
        background = pygame.Surface(Constants.SCREEN.get_size())
        Constants.SCREEN.fill((0, 0, 0))
        labels = pygame.sprite.Group()
        h_label = Label.Label("health", "Health: 100%", (0, 0))
        labels.add(h_label)
        players = pygame.sprite.Group()
        player1 = Player.Player([Constants.WIDTH / 2, Constants.HEIGHT / 2],
                                [Constants.WIDTH, Constants.HEIGHT],
                                Constants.PLAYER_SPEED, Constants.DIFFICULTY)
        players.add(player1)
        enemies = pygame.sprite.Group()
        for i in range(Constants.ENEMY_COUNT):
            enemy_speed = random.randint(1, Constants.ENEMY_SPEEDS) * \
                          Constants.PLAYER_SPEED * 2 / Constants.ENEMY_SPEEDS
            new_enemy = Enemy.Enemy(
                [random.randint(0, Constants.WIDTH - player1.rect.width),
                 random.randint(0, Constants.HEIGHT - player1.rect.height)],
                [Constants.WIDTH, Constants.HEIGHT], enemy_speed,
                direction=random.randint(1, 8))
            enemies.add(new_enemy)

    #Function to draw the sprite groups
    def draw(self):

        #Clear the sprite groups from the screen
        players.clear(Constants.SCREEN, background)
        enemies.clear(Constants.SCREEN, background)
        labels.clear(Constants.SCREEN, background)

        if self.health <= 0:
            #labels.clear(Constants.SCREEN,background)
            labels.draw(Constants.SCREEN)
            display.update()
            game_over()

        else:
            labels.clear(Constants.SCREEN, background)
            enemies.draw(Constants.SCREEN)
            labels.draw(Constants.SCREEN)
            players.draw(Constants.SCREEN)
            display.update()

    #Only specific key event we will handle for now is 'q' or 'r' to restart
    def keyEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                game_over()
            elif event.key == pygame.K_r:
                game_over()

    ''' Was code to update all the labels, but we only need to update the
    health label now
    def update_labels(self, params):
        for label in labels.sprites():
            if label.name == "health":
                label.update(self.health)
            elif label.name == "fps":
                label.update(params[0])
            elif label.name == "spf":
                label.update(params[1])
            elif label.name == "upf":
                label.update(params[2])
                '''

    #Code to update all of the sprite groups and clear them from the screen
    def update(self, time):
        #Update the player
        players.update(Constants.INTERVAL)
        for player in players.sprites():
                dir_changed = player.dir_changed
                direction = player.direction
        enemies.update(dir_changed, direction, Constants.INTERVAL)

        #Determine current health status & update Label
        for player in players.sprites():
            self.health = player.calculate_health()
        for label in labels.sprites():
            if label.name == "health":
                label.update(self.health)


# Define function to allow a user to restart if their health reaches 0%
def game_over():
    global myFont
    for label1 in labels:
        myFont = label1.font
    game_over_surface = myFont.render(
        'Game Over - Would you like to restart? (Y/N)', 1, (255, 255, 255))
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.center = Constants.SCREEN.get_rect().center
    Constants.SCREEN.blit(game_over_surface, game_over_rect)
    display.update()
    while True:
        for eve in pygame.event.get():
            if eve.type == pygame.QUIT:
                exit()
            elif eve.type == pygame.KEYDOWN:
                if eve.key == pygame.K_y:
                    Constants.SCREEN.fill((0, 0, 0))
                    Play.__init__(Play())
                    return
                if eve.key == pygame.K_n or eve.key == pygame.K_ESCAPE:
                    exit()
