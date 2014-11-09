import pygame
import Tile


class Wall(Tile.Tile):
    building_0_00_img = None
    building_0_01_img = None
    building_0_10_img = None
    building_0_11_img = None
    building_0_20_img = None
    building_0_21_img = None
    building_0_c0_img = None
    building_0_c1_img = None

    building_1_00_img = None
    building_1_01_img = None
    building_1_02_img = None
    building_1_03_img = None
    building_1_10_img = None
    building_1_11_img = None
    building_1_12_img = None
    building_1_13_img = None
    building_1_c0_img = None
    building_1_c1_img = None
    building_1_c2_img = None
    building_1_c3_img = None

    building_2_00_img = None
    building_2_01_img = None
    building_2_10_img = None
    building_2_11_img = None
    building_2_c0_img = None
    building_2_c1_img = None

    building_3_00_img = None
    building_3_01_img = None
    building_3_02_img = None
    building_3_10_img = None
    building_3_11_img = None
    building_3_12_img = None
    building_3_20_img = None
    building_3_21_img = None
    building_3_22_img = None
    building_3_30_img = None
    building_3_31_img = None
    building_3_32_img = None
    building_3_c0_img = None
    building_3_c1_img = None
    building_3_c2_img = None

    sidewalk_0_img = None
    sidewalk_1_img = None
    sidewalk_2_img = None
    sidewalk_3_img = None
    sidewalk_4_img = None
    sidewalk_5_img = None
    sidewalk_6_img = None
    sidewalk_7_img = None
    sidewalk_8_img = None

    has_images = False

    def __init__(self, x, y, char):
        Tile.Tile.__init__(self, 3)

        # initialize wall image
        if not Wall.has_images:
            Wall.set_images()

        # building 0
        if char == 'a':
            self.image = Wall.building_0_00_img
        elif char == 'b':
            self.image = Wall.building_0_01_img
        elif char == 'c':
            self.image = Wall.building_0_10_img
        elif char == 'd':
            self.image = Wall.building_0_11_img
        elif char == 'e':
            self.image = Wall.building_0_20_img
        elif char == 'f':
            self.image = Wall.building_0_21_img
        elif char == 'g':
            self.image = Wall.building_0_c0_img
        elif char == 'i':
            self.image = Wall.building_0_c1_img

        # building 1
        elif char == 'j':
            self.image = Wall.building_1_00_img
        elif char == 'k':
            self.image = Wall.building_1_01_img
        elif char == 'm':
            self.image = Wall.building_1_02_img
        elif char == 'n':
            self.image = Wall.building_1_03_img
        elif char == 'q':
            self.image = Wall.building_1_10_img
        elif char == 'r':
            self.image = Wall.building_1_11_img
        elif char == 'u':
            self.image = Wall.building_1_12_img
        elif char == 'w':
            self.image = Wall.building_1_13_img
        elif char == 'x':
            self.image = Wall.building_1_c0_img
        elif char == 'y':
            self.image = Wall.building_1_c1_img
        elif char == 'z':
            self.image = Wall.building_1_c2_img
        elif char == '1':
            self.image = Wall.building_1_c3_img

        # building 2
        elif char == '2':
            self.image = Wall.building_2_00_img
        elif char == '3':
            self.image = Wall.building_2_01_img
        elif char == '4':
            self.image = Wall.building_2_10_img
        elif char == '5':
            self.image = Wall.building_2_11_img
        elif char == '6':
            self.image = Wall.building_2_c0_img
        elif char == '7':
            self.image = Wall.building_2_c1_img

        # sidewalk
        elif char == '8':
            self.image = Wall.sidewalk_0_img
        elif char == '9':
            self.image = Wall.sidewalk_1_img
        elif char == '0':
            self.image = Wall.sidewalk_2_img
        elif char == '!':
            self.image = Wall.sidewalk_3_img
        elif char == '@':
            self.image = Wall.sidewalk_4_img
        elif char == '#':
            self.image = Wall.sidewalk_5_img
        elif char == '$':
            self.image = Wall.sidewalk_6_img
        elif char == '%':
            self.image = Wall.sidewalk_7_img
        elif char == '^':
            self.image = Wall.sidewalk_8_img

        # building
        elif char == '&':
            self.image = Wall.building_3_00_img
        elif char == '*':
            self.image = Wall.building_3_01_img
        elif char == '(':
            self.image = Wall.building_3_02_img
        elif char == ')':
            self.image = Wall.building_3_10_img
        elif char == '_':
            self.image = Wall.building_3_11_img
        elif char == '+':
            self.image = Wall.building_3_12_img
        elif char == '{':
            self.image = Wall.building_3_20_img
        elif char == '}':
            self.image = Wall.building_3_21_img
        elif char == ':':
            self.image = Wall.building_3_22_img
        elif char == '<':
            self.image = Wall.building_3_30_img
        elif char == '>':
            self.image = Wall.building_3_31_img
        elif char == '?':
            self.image = Wall.building_3_32_img
        elif char == ',':
            self.image = Wall.building_3_c0_img
        elif char == '.':
            self.image = Wall.building_3_c1_img
        elif char == '`':
            self.image = Wall.building_3_c2_img

        self.rect = self.image.get_rect()
        # self.rect.center = location
        self.x = x
        self.y = y

    def __str__(self):
        return 'w'

    @staticmethod
    def set_images():
        image = pygame.image.load(
            "images/sprites/buildings/tileset.png").convert_alpha()
        tile_table = []
        for t_y in range(0, 600/50):
            line = []
            tile_table.append(line)
            for t_x in range(0, 550/50):
                rect = (t_x * 50, t_y * 50, 50, 50)
                line.append(image.subsurface(rect))

        Wall.building_0_00_img = tile_table[0][0]
        Wall.building_0_01_img = tile_table[0][1]
        Wall.building_0_10_img = tile_table[1][0]
        Wall.building_0_11_img = tile_table[1][1]
        Wall.building_0_20_img = tile_table[2][2]
        Wall.building_0_21_img = tile_table[2][3]
        Wall.building_0_c0_img = tile_table[2][0]
        Wall.building_0_c1_img = tile_table[2][1]

        Wall.building_1_00_img = tile_table[3][0]
        Wall.building_1_01_img = tile_table[3][1]
        Wall.building_1_02_img = tile_table[3][2]
        Wall.building_1_03_img = tile_table[3][3]
        Wall.building_1_10_img = tile_table[6][0]
        Wall.building_1_11_img = tile_table[6][1]
        Wall.building_1_12_img = tile_table[6][2]
        Wall.building_1_13_img = pygame.image.load("images/sprites/buildings/building_1.png").convert_alpha()
        Wall.building_1_c0_img = tile_table[4][0]
        Wall.building_1_c1_img = tile_table[4][1]
        Wall.building_1_c2_img = tile_table[4][2]
        Wall.building_1_c3_img = tile_table[4][3]

        Wall.building_2_00_img = tile_table[7][0]
        Wall.building_2_01_img = tile_table[7][1]
        Wall.building_2_10_img = tile_table[8][2]
        Wall.building_2_11_img = tile_table[8][3]
        Wall.building_2_c0_img = tile_table[8][0]
        Wall.building_2_c1_img = tile_table[8][1]

        Wall.building_3_00_img = tile_table[0][4]
        Wall.building_3_01_img = tile_table[0][5]
        Wall.building_3_02_img = tile_table[0][6]
        Wall.building_3_10_img = tile_table[1][4]
        Wall.building_3_11_img = tile_table[1][5]
        Wall.building_3_12_img = tile_table[1][6]
        Wall.building_3_20_img = tile_table[2][4]
        Wall.building_3_21_img = tile_table[2][5]
        Wall.building_3_22_img = tile_table[2][6]
        Wall.building_3_30_img = tile_table[3][7]
        Wall.building_3_31_img = tile_table[3][8]
        Wall.building_3_32_img = tile_table[3][9]
        Wall.building_3_c0_img = tile_table[3][4]
        Wall.building_3_c1_img = tile_table[3][5]
        Wall.building_3_c2_img = tile_table[3][6]

        Wall.sidewalk_0_img = tile_table[9][3]
        Wall.sidewalk_1_img = tile_table[9][4]
        Wall.sidewalk_2_img = tile_table[9][5]
        Wall.sidewalk_3_img = tile_table[10][3]
        Wall.sidewalk_4_img = tile_table[10][4]
        Wall.sidewalk_5_img = tile_table[10][5]
        Wall.sidewalk_6_img = tile_table[11][3]
        Wall.sidewalk_7_img = tile_table[11][4]
        Wall.sidewalk_8_img = tile_table[11][5]

        Wall.has_images = True
