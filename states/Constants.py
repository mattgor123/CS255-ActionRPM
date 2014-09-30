

# Constants (ALL MUST BE INTEGERS except INTERVAL)
class Constants(object):
    WIDTH = None
    HEIGHT = None
    INTERVAL = .01
    PLAYER_MAX_SPEED = 300
    PLAYER_MIN_SPEED = (1 / INTERVAL) - 10
    PLAYER_ACCELERATION = 75
    ENEMY_COUNT = 13
    ENEMY_SPEEDS = 6
    DIFFICULTY = 10
    SCREEN = None
    STATE = None
    PLAYER_STARTING_HEALTH = 100
    HIGH_SCORE_FILE = 'scores.dat'
