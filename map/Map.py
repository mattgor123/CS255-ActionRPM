__author__ = 'tuvialerea'


import pygame as PG
import sprites as SP
import states.Constants as Constants


class Map():

    LETTER_WIDTH = Constants.WIDTH / SP.Tile.WIDTH   # 10
    LETTER_HEIGHT = Constants.WIDTH / SP.Tile.HEIGHT # 10
    MAX_LETTERS = 2
    MAX_HEIGHT = MAX_LETTERS * LETTER_HEIGHT
    MAX_WIDTH = MAX_LETTERS * LETTER_WIDTH

    def __init__(self):
        self.map = []
        self.current_x = 0
        self.current_y = 0
        self.init_map()

    def init_map(self):
        map_file = open("./map.txt", "r")
        for i in range(0, Map.MAX_LETTERS):
            line = map_file.readline()
            for j in range(0, Map.MAX_LETTERS):
                self.map_load(j, i, line[j])

    def map_load(self, x, y, char):
        filename = char + ".txt"
        map_x = x * Map.LETTER_WIDTH
        map_y = y * Map.LETTER_HEIGHT
        file = open(filename, "r")
        for line in file:
            for char in line:
                self.map[map_x][map_y] = self.resolve(char)
                map_x += 1
                map_y += 1

    def resolve(self, char):
        if char == 'w':
            return SP.Wall()
        elif char == 's':
            return SP.Street()
        else:
            return None