from constants import *

MAZE1 = [[1 for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

START_POSITION = (len(MAZE1)-1, 0) # default is top right and bottom left corners
END_POSITION = (0, len(MAZE1[0])-1)

import mazes
MAZE1 = mazes.maze_data1