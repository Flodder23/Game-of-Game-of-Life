# ---  a,b refers to cell (a,b) whereas x,y refers to pixel coordinates --- #

import pygame
import math as maths
import config
import preset
import time
import random


class Cell:
    def __init__(self, a, b):
        """a,b are the coordinates of the cell the instance represents"""
        self.CurrentState = config.Square
        self.NextState = config.Dead
        self.Coordinates = (a, b)

    def kill(self):
        self.NextState = config.Dead

    def birth(self, state):
        self.NextState = state

    def draw(self, colour):
        """Draws a type of cell (Type) at the desired cell (a,b)"""
        x = (self.Coordinates[0] - Board.Cushion) * Board.Size + Board.Edge / 2
        y = (self.Coordinates[1] - Board.Cushion) * Board.Size + Board.Edge / 2
        s = Board.Size - Board.Edge
        pygame.draw.rect(Screen, (255, 255, 255), (x, y, s, s))
        if self.CurrentState == config.Square:
            pygame.draw.rect(Screen, colour, (x, y, s, s))


class Board:
    def __init__(self):  # customisable, default_value, description
        self.Width = config.Width
        self.Height = config.Height
        self.Size = config.Size
        self.Wrap = False  # Whether the board wraps around on itself
        self.Edge = config.Edge
        self.Generations = 0
        if self.Wrap:
            self.Cushion = 0  # C 10 How far the board extends beyond the visible amount
        else:
            self.Cushion = 10
        self.Cell = [[Cell(a, b) for b in range(self.Height + (2 * self.Cushion))]
                     for a in range(self.Width + 2 * self.Cushion)]

    def draw(self):
        pygame.display.set_caption("Game of Life - Generation " + str(self.Generations))
        for a in range(self.Cushion, self.Cushion + self.Width):
            for b in range(self.Cushion, self.Cushion + self.Height):
                self.Cell[a][b].draw((255, 255, 255))
        pygame.display.update()

    def update(self):
        """Puts the NextState variables in the CurrentState variables"""
        for a in range(self.Width + 2 * self.Cushion):
            for b in range(self.Height + 2 * self.Cushion):
                self.Cell[a][b].CurrentState = self.Cell[a][b].NextState

    def take_turn(self):
        """Returns the given board as it will be after one turn; changes the NextState variables"""
        if self.Wrap:
            cushion = 0
        else:
            cushion = 1
        for a in range(cushion, self.Width + (2 * self.Cushion) - cushion):  # Goes through all cells and kills
            for b in range(cushion, self.Height + (2 * self.Cushion) - cushion):  # those that will die and births
                fate = check(a, b)  # those that will be born.
                if fate == config.Dead:
                    self.Cell[a][b].kill()
                else:
                    self.Cell[a][b].birth(fate)

    def place_preset(self, preset_no, a, b):
        self = preset.place(self, preset_no, a, b)

    def reset(self):
        self.__init__()
        self.update()
        self.draw()


def check(a, b):
    """Checks whether the cell will be dead or alive at the end of this turn,
    and if so what type it will be"""
    state = Board.Cell[a][b].CurrentState
    total = [0, 0]
    al = a - 1  # a left (neighbour)
    ar = a + 1  # a right
    bu = b - 1  # b up
    bd = b + 1  # b down
    if Board.Wrap and a == Board.Width - 1:
        ar = 0
    if Board.Wrap and b == Board.Height - 1:
        bd = 0

    total[Board.Cell[al][b].CurrentState] += 1
    total[Board.Cell[a][bu].CurrentState] += 1
    total[Board.Cell[ar][b].CurrentState] += 1
    total[Board.Cell[a][bd].CurrentState] += 1
    total[Board.Cell[al][bu].CurrentState] += 1
    total[Board.Cell[ar][bu].CurrentState] += 1
    total[Board.Cell[al][bd].CurrentState] += 1
    total[Board.Cell[ar][bd].CurrentState] += 1
    new = config.Dead
    if state == config.Dead:
        if total[config.Dead] == 5:  # if 5 dead cells; ie. if 3 alive cells
            new = config.Square
    if state == config.Square:
        if total[config.Dead] == 5 or total[config.Dead] == 6:
            new = config.Square
    return new


