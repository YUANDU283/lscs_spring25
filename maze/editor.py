#!/usr/bin/env python3
import pygame
import random
import sys
import colors
from constants import *
from mazes import maze_data1
import argparse
import time

BUTTON_H = 40
BUTTON_W = 100
FONT_SIZE = 28
mousedown = False
press_limit = 0.3
press_time = 0
pressed = 0


def output(maze, file_name="mazes.py"):
    """
    Output maze data to a file
    Args:
        maze: list[list[int]]
        file_name: str, default="mazes.py"
    """
    print("Outputting to file")
    with open(file_name, "w") as f:
        f.write("from constants import *\nmaze_data1 = [[1 for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]")
        f.write("\nmaze_data1 = [\n")
        for row in maze:
            f.write("        " + str(row) + ",\n")
        f.write("]\n")
    print("Saved to file")


def get_cell_position(mouse_pos):
    """
    Get cell position from mouse position
    Args:
        mouse_pos: tuple[int, int]
        Returns: tuple[int, int]
    """
    cell_x = mouse_pos[0] // CELL_SIZE
    cell_y = mouse_pos[1] // CELL_SIZE
    return cell_x, cell_y


def draw_maze(screen, maze):
    rows = len(maze)
    cols = len(maze[0])
    for r in range(rows):
        for c in range(cols):
            rect = pygame.Rect(c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if maze[r][c] == 1:
                color = colors.WALL_COLOR
            else:
                color = colors.UNEXPLORED_COLOR
            pygame.draw.rect(screen, color, rect)

def highlight_cell(screen, mouse_pos):
    """
    Highlight cell boundary on mouseover
    Args:
        screen: pygame.Surface
        mouse_pos: tuple[int, int]
    """
    cell_x, cell_y = get_cell_position(mouse_pos)
    if is_valid_cell(cell_x, cell_y):
        pygame.draw.rect(
            screen,
            colors.FOCUS_COLOR,
            (cell_x * CELL_SIZE, cell_y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
            2,
        )


def draw_button(button_rect, screen, mouse_pos, mouse_pushed_in):
    """
    Draw button on screen
    Args:
        button_rect: pygame.Rect
        screen: pygame.Surface
        mouse_pos: tuple[int, int],
        mouse_pushed_in: tuple[bool, bool, bool], whether mouse buttons are pressed, left_button, middle_button, right_button respectively
    """

    if button_rect.collidepoint(mouse_pos):
        # Change cursor when hovering over the button
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        # Change button color when hovering over the button
        button_color = colors.BUTTON_COLORS["hover"]
        button_text_color = colors.BUTTON_COLORS["hove_text"]
    else:
        # Set to default cursor otherwise
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        # Set button color to normal
        button_color = colors.BUTTON_COLORS["normal"]
        button_text_color = colors.BUTTON_COLORS["text"]

    # slightly shrink button when clicked
    if mouse_pushed_in[0] and button_rect.collidepoint(mouse_pos):
        button_rect = button_rect.inflate(-10, -10)

    pygame.draw.rect(screen, button_color, button_rect, border_radius=10)

    font = pygame.font.Font(None, FONT_SIZE)
    button_text = font.render("Export", True, button_text_color)

    text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, text_rect)


def is_valid_cell(cell_x, cell_y):
    """
    Check if cell is within maze bounds
    """
    return 0 <= cell_x < NUM_COLS and 0 <= cell_y < NUM_ROWS


def handle_mouse_click(mouse_pos, maze_data, button):
    global press_limit
    global press_time
    """
    Flip cell value on click
    Output maze data on button click
    Args:
        mouse_pos: tuple[int, int]
        maze_data: list[list[int]]
        button: pygame.Rect
    """
    cell_x, cell_y = get_cell_position(mouse_pos)
    if is_valid_cell(cell_x, cell_y):
        if press_time < press_limit:
            maze_data[cell_y][cell_x] = 1 - maze_data[cell_y][cell_x]
            if pygame.mouse.get_pressed()[2]:
                maze_data[cell_y][cell_x] = 1
        elif pygame.mouse.get_pressed()[2]:
            maze_data[cell_y][cell_x] = 1
        else:
            maze_data[cell_y][cell_x] = 0
    # Output maze data on button click
    elif button.collidepoint(pygame.mouse.get_pos()):
        output(maze_data)


def redraw_maze(screen, maze_data, button, mouse_pos, mouse_pushed_in):
    screen.fill(colors.WHITE)
    # Draw maze
    draw_maze(screen, maze_data)

    # Draw button
    draw_button(button, screen, mouse_pos, mouse_pushed_in)

    # Highlight cell on mouseover
    highlight_cell(screen, mouse_pos)

    # Update screen
    pygame.display.flip()
    pygame.time.Clock().tick(30)


# Maze data (1s are walls, 0s are empty cells)
def init_maze(start_new):
    if start_new:
        maze_data = [
            [random.choice([0, 1]) for _ in range(NUM_COLS)]
            for _ in range(NUM_ROWS)
        ]
    else:
        maze_data = maze_data1
    return maze_data


def quit():
    pygame.quit()
    sys.exit()

def main():
    parser = argparse.ArgumentParser(description="Maze Editor")
    parser.add_argument(
        "--new", action="store_true", help="Start with a new maze"
    )
    args = parser.parse_args()
    run(args.new)

def run(start_new=False):
    global mousedown
    global press_time

    width = SCREEN_WIDTH
    height = SCREEN_HEIGHT + 2 * BUTTON_H

    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Maze Editor")

    # Button Rect
    button = pygame.Rect(
        (width - BUTTON_W) // 2,
        (height - BUTTON_H) - BUTTON_H // 2,
        BUTTON_W,
        BUTTON_H,
    )

    maze_data = init_maze(start_new)

    # Main loop
    while True:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mousedown = True
                pressed = time.time()
            elif event.type == pygame.MOUSEBUTTONUP:
                mousedown = False
        if pygame.mouse.get_pressed()[0] or pygame.mouse.get_pressed()[2]:
            press_time = time.time()-pressed
            handle_mouse_click(mouse_pos, maze_data, button)

        mouse_pushed_in = pygame.mouse.get_pressed()
        redraw_maze(screen, maze_data, button, mouse_pos, mouse_pushed_in)

    quit()


if __name__ == "__main__":
    main()