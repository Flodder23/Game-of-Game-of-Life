# ---  a,b refers to cell (a,b) whereas x,y refers to pixel coordinates --- #

import pygame
import math as maths
import config
import preset
import time
import random


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
    aa = a - 1
    ab = a + 1
    ba = b - 1
    bb = b + 1
    if config.Wrap and a == config.Width-1:
        ab = 0
    if config.Wrap and b == config.Height-1:
        bb = 0

    total[Board[aa][b].CurrentState] += 1
    total[Board[a][ba].CurrentState] += 1
    total[Board[ab][b].CurrentState] += 1
    total[Board[a][bb].CurrentState] += 1
    total[Board[aa][ba].CurrentState] += 1
    total[Board[ab][ba].CurrentState] += 1
    total[Board[aa][bb].CurrentState] += 1
    total[Board[ab][bb].CurrentState] += 1
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
    return [[Cell() for _ in range(config.Height + (2 * config.Cushion))] for _ in
            range(config.Width + 2 * config.Cushion)]


def draw(state, a, b, colour):
    """Draws a type of cell (Type) at the desired cell (a,b)"""
    x = (a - config.Cushion) * config.Size + config.Edge / 2
    y = (b - config.Cushion) * config.Size + config.Edge / 2
    s = config.Size - config.Edge
    pygame.draw.rect(Screen, (255, 255, 255), (x, y, s, s))
    if state == config.Square:
        pygame.draw.rect(Screen, colour, (x, y, s, s))


def check_user_input(board, paused, gps, gps_limit):
    """Checks for user input and acts accordingly"""
    one_turn = False
    for event in pygame.event.get():
        x, y = pygame.mouse.get_pos()
        a = x // config.Size + config.Cushion
        b = y // config.Size + config.Cushion
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            paused = not paused
        if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
            pygame.quit()
            import sys
            sys.exit(0)
        for key in range(pygame.K_1, pygame.K_8):
            if pygame.key.get_pressed()[key]:
                board = preset.place(board, int(pygame.key.name(key)), a, b)
        if pygame.key.get_pressed()[pygame.K_f]:
            gps_limit = not gps_limit
            draw_gps_slider(((maths.log(gps, 10) + 1) / -3) * (config.EndOfSlider - config.StartOfSlider) +
                            config.EndOfSlider, gps_limit)
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            one_turn = True
        if pygame.key.get_pressed()[pygame.K_RETURN]:
            board = clean_board()
            global Generations
            Generations = 0
        if pygame.mouse.get_pressed()[0]:
            if config.Size * config.Width + config.Edge / 2 < x < config.Size * config.Width + config.ButtonSize + \
                            config.Edge / 2:  # within the button+GPS slider area
                if y < config.StartOfSlider:
                    y = config.StartOfSlider
                elif y > config.EndOfSlider:
                    y = config.EndOfSlider
                gps_limit = True
                draw_gps_slider(y, gps_limit)
                min_gps_log = maths.log(config.MinGPS, config.MaxGPS)
                gps = config.MaxGPS ** (((1 - min_gps_log) * (config.EndOfSlider - y) /
                                         (config.EndOfSlider - config.StartOfSlider)) + min_gps_log)
            elif 0 <= a < config.Width + config.Cushion and 0 <= b < config.Height + config.Cushion:
                Board[a][b].birth(config.Square)
        if pygame.mouse.get_pressed()[2]:
            board[a][b].kill()
    return board, paused, one_turn, gps, gps_limit


def draw_board():
    """Draws the board"""
    pygame.display.set_caption("Game of Life - Generation " + str(Generations))
    for a in range(config.Cushion, config.Cushion + config.Width):
        for b in range(config.Cushion, config.Cushion + config.Height):
            if Board[a][b].NextState == config.Dead:
                colour = (255, 255, 255)
            else:
                colour = (0, 0, 0)
            draw(Board[a][b].NextState, a, b, colour)  # Draws the cell as desired


def take_turn(board):
    """Returns the given board as it will be after one turn; changes the NextState variables"""
    if config.Wrap:
        cushion = 0
    else:
        cushion = 1
    for a in range(cushion, config.Width + (2 * config.Cushion) - cushion):  # Goes through all cells and kills
        for b in range(cushion, config.Height + (2 * config.Cushion) - cushion):  # those that will die and births
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


def draw_gps_slider(y, gps_limit):
    """Draws the slider with the y coordinate of the button click
       (How many GPS this corresponds to is not dealt with here.)"""
    if y < config.StartOfSlider:
        y = config.StartOfSlider
    elif y > config.EndOfSlider:
        y = config.EndOfSlider
    pygame.draw.rect(Screen, config.Background, ((config.ButtonStart, config.StartOfSlider - config.NotchLength),
                                                 (config.ButtonStart + config.Edge + config.Border +
                                                  config.ButtonSize, config.EndOfSlider)))
    pygame.draw.line(Screen, (180, 180, 180), (config.SliderY, config.StartOfSlider), (config.SliderY,
                                                                                       config.EndOfSlider))
    for n in range(config.Notches):
        pygame.draw.line(Screen, (180, 180, 180), (config.SliderY - config.NotchLength / 2,
                                                   config.StartOfSlider + n * config.SpaceBetweenNotches),
                         (config.SliderY + config.NotchLength / 2,
                          config.StartOfSlider + n * config.SpaceBetweenNotches))
    config.write(Screen, config.SliderY - (12 + config.NotchLength), (config.StartOfSlider + config.EndOfSlider) * 0.5,
                 "Speed", (180, 180, 180), 20,
                 rotate=90, alignment=("left", "centre"))
    if gps_limit:
        colour = (0, 255, 100)
    else:
        colour = (160, 160, 160)
    pygame.draw.polygon(Screen, colour, ((config.SliderY + config.NotchLength / 2, y),
                                         (config.SliderY + config.NotchLength, y - config.NotchLength / 2),
                                         (config.SliderY + 2 * config.NotchLength, y - config.NotchLength / 2),
                                         (config.SliderY + 2 * config.NotchLength, y + config.NotchLength / 2),
                                         (config.SliderY + config.NotchLength, y + config.NotchLength / 2)))


pygame.init()
Screen = pygame.display.set_mode((config.Size * config.Width + config.ButtonSize, config.Size * config.Height))
Screen.fill(config.Background)
Board = clean_board()
Paused = True
GPS = 10
GPSLimit = True
draw_gps_slider(((maths.log(GPS, 10) + 1) / -3) * (config.EndOfSlider - config.StartOfSlider) + config.EndOfSlider,
                GPSLimit)
LastFrame = time.time()  # The time when the last frame update happened.
Generations = 0

for _ in range(int(config.Width * config.Height / 5)):
    rx = random.randint(config.Cushion, config.Cushion + config.Width - 1)
    ry = random.randint(config.Cushion, config.Cushion + config.Height - 1)
    Board[rx][ry].CurrentState = 0
    Board[rx][ry].birth(config.Square)  # random.randint(0, config.NoOfButtons - 1))

while True:
    Board, Paused, OneTurn, GPS, GPSLimit = check_user_input(Board, Paused, GPS, GPSLimit)
    Board = update_board(Board)
    if (not Paused or (Paused and OneTurn)) and ((not GPSLimit) or time.time() - LastFrame > 1 / GPS):
        if OneTurn:
            OneTurn = False
        Board = take_turn(Board)
        Board = update_board(Board)
        LastFrame = time.time()
        Generations += 1
    draw_board()
    pygame.display.update()
