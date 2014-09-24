import pygame.image as PI
import pygame as PG


def loadSheet(path, x, y, dimensions):
    currentX = 0
    currentY = 0

    toReturn = []
    sheet = PI.load(path).convert()
    for j in range(0,dimensions[1]):
        toReturn[j] = []
        for i in range(0, dimensions[0]):
            surface = PG.Surface((x, y)).convert()
            surface.blit(sheet, (0,0),(currentX, currentY, currentX + x,
                                       currentY + y) )
            toReturn[j][i] = surface
            currentX += x

        currentY += y

    return toReturn


if __name__ == "__main__":
    print "Test"