def check_user_input(game_state):
    """Checks for user input and acts accordingly"""
    for event in pygame.event.get():
        x, y = pygame.mouse.get_pos()
        a = x // Board.Size + Board.Cushion
        b = y // Board.Size + Board.Cushion
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            game_state.Paused = not game_state.Paused
        if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
            pygame.quit()
            import sys
            sys.exit(0)
        for key in range(pygame.K_1, pygame.K_8):
            if pygame.key.get_pressed()[key]:
                Board.place_preset(int(pygame.key.name(key)), a, b)
                Board.update()
                Board.draw()
        if pygame.key.get_pressed()[pygame.K_f]:
            game_state.GPSLimit = not game_state.GPSLimit
            bottom_gps_log = maths.log(game_state.BottomGPS, game_state.TopGPS)
            draw_gps_slider(Widgets.EndOfSlider - ((maths.log(game_state.GPS, game_state.TopGPS) - bottom_gps_log) *
                                                   (Widgets.EndOfSlider - Widgets.StartOfSlider)) /
                            (1 - bottom_gps_log), game_state.GPSLimit)
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            game_state.OneTurn = True
        else:
            game_state.OneTurn = False
        if pygame.key.get_pressed()[pygame.K_RETURN]:
            Board.reset()
        if pygame.mouse.get_pressed()[0]:
            if Board.Size * Board.Width + Board.Edge / 2 < x < Board.Size * Board.Width + Widgets.ButtonSize + \
                            Board.Edge / 2:  # within the button+GPS slider area
                if y < Widgets.StartOfSlider:
                    y = Widgets.StartOfSlider
                elif y > Widgets.EndOfSlider:
                    y = Widgets.EndOfSlider
                    game_state.GPSLimit = True
                draw_gps_slider(y, game_state.GPSLimit)
                bottom_gps_log = maths.log(game_state.BottomGPS, game_state.TopGPS)
                game_state.GPS = game_state.TopGPS ** (((1 - bottom_gps_log) * (Widgets.EndOfSlider - y) /
                                                        (Widgets.EndOfSlider - Widgets.StartOfSlider)) + bottom_gps_log)
            elif 0 <= a < Board.Width + Board.Cushion and 0 <= b < Board.Height + Board.Cushion:
                Board.Cell[a][b].birth(config.Square)
                Board.update()
                Board.draw()
        if pygame.mouse.get_pressed()[2]:
            Board.Cell[a][b].kill()
            Board.update()
            Board.draw()
    return game_state


def draw_gps_slider(y, gps_limit):
    """Draws the slider with the y coordinate of the button click
       (How many GPS this corresponds to is not dealt with here.)"""
    if y < Widgets.StartOfSlider:
        y = Widgets.StartOfSlider
    elif y > Widgets.EndOfSlider:
        y = Widgets.EndOfSlider
    pygame.draw.rect(Screen, GameState.Colour["Background"],
                     ((Widgets.ButtonStart, Widgets.StartOfSlider - Widgets.NotchLength),
                      (Widgets.ButtonStart + Board.Edge + Widgets.HighlightSize +
                       Widgets.ButtonSize, Widgets.EndOfSlider)))
    pygame.draw.line(Screen, GameState.Colour["Text"], (Widgets.SliderY, Widgets.StartOfSlider), (Widgets.SliderY,
                                                                                                  Widgets.EndOfSlider))
    for n in range(Widgets.NoOfNotches):
        pygame.draw.line(Screen, GameState.Colour["Text"], (Widgets.SliderY - Widgets.NotchLength / 2,
                                                            Widgets.StartOfSlider + n * Widgets.SpaceBetweenNotches),
                         (Widgets.SliderY + Widgets.NotchLength / 2,
                          Widgets.StartOfSlider + n * Widgets.SpaceBetweenNotches))
    config.write(Screen, Widgets.SliderY - (12 + Widgets.NotchLength),
                 (Widgets.StartOfSlider + Widgets.EndOfSlider) * 0.5,
                 "Speed", GameState.Colour["Text"], 20,
                 rotate=90, alignment=("left", "centre"))
    if gps_limit:
        colour = "Highlighter"
    else:
        colour = "Unselected"
    pygame.draw.polygon(Screen, GameState.Colour[colour], ((Widgets.SliderY + Widgets.NotchLength / 2, y),
                                                           (Widgets.SliderY + Widgets.NotchLength,
                                                            y - Widgets.NotchLength / 2),
                                                           (Widgets.SliderY + 2 * Widgets.NotchLength,
                                                            y - Widgets.NotchLength / 2),
                                                           (Widgets.SliderY + 2 * Widgets.NotchLength,
                                                            y + Widgets.NotchLength / 2),
                                                           (Widgets.SliderY + Widgets.NotchLength,
                                                            y + Widgets.NotchLength / 2)))
    pygame.display.update()


pygame.init()
pygame.event.set_allowed(None)
pygame.event.set_allowed(pygame.MOUSEMOTION)
pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)
pygame.event.set_allowed(pygame.KEYDOWN)
pygame.event.set_allowed(pygame.KEYUP)
pygame.event.set_allowed(pygame.QUIT)
Board = Board()
GameState = config.GameState()
Widgets = config.Widgets()
Screen = pygame.display.set_mode((Board.Size * Board.Width + Widgets.ButtonSize, Board.Size * Board.Height))
Screen.fill(GameState.Colour["Background"])
draw_gps_slider(((maths.log(GameState.GPS, 10) + 1) / -3) * (Widgets.EndOfSlider - Widgets.StartOfSlider) +
                Widgets.EndOfSlider, GameState.GPSLimit)
LastFrame = time.time()  # The time when the last frame update happened.
for _ in range(int(Board.Width * Board.Height / 5)):
    rx = random.randint(Board.Cushion, Board.Cushion + Board.Width - 1)
    ry = random.randint(Board.Cushion, Board.Cushion + Board.Height - 1)
    Board.Cell[rx][ry].CurrentState = 0
    Board.Cell[rx][ry].birth(config.Square)  # random.randint(0, config.NoOfButtons - 1))
Board.draw()

while True:
    GameState = check_user_input(GameState)
    Board.update()
    if (not GameState.Paused or (GameState.Paused and GameState.OneTurn)) and \
            ((not GameState.GPSLimit) or time.time() - LastFrame > 1 / GameState.GPS):
        if GameState.OneTurn:
            GameState.OneTurn = False
        Board.take_turn()
        Board.update()
        Board.Generations += 1
        Board.draw()
        LastFrame = time.time()