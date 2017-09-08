# ---  a,b refers to cell (a,b) whereas x,y refers to pixel coordinates --- #

import pygame
import math as maths
import config
import preset


class Cell:
    def __init__(self):
        self.CurrentState = config.Square
        self.NextState = config.Dead

    def kill(self):
        self.NextState = config.Dead

    def birth(self, state):
        self.NextState = state


def check(a, b):
    """Checks whether the cell will be dead or alive at the end of this turn,
    and if so what type it will be"""
    state = Board[a][b].CurrentState
    total = [0, 0]
    total[Board[a + 1][b].CurrentState] += 1
    total[Board[a][b + 1].CurrentState] += 1
    total[Board[a - 1][b].CurrentState] += 1
    total[Board[a][b - 1].CurrentState] += 1
    total[Board[a + 1][b + 1].CurrentState] += 1
    total[Board[a - 1][b - 1].CurrentState] += 1
    total[Board[a + 1][b - 1].CurrentState] += 1
    total[Board[a - 1][b + 1].CurrentState] += 1
    new = config.Dead
    if state == config.Dead:
        if total[config.Dead] == 5:  # if 5 dead cells; ie. if 3 alive cells
            new = config.Square
    if state == config.Square:
        if total[config.Dead] == 5 or total[config.Dead] == 6:
            new = config.Square
    return new


def clean_board():
    """Returns a new, blank board"""
    # noinspection PyUnusedLocal
    return [[Cell() for a in range(config.Height + (2 * config.Cushion))] for b in
            range(config.Width + 2 * config.Cushion)]


def draw(state, a, b, colour):
    """Draws a type of cell (Type) at the desired cell (a,b)"""
    x = (a - config.Cushion) * config.Size + config.Edge / 2
    y = (b - config.Cushion) * config.Size + config.Edge / 2
    s = config.Size - config.Edge
    pygame.draw.rect(Screen, (255, 255, 255), (x, y, s, s))
    if state == config.Square:
        pygame.draw.rect(Screen, colour, (x, y, s, s))


# noinspection PyShadowingNames
def check_user_input(board, paused):
    """Checks for user input and acts accordingly"""
    one_turn = False
    for event in pygame.event.get():
        x, y = pygame.mouse.get_pos()
        a = maths.floor(x / config.Size) + config.Cushion
        b = maths.floor(y / config.Size) + config.Cushion
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            if paused:
                paused = False
            else:
                paused = True
        if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
            pygame.quit()
            import sys
            sys.exit(0)
        for key in range(pygame.K_1, pygame.K_8):
            if pygame.key.get_pressed()[key]:
                board = preset.place(board, int(pygame.key.name(key)), a, b)
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            one_turn = True
        if pygame.key.get_pressed()[pygame.K_RETURN]:
            board = clean_board()
        if pygame.mouse.get_pressed()[0]:
            board[a][b].birth(config.Square)
        if pygame.mouse.get_pressed()[2]:
            board[a][b].kill()
    return board, paused, one_turn


def draw_board():
    """Draws the board"""
    for a in range(config.Cushion, config.Cushion + config.Width):
        for b in range(config.Cushion, config.Cushion + config.Height):
            if Board[a][b].NextState == config.Dead:
                colour = (255, 255, 255)
            else:
                colour = (0, 0, 0)
            draw(Board[a][b].NextState, a, b, colour)  # Draws the cell as desired


def take_turn(board):
    """Returns the given board as it will be after one turn; changes the NextState variables"""
    for a in range(1, config.Width + (2 * config.Cushion) - 1):  # Goes through all cells and kills
        for b in range(1, config.Height + (2 * config.Cushion) - 1):  # those that will die and births
            fate = check(a, b)  # those that will be born.
            if fate == config.Dead:
                board[a][b].kill()
            else:
                board[a][b].birth(fate)
    return board


def update_board(board):
    """Updates the given board and returns it; puts NextState values in CurrentState"""
    for a in range(config.Width + 2 * config.Cushion):
        for b in range(config.Height + 2 * config.Cushion):
            board[a][b].CurrentState = board[a][b].NextState
    return board


pygame.init()
Screen = pygame.display.set_mode((config.Size * config.Width, config.Size * config.Height))
Screen.fill(config.Background)
pygame.display.set_caption("Game of Life")
Board = clean_board()
Paused = True

while True:
    Board, Paused, OneTurn = check_user_input(Board, Paused)  # If game is paused OneTurn allows you
    Board = update_board(Board)                                 # to go forward one turn at a time
    if not Paused or (Paused and OneTurn):
        if OneTurn:
            OneTurn = False
        Board = take_turn(Board)
        Board = update_board(Board)
    draw_board()
    pygame.display.update()
