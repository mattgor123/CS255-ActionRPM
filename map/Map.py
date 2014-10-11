import pygame as PG
from sprites.Tile import Tile
import sprites.Wall as Wall
import sprites.Street as Street
import sprites
from states.Constants import Constants


class Map():

    LETTER_WIDTH = Constants.WIDTH / Tile.WIDTH    # 10
    LETTER_HEIGHT = Constants.HEIGHT / Tile.HEIGHT  # 10
    MAX_LETTERS = 2
    MAX_HEIGHT = MAX_LETTERS * LETTER_HEIGHT
    MAX_WIDTH = MAX_LETTERS * LETTER_WIDTH

    def __init__(self):
        self.map = []
        self.init_map()

    def init_map(self):
        map_file = open("map/map.txt", "r")
        for i in range(0, Map.MAX_LETTERS):
            line = map_file.readline()
            for j in range(0, Map.MAX_LETTERS):
                self.map_load(j, i, line[j])

    def map_load(self, x, y, char):
        filename = "map/" + char + ".txt"
        map_x = x * Map.LETTER_WIDTH
        map_y = y * Map.LETTER_HEIGHT
        self.add_chunk(map_x, map_y)
        file = open(filename, "r")
        for line in file:
            line = line.rstrip('\n')
            for char in line:
                self.map[map_x][map_y] = self.resolve(char)
                map_x += 1
            map_y += 1
            map_x = x * Map.LETTER_WIDTH

    def resolve(self, char):
        if char == 'w':
            return sprites.Wall.Wall()
        elif char == 's':
            return sprites.Street.Street()
        else:
            return None

    def add_chunk(self, x, y):
        while x > len(self.map):
            self.map.append([])
            print "Problem, Map add_chunk"
        for i in range(0, Map.LETTER_WIDTH):
            if x >= len(self.map):
                self.map.append([])
            for j in range(0, Map.LETTER_HEIGHT):
                self.map[x].append(None)
            x += 1

    def __str__(self):
        toReturn = ""
        for col in self.map:
            for item in col:
                toReturn += item.__str__()
            toReturn += '\n'
        return toReturn

if __name__ == "__main__":
    test = Map()
