
############
# Database #
############
DATABASE_DIR = 'storage'
DATABASE_NAME = 'score.db'

########
# Game #
########
PLAYER_LIVES = 3
LEVELS = 10
PACMAN_SPEED_PER_LVL = {1: 10, 2: 10, 3: 10, 4: 9, 5: 9,
                        6: 9, 7: 8, 8: 8, 9: 7, 10: 5}

##########
# Ghosts #
##########
GHOST_SPEED_PER_LVL = {1: 30, 2: 19, 3: 18, 4: 17, 5: 16,
                       6: 15, 7: 14, 8: 13, 9: 12, 10: 11}
EATEN_GHOST_SPEED = 5
CHASING_GHOST_TIME = 14
FRIGHTENED_GHOST_TIME = 12
SCATTER_GHOST_TIME = 5

########
# Maze #
########
MAZE_SEED = {1: 30, 2: 28, 3: 26, 4: 24, 5: 22,
             6: 20, 7: 18, 8: 16, 9: 14, 10: 12}
MAZE_NR_CELLS = 8

########
# Time #
########
COUNTDOWN_TIME = 4
LEVEL_TIME = 90
GAME_OVER_CD_TIME = 5
