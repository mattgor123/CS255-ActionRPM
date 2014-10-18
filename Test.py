from map import Map
import pygame.display as display
import pygame as PG
import pygame.event as PE

PG.init()
WIDTH = 800
HEIGHT = 600
SCREEN = display.set_mode((WIDTH, HEIGHT))
test = Map.Map()

x = 0
y = 0
while True:
    SCREEN.fill((0, 0, 0))

    group = test.render(x, y)
    group.update()
    group.draw(SCREEN)
    display.flip()

    for event in PE.get():
        if event.type == PG.QUIT:
            exit()
        if event.type == PG.KEYDOWN and event.key == PG.K_RIGHT:
            x += 5
        if event.type == PG.KEYDOWN and event.key == PG.K_LEFT:
            x -= 5
        if event.type == PG.KEYDOWN and event.key == PG.K_DOWN:
            y += 5
        if event.type == PG.KEYDOWN and event.key == PG.K_UP:
            y -= 5