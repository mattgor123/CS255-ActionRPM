from states import Constants


class LevelChanger():
    def __init__(self):
        self.current_level = -1
        self.levels = []
        self.player = None

    def add_level(self, level):
        self.levels.append(level)

    def set_level(self, level_num):
        self.levels[self.current_level].map = None
        old_level = self.current_level
        self.current_level = level_num
        if self.levels[self.current_level] is None:
            raise Exception
        # Change player pos based on level to switch to
        self.levels[self.current_level].player(self.curplayer)
        Constants.STATE = self.levels[self.current_level]
