from map import Map
import pygame.display as display
import pygame as PG
import pygame.event as PE
import sprites.Player as Player
from states.Constants import Constants

PG.init()
WIDTH = 800
HEIGHT = 600
SCREEN = display.set_mode((WIDTH, HEIGHT))
test = Map.Map()
SCREEN.fill((0, 0, 0))
x = 40
y = 150
player = Player.Player(test.get_top_left(40, 30), [
    Constants.WIDTH, Constants.HEIGHT], Constants.DIFFICULTY)
players = PG.sprite.Group()
players.add(player)
background = PG.Surface(SCREEN.get_size())

while True:

    group = test.render(x, y)
    group.update()
    group.draw(SCREEN)
    players.draw(SCREEN)
    display.update()
    group.clear(SCREEN, background)
    players.clear(SCREEN, background)

    for event in PE.get():
        if event.type == PG.QUIT:
            exit()

    keys_pressed = PG.key.get_pressed()
    if keys_pressed[PG.K_RIGHT]:
        x += 1
    if keys_pressed[PG.K_LEFT]:
        x -= 1
    if keys_pressed[PG.K_DOWN]:
        y += 1
    if keys_pressed[PG.K_UP]:
        y -= 1
