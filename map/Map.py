import pygame as PG
import math

from sprites.Tile import Tile
import sprites.Wall as Wall
import sprites.Street as Street
import sprites.TollBooth as EZPass
import sprites
from states.Constants import Constants


class Map():
    # Width of map a single letter counts for
    LETTER_WIDTH = Constants.WIDTH / Tile.WIDTH  # 10
    # Height of map a single letter counts for
    LETTER_HEIGHT = Constants.HEIGHT / Tile.HEIGHT  # 10
    # Maximum number of letters to read
    MAX_LETTERS = 3
    # Maximum height of map
    MAX_HEIGHT = MAX_LETTERS * LETTER_HEIGHT
    # Maximum width of map
    MAX_WIDTH = MAX_LETTERS * LETTER_WIDTH
    # Range to give for checking collisions
    TILE_RANGE = 5

    # Initializes the map, reads level1.txt
    def __init__(self, filename, size):
        self.map = []
        self.openables = []
        Map.MAX_LETTERS = size
        Map.MAX_HEIGHT = Map.MAX_LETTERS * Map.LETTER_HEIGHT
        Map.MAX_WIDTH = Map.MAX_LETTERS * Map.LETTER_WIDTH
        self.init_map(filename)
        self.x_min = 0
        self.x_max = 0
        self.y_min = 0
        self.y_max = 0
        self.filename = filename
        self.size = size

    # Reads up to max letters from level1.txt and loads
    # them into RAM
    def init_map(self, filename):
        map_file = open("map/" + filename, "r")
        for i in range(0, Map.MAX_LETTERS):
            line = map_file.readline()
            for j in range(0, Map.MAX_LETTERS):
                self.map_load(j, i, line[j])

    # Loads the more zoomed in map file for the specific
    # character given
    def map_load(self, x, y, char):
        filename = "map/" + char + ".txt"
        map_x = x * Map.LETTER_WIDTH
        map_y = y * Map.LETTER_HEIGHT
        self.add_chunk(map_x, map_y)
        file = open(filename, "r")
        for line in file:
            line = line.rstrip('\n')
            for char in line:
                self.map[map_x][map_y] = self.resolve(char, x, y, map_x, map_y)
                map_x += 1
            map_y += 1
            map_x = x * Map.LETTER_WIDTH

    # Creates an object represented by the given char
    def resolve(self, char, x, y, map_x, map_y):
        to_return = None
        # Streets
        if char == 's':
            to_return = sprites.Street.Street(map_x, map_y, "empty")
        elif char == 'h':
            to_return = sprites.Street.Street(map_x, map_y, "horizontal")
        elif char == 'v':
            to_return = sprites.Street.Street(map_x, map_y, "vertical")
        elif char == 'o':
            to_return = sprites.Street.Street(map_x, map_y, "o")
        elif char == 'p':
            to_return = sprites.Street.Street(map_x, map_y, "p")
        elif char == 'l':
            to_return = sprites.Street.Street(map_x, map_y, "l")
        elif char == ';':
            to_return = sprites.Street.Street(map_x, map_y, ";")
        #Sidewalks
        elif char == 'a':
            to_return = sprites.Wall.Wall(map_x, map_y, "a")
        elif char == 'q':
            to_return = sprites.Wall.Wall(map_x, map_y, "q")
        elif char == 'z':
            to_return = sprites.Wall.Wall(map_x, map_y, "z")
        elif char == 'x':
            to_return = sprites.Wall.Wall(map_x, map_y, "x")
        elif char == 'd':
            to_return = sprites.Wall.Wall(map_x, map_y, "d")
        elif char == 'e':
            to_return = sprites.Wall.Wall(map_x, map_y, "e")
        elif char == 'r':
            to_return = sprites.Wall.Wall(map_x, map_y, "r")
        elif char == 'u':
            to_return = sprites.Wall.Wall(map_x, map_y, "u")
        elif char == 'i':
            to_return = sprites.Wall.Wall(map_x, map_y, "i")
        elif char == ':':
            to_return = sprites.Wall.Wall(map_x, map_y, ":")
        elif char == '"':
            to_return = sprites.Wall.Wall(map_x, map_y, "\"")
        elif char == '>':
            to_return = sprites.Wall.Wall(map_x, map_y, ">")
        elif char == '?':
            to_return = sprites.Wall.Wall(map_x, map_y, "?")
        #Tollbooth
        elif char == 't':
            to_return = sprites.TollBooth.TollBooth(map_x, map_y)
            self.openables.append(to_return)
        #Buildings
        elif char == '!':
            to_return = sprites.Wall.Wall(map_x, map_y, "!")
        elif char == '@':
            to_return = sprites.Wall.Wall(map_x, map_y, "@")
        elif char == '#':
            to_return = sprites.Wall.Wall(map_x, map_y, "#")
        elif char == '$':
            to_return = sprites.Wall.Wall(map_x, map_y, "$")
        elif char == '%':
            to_return = sprites.Wall.Wall(map_x, map_y, "%")
        elif char == '^':
            to_return = sprites.Wall.Wall(map_x, map_y, "^")
        elif char == 'b':
            to_return = sprites.Wall.Wall(map_x, map_y, "b")
        elif char == 'n':
            to_return = sprites.Wall.Wall(map_x, map_y, "n")
        elif char == '-':
            to_return = sprites.Wall.Wall(map_x, map_y, '-')
        elif char == '+':
            to_return = sprites.Wall.Wall(map_x, map_y, '+')
        elif char == 'Q':
            to_return = sprites.Wall.Wall(map_x, map_y, 'Q')
        elif char == 'W':
            to_return = sprites.Wall.Wall(map_x, map_y, 'W')
        elif char == 'A':
            to_return = sprites.Wall.Wall(map_x, map_y, 'A')
        elif char == 'S':
            to_return = sprites.Wall.Wall(map_x, map_y, 'S')
        elif char == 'E':
            to_return = sprites.Wall.Wall(map_x, map_y, 'E')
        elif char == 'R':
            to_return = sprites.Wall.Wall(map_x, map_y, 'R')
        elif char == 'D':
            to_return = sprites.Wall.Wall(map_x, map_y, 'D')
        elif char == 'F':
            to_return = sprites.Wall.Wall(map_x, map_y, 'F')
        elif char == 'T':
            to_return = sprites.Wall.Wall(map_x, map_y, 'T')
        elif char == 'Y':
            to_return = sprites.Wall.Wall(map_x, map_y, 'Y')
        elif char == 'G':
            to_return = sprites.Wall.Wall(map_x, map_y, 'G')
        elif char == 'H':
            to_return = sprites.Wall.Wall(map_x, map_y, 'H')
        elif char == 'U':
            to_return = sprites.Wall.Wall(map_x, map_y, 'U')
        elif char == 'I':
            to_return = sprites.Wall.Wall(map_x, map_y, 'I')
        elif char == 'J':
            to_return = sprites.Wall.Wall(map_x, map_y, 'J')
        elif char == 'K':
            to_return = sprites.Wall.Wall(map_x, map_y, 'K')
        elif char == '(':
            to_return = sprites.Wall.Wall(map_x, map_y, '(')
        elif char == ')':
            to_return = sprites.Wall.Wall(map_x, map_y, ')')
        elif char == 'O':
            to_return = sprites.Wall.Wall(map_x, map_y, 'O')
        elif char == 'P':
            to_return = sprites.Wall.Wall(map_x, map_y, 'P')
        #Default wall
        else:
            to_return = sprites.Wall.Wall(map_x, map_y, "w")
        return to_return

    # Appends a new chunk starting at x,y to the map.
    # Loads all Nones
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

    # Returns a string representation of the map
    def __str__(self):
        toReturn = ""
        for col in self.map:
            for item in col:
                toReturn += item.__str__()
            toReturn += '\n'
        return toReturn

    # Returns a sprite group of all the sprites that need
    # to be rendered around the player_x, player_y.
    # Adjusts the maps mins / maxes so that there is never
    # black space rendered
    def render(self, player_x, player_y):
        to_render = PG.sprite.Group()

        self.x_min = player_x - ((Map.LETTER_WIDTH / 2))
        self.x_max = player_x + ((Map.LETTER_WIDTH / 2))
        if self.x_min < 0:
            self.x_max += math.fabs(self.x_min) - 1
            self.x_min = 0
        if self.x_max >= len(self.map):
            self.x_min -= (self.x_max - len(self.map))
            self.x_max = len(self.map) - 1

        self.y_min = player_y - (Map.LETTER_HEIGHT / 2)
        self.y_max = player_y + (Map.LETTER_HEIGHT / 2) - 2
        if self.y_min < 0:
            self.y_max += math.fabs(self.y_min) - 1
            self.y_min = 0
        if self.y_max >= len(self.map[0]):
            self.y_min -= (self.y_max - len(self.map[0]))
            self.y_max = len(self.map[0]) - 1

        # self.x_min = int(self.x_min)
        # self.x_max = int(self.x_max)
        # self.y_min = int(self.y_min)
        # self.y_max = int(self.y_max)

        for x in range(int(self.x_min), int(self.x_max) + 1):
            for y in range(int(self.y_min), int(self.y_max) + 1):
                self.map[x][y].rect.topleft = ((x - self.x_min) * Tile.WIDTH,
                                               (y - self.y_min) * Tile.HEIGHT)
                to_render.add(self.map[x][y])
        return to_render

    # Gets the tuple for the top_left corner of a sprite
    # with map coordinates x,y
    def get_topleft(self, x, y):
        x_coor = (x - self.x_min) * Tile.WIDTH
        y_coor = (y - self.y_min) * Tile.HEIGHT
        return tuple((x_coor, y_coor))

    # Gets all the tiles within a radius of TILE_RANGE from
    # x,y
    def get_tiles(self, x, y):
        to_return = []
        x = int(x)
        y = int(y)
        for i in range(x - Map.TILE_RANGE - 1, x + Map.TILE_RANGE + 1):
            for j in range(y - Map.TILE_RANGE - 1, y + Map.TILE_RANGE + 1):
                if self.inbound(i, j):
                    to_return.append(self.map[i][j])
                    # print i, ",", j
        return to_return

    # Checks if the given coordinates x,y are in the bounds of the map
    def inbound(self, x, y):
        if x >= len(self.map) or x < 0:
            return False
        if y >= len(self.map[0]) or y < 0:
            return False
        return True
