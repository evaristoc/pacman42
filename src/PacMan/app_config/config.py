
############
# Database #
############
DATABASE_DIR = 'storage'
DATABASE_NAME = 'score.db'

########
# Game #
########
PLAYER_LIVES = 6
LEVELS = 10
PACMAN_SPEED_PER_LVL = {1: 25, 2: 28, 3: 26, 4: 24, 5: 22,
                        6: 20, 7: 18, 8: 16, 9: 14, 10: 12}

##########
# Ghosts #
##########
GHOST_SPEED_PER_LVL = {1: 35, 2: 28, 3: 26, 4: 24, 5: 22,
                       6: 20, 7: 18, 8: 16, 9: 14, 10: 12}
EATEN_GHOST_SPEED = 10
CHASING_GHOST_TIME = 14
FRIGHTENED_GHOST_TIME = 12
SCATTER_GHOST_TIME = 5

########
# Maze #
########
MAZE_SEED = {1: 30, 2: 28, 3: 26, 4: 24, 5: 22,
             6: 20, 7: 18, 8: 16, 9: 14, 10: 12}
MAZE_NR_CELLS = 5

########
# Time #
########
COUNTDOWN_TIME = 4
LEVEL_TIME = 90
