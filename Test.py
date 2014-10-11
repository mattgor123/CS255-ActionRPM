from map import Map
import pygame.display as display
import pygame as PG
import pygame.event as PE

PG.init()
WIDTH = 800
HEIGHT = 600
SCREEN = display.set_mode((WIDTH, HEIGHT))
test = Map.Map()
SCREEN.fill((0, 0, 0))
x = 80
y = 60
background = PG.Surface(SCREEN.get_size())

while True:

    group = test.render(x, y)
    group.update()
    group.draw(SCREEN)
    display.update()
    group.clear(SCREEN,background)

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
