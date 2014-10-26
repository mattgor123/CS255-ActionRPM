import pygame.image as PI
import pygame as PG

# x,y is size of image
# dimension is [x,y] for layout of spritesheet


def loadSheet(path, x, y, dimensions):

    currentX = 0
    currentY = 0

    toReturn = []
    sheet = PI.load(path)

    for j in range(0, dimensions[1]):
        toReturn.append([])
        currentX = 0
        for i in range(0, dimensions[0]):
            surface = PG.Surface((x, y)).convert()
            surface.fill((158, 125, 186))
            surface.blit(sheet, (0, 0), (currentX, currentY, currentX + x,
                                         currentY + y))
            surface.set_colorkey((158, 125, 186), PG.RLEACCEL)
            #surface = PG.transform.scale(surface, (128,64))
            toReturn[j].append(surface)
            currentX += x

        currentY += y

    return toReturn


def rotateSprites(sprites, degrees):
    toReturn = []
    for image in sprites:
        toReturn.append(PG.transform.rotate(image, degrees))

    return toReturn

if __name__ == "__main__":
    PG.init()
    screen = PG.display.set_mode((800, 600))
    sprites = loadSheet("../images/sprites/enemyfullhealthlights.png", 52, 26,
                        [3, 1])
    sprites = sprites[0]
    sprites = rotateSprites(sprites, 180)
    i = 0
    count = 0
    while True:
        screen.fill((0, 0, 0))
        screen.blit(sprites[i], (400, 300))
        PG.display.flip()
        if count % 100 == 0:
            i += 1
        if i == 3:
            i = 0
        count += 1
        for event in PG.event.get():
            if event.type == PG.QUIT:
                exit()
