import pygame
import Tile


class Wall(Tile.Tile):
    #Sidewalks
    a_wall = None
    q_wall = None
    z_wall = None
    x_wall = None
    d_wall = None
    e_wall = None
    r_wall = None
    u_wall = None
    i_wall = None
    tl_connector = None
    tr_connector = None
    bl_connector = None
    br_connector = None
    #Buildings
    sm_building_1 = None
    sm_building_2 = None
    sm_building_3 = None
    horiz_building_1l = None
    horiz_building_1r = None
    vert_building_1t = None
    vert_building_1b = None
    lrg_1_tl = None
    lrg_1_tr = None
    lrg_1_bl = None
    lrg_1_br = None
    lrg_2_tl = None
    lrg_2_tr = None
    lrg_2_bl = None
    lrg_2_br = None
    lrg_3_tl = None
    lrg_3_tr = None
    lrg_3_bl = None
    lrg_3_br = None
    lrg_4_tl = None
    lrg_4_tr = None
    lrg_4_bl = None
    lrg_4_br = None
    lrg_5_tl = None
    lrg_5_tr = None
    lrg_5_bl = None
    lrg_5_br = None
    #Default wall
    default_wall = None

    has_images = False

    def __init__(self, x, y, type):
        Tile.Tile.__init__(self, 3)

        # initialize wall image
        if not Wall.has_images:
            Wall.set_images()

        if type == "a":
            self.image = Wall.a_wall
        elif type == "q":
            self.image = Wall.q_wall
        elif type == "z":
            self.image = Wall.z_wall
        elif type == "x":
            self.image = Wall.x_wall
        elif type == "d":
            self.image = Wall.d_wall
        elif type == "e":
            self.image = Wall.e_wall
        elif type == "r":
            self.image = Wall.r_wall
        elif type == "u":
            self.image = Wall.u_wall
        elif type == "i":
            self.image = Wall.i_wall
        elif type == ":":
            self.image = Wall.tl_connector
        elif type == "\"":
            self.image = Wall.tr_connector
        elif type == ">":
            self.image = Wall.bl_connector
        elif type == "?":
            self.image = Wall.br_connector
        elif type == "!":
            self.image = Wall.sm_building_1
        elif type == "@":
            self.image = Wall.sm_building_2
        elif type == "#":
            self.image = Wall.sm_building_3
        elif type == "b":
            self.image = Wall.horiz_building_1l
        elif type == "n":
            self.image = Wall.horiz_building_1r
        elif type == "-":
            self.image = Wall.vert_building_1t
        elif type == "+":
            self.image = Wall.vert_building_1b
        elif type == "Q":
            self.image = Wall.lrg_1_tl
        elif type == "W":
            self.image = Wall.lrg_1_tr
        elif type == "A":
            self.image = Wall.lrg_1_bl
        elif type == "S":
            self.image = Wall.lrg_1_br
        elif type == "E":
            self.image = Wall.lrg_2_tl
        elif type == "R":
            self.image = Wall.lrg_2_tr
        elif type == "D":
            self.image = Wall.lrg_2_bl
        elif type == "F":
            self.image = Wall.lrg_2_br
        elif type == "T":
            self.image = Wall.lrg_3_tl
        elif type == "Y":
            self.image = Wall.lrg_3_tr
        elif type == "G":
            self.image = Wall.lrg_3_bl
        elif type == "H":
            self.image = Wall.lrg_3_br
        elif type == "U":
            self.image = Wall.lrg_4_tl
        elif type == "I":
            self.image = Wall.lrg_4_tr
        elif type == "J":
            self.image = Wall.lrg_4_bl
        elif type == "K":
            self.image = Wall.lrg_4_br
        elif type == "(":
            self.image = Wall.lrg_5_tl
        elif type == ")":
            self.image = Wall.lrg_5_tr
        elif type == "O":
            self.image = Wall.lrg_5_bl
        elif type == "P":
            self.image = Wall.lrg_5_br

        else:
            self.image = Wall.sm_building_1


        self.rect = self.image.get_rect()
        # self.rect.center = location
        self.x = x
        self.y = y

    def __str__(self):
        return 'w'

    @staticmethod
    def set_images():
        Wall.a_wall = pygame.image.load(
            "images/sprites/wall/horizontal_bot_sidewalk.png")
        Wall.q_wall = pygame.image.load(
            "images/sprites/wall/horizontal_top_sidewalk.png")
        Wall.z_wall = pygame.image.load(
            "images/sprites/wall/vertical_left_sidewalk.png")
        Wall.x_wall = pygame.image.load(
            "images/sprites/wall/vertical_right_sidewalk.png")
        Wall.d_wall = pygame.image.load(
            "images/sprites/wall/empty_sidewalk.png")
        Wall.e_wall  = pygame.image.load(
            "images/sprites/wall/tl_sidewalk.png")
        Wall.r_wall = pygame.image.load(
            "images/sprites/wall/tr_sidewalk.png")
        Wall.u_wall = pygame.image.load("images/sprites/wall/bl_sidewalk.png")
        Wall.i_wall = pygame.image.load("images/sprites/wall/br_sidewalk.png")
        Wall.tl_connector = pygame.image.load(
            "images/sprites/wall/tl_connector.png")
        Wall.tr_connector = pygame.image.load(
            "images/sprites/wall/tr_connector.png")
        Wall.bl_connector = pygame.image.load(
            "images/sprites/wall/bl_connector.png")
        Wall.br_connector = pygame.image.load(
            "images/sprites/wall/br_connector.png")
        #Buildings
        Wall.sm_building_1 = pygame.image.load(
            "images/sprites/buildings/sm_building_1.png")
        Wall.sm_building_2 = pygame.image.load(
            "images/sprites/buildings/sm_building_2.png")
        Wall.sm_building_3 = pygame.image.load(
            "images/sprites/buildings/sm_building_3.png")
        Wall.horiz_building_1l = pygame.image.load(
            "images/sprites/buildings/horiz_building_1l.png")
        Wall.horiz_building_1r = pygame.image.load(
            "images/sprites/buildings/horiz_building_1r.png")
        Wall.vert_building_1t = pygame.image.load(
            "images/sprites/buildings/vert_building_1t.png")
        Wall.vert_building_1b = pygame.image.load(
            "images/sprites/buildings/vert_building_1b.png")
        Wall.lrg_1_tl = pygame.image.load(
            "images/sprites/buildings/lrg_building_1_tl.png")
        Wall.lrg_1_tr = pygame.image.load(
            "images/sprites/buildings/lrg_building_1_tr.png")
        Wall.lrg_1_bl = pygame.image.load(
            "images/sprites/buildings/lrg_building_1_bl.png")
        Wall.lrg_1_br = pygame.image.load(
            "images/sprites/buildings/lrg_building_1_br.png")
        Wall.lrg_2_tl = pygame.image.load(
            "images/sprites/buildings/lrg_building_2_tl.png")
        Wall.lrg_2_tr = pygame.image.load(
            "images/sprites/buildings/lrg_building_2_tr.png")
        Wall.lrg_2_bl = pygame.image.load(
            "images/sprites/buildings/lrg_building_2_bl.png")
        Wall.lrg_2_br = pygame.image.load(
            "images/sprites/buildings/lrg_building_2_br.png")
        Wall.lrg_3_tl = pygame.image.load(
            "images/sprites/buildings/lrg_building_3_tl.png")
        Wall.lrg_3_tr = pygame.image.load(
            "images/sprites/buildings/lrg_building_3_tr.png")
        Wall.lrg_3_bl = pygame.image.load(
            "images/sprites/buildings/lrg_building_3_bl.png")
        Wall.lrg_3_br = pygame.image.load(
            "images/sprites/buildings/lrg_building_3_br.png")
        Wall.lrg_4_tl = pygame.image.load(
            "images/sprites/buildings/lrg_building_4_tl.png")
        Wall.lrg_4_tr = pygame.image.load(
            "images/sprites/buildings/lrg_building_4_tr.png")
        Wall.lrg_4_bl = pygame.image.load(
            "images/sprites/buildings/lrg_building_4_bl.png")
        Wall.lrg_4_br = pygame.image.load(
            "images/sprites/buildings/lrg_building_4_br.png")
        Wall.lrg_5_tl = pygame.image.load(
            "images/sprites/buildings/lrg_building_5_tl.png")
        Wall.lrg_5_tr = pygame.image.load(
            "images/sprites/buildings/lrg_building_5_tr.png")
        Wall.lrg_5_bl = pygame.image.load(
            "images/sprites/buildings/lrg_building_5_bl.png")
        Wall.lrg_5_br = pygame.image.load(
            "images/sprites/buildings/lrg_building_5_br.png")
        Wall.has_images = True



