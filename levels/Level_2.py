from Level import Level
import sprites.Enemy as Enemy
from states.Constants import Constants
from states.GameEnded import GameEnded
import map.Map as Map


class Level_2(Level):

    def __init__(self, player):
        Level.__init__(self, player)
        self.init_enemies()
        self.init_items()
        self.tiles = None
        self.PLAYER_START = [72, 56]
        self.is_beatable = False

    def init_items(self):
        #Create miscellaneous shit
        pass

    def init_enemies(self):
        #Put in enemies
        #This enemy is by the EZpass exit
        self.enemies.add(Enemy.Enemy([39.2, 4.4], [
            Constants.WIDTH, Constants.HEIGHT], 5, "down",
            ["d3", "r1.8", "u3", "l1.8"]))
        self.enemies.add(Enemy.Enemy([40.4, 17.5],
                                [Constants.WIDTH, Constants.HEIGHT],
                                5, "down", ["d12.5", "l16", "u12.5", "r16"]))
        self.enemies.add(Enemy.Boss_1([70, 40],
                                 [Constants.WIDTH,
                                  Constants.HEIGHT]))

    def update(self, interval):
        super(Level_2, self).update(interval)

    def draw(self, background):
        self.tiles.clear(Constants.SCREEN, background)
        self.tiles.draw(Constants.SCREEN)
        super(Level_2, self).draw(background)

    def set_tiles(self):
        self.tiles = self.map.render(self.player.x, self.player.y)
        self.player.rect.topleft = self.map.get_topleft(self.player.x,
                                                    self.player.y)
        for enemy in self.enemies.sprites():
            enemy.rect.topleft = self.map.get_topleft(enemy.x, enemy.y)
        for item in self.items.sprites():
            item.rect.topleft = self.map.get_topleft(item.x, item.y)

    def init_map(self):
        self.map = Map.Map("level2.txt", 5)
        self.set_tiles()

    def game_over(self, died):
        if died:
            Constants.STATE = GameEnded("GAME OVER")
        else:
            Constants.STATE.set_level(1)
