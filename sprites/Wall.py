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


        else:
            self.image = Wall.default_wall


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
        Wall.default_wall = pygame.image.load(
            "images/sprites/wall/default_wall.png")
        Wall.has_images = True



