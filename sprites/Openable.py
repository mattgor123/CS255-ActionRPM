import Tile


class Openable(Tile.Tile):
    def __init__(self, x, y, starting_strength):
        Tile.Tile.__init__(self, starting_strength)
        self.x = x
        self.y = y
        self.opened = False

    def open(self):
        self.opened = True
        Tile.Tile.set_strength(self, -1)

    def __str__(self):
        return 'o'
