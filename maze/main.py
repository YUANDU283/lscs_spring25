#!/usr/bin/env python3
import pygame
import sys
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE, FPS
import colors
from maze_data import MAZE1, START_POSITION, END_POSITION
import copy
from mazes import *
import time

#sys.setrecursionlimit(999999) 
#print(sys.getrecursionlimit())

possible_paths = []

def draw_maze(
    screen,
    maze, 
    player_pos
):
    """
    Draw the maze, highlighting visited cells, step numbers,
    and optionally the final path. Also label start/end squares.
    """
    font = pygame.font.SysFont(None, 20)  # Font for step labels

    rows = len(maze)
    cols = len(maze[0])

    # 1) Draw the base maze
    for r in range(rows):
        for c in range(cols):
            rect = pygame.Rect(c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if maze[r][c] == 1:
                color = colors.WALL_COLOR
            elif [r, c] == player_pos:
                color = colors.FOCUS_COLOR
            else:
                color = colors.UNEXPLORED_COLOR
            pygame.draw.rect(screen, color, rect)

    # 4) Label the start and end squares with "A" and "B"
    #    (on top of whatever color they currently have)
    start_r, start_c = START_POSITION
    start_rect = pygame.Rect(
        start_c * CELL_SIZE, start_r * CELL_SIZE, CELL_SIZE, CELL_SIZE
    )
    pygame.draw.rect(screen, colors.START_COLOR, start_rect)
    start_text = font.render("A", True, (255, 255, 255))  # white text
    start_text_rect = start_text.get_rect(center=start_rect.center)
    screen.blit(start_text, start_text_rect)

    end_r, end_c = END_POSITION
    end_rect = pygame.Rect(end_c * CELL_SIZE, end_r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, colors.END_COLOR, end_rect)
    end_text = font.render("B", True, (255, 255, 255))  # white text
    end_text_rect = end_text.get_rect(center=end_rect.center)
    screen.blit(end_text, end_text_rect)


def draw_grid(screen):
    rows = len(MAZE1)
    cols = len(MAZE1[0])
    for r in range(rows):
        pygame.draw.line(
            screen,
            colors.GRID_COLOR,
            (0, r * CELL_SIZE),
            (cols * CELL_SIZE, r * CELL_SIZE),
        )

    for c in range(cols):
        pygame.draw.line(
            screen,
            colors.GRID_COLOR,
            (c * CELL_SIZE, 0),
            (c * CELL_SIZE, rows * CELL_SIZE),
        )


def run_game(screen, clock):
    
    # Start at the defined starting position.
    player_pos = list(START_POSITION)

    running = True
    start = time.time()
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                old_pos = copy.copy(player_pos)
                if event.key == pygame.K_w:
                    player_pos[0] = max(0, player_pos[0]-1)
                elif event.key == pygame.K_s:
                    player_pos[0] = min(len(MAZE1)-1, player_pos[0]+1)
                if event.key == pygame.K_a:
                    player_pos[1] = max(0, player_pos[1]-1)
                elif event.key == pygame.K_d:
                    player_pos[1] = min(len(MAZE1[0])-1, player_pos[1]+1)
                if MAZE1[player_pos[0]][player_pos[1]] == 1:
                    player_pos = old_pos

        if player_pos == list(END_POSITION):
            break
        # Clear the screen.
        screen.fill((0, 0, 0))
        
        draw_maze(screen, MAZE1, player_pos)
        draw_grid(screen)
        pygame.display.flip()
    end = time.time()
    print(f"YOU FINISHED THE MAZE!\nYour time: {end-start}s")
    return


def main():

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Maze Game")
    clock = pygame.time.Clock()

    run_game(screen, clock)

    start = time.time()
    computer()
    end = time.time()
    print(f"Computer's time: {end-start}s")

    pygame.quit()
    sys.exit()






def all_possible_moves(map, ind=(0,0)):
    # Returns list of indices that are adjacent to square and possible to move to
    indices = [[0,1],[1,0],[-1,0],[0,-1]]
    possibles = []
    for index in indices:
        try:
            if ind[0]+index[0] > -1 and ind[1]+index[1] > -1:
                square = map[ind[0]+index[0]][ind[1]+index[1]]
            else:
                continue
        except:
            continue
        if square == 0:
            possibles.append([ind[0]+index[0], ind[1]+index[1]])
    return possibles

endorfinished = []
def plant_tree(map=MAZE1, ind=START_POSITION, path=[]):
    global possible_paths
    global endorfinished
    # Find possible moves that don't go backwards
    possibles = all_possible_moves(map, ind=ind)
    for possible in possibles:
        if possible in path:
            possibles.remove(possible)
    
    # Stop if no more moves possible or finished maze(1 because it can move backwards)
    if len(possibles) == 0 or ind == END_POSITION:
        # If path isn't to a dead end and is to the finish than it is a possible path
        #print(path)
        endorfinished.append(path)
        if ind == list(END_POSITION):
            possible_paths.append(path)
        return True
    
    # Continue to find possible paths
    for inds in possibles:
        # Find possible paths from the possible moves
        if inds in path: # Don't want to go backwards?
            continue
        path2 = copy.deepcopy(path)
        path2.append(inds)
        plant_tree(map, ind=inds, path=path2)

def climb_tree(possible_paths=possible_paths):
    # If multiple shortest paths, it will pick the first one it sees
    for i in endorfinished:
        print(i)
    try:
        shortest_path = possible_paths[0]
    except IndexError:
        print("No solution to maze")
        return
    for possible_path in possible_paths:
        # If shorter than current shortest path it becomes the new shortest path
        if len(possible_path) < len(shortest_path): shortest_path = possible_path
    print(shortest_path)
    return shortest_path

def computer():
    # Step 1: find all movable squares adjacent to current square
    # Step 2: add those squares to the tree
    # Step 3: repeat 1 and 2 until there is no more unexplored squares
    # Step 4: look at the ends of the tree to find all paths to B
    # Step 5: find the shortest path to B and return it
    plant_tree()
    climb_tree()


if __name__ == "__main__":
    main()