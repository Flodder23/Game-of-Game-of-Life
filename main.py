# ---  a,b refers to cell (a,b) whereas x,y refers to pixel coordinates --- #

import pygame
import math as maths
import config
import preset
import time
import random


class Cell:
    def __init__(self, a, b, current, next, colour):
        """a,b are the coordinates of the cell the instance represents."""
        self.CurrentState = current
        self.NextState = next
        self.BoardPos = (a, b)
        self.Coordinates = ((self.BoardPos[0] - config.Cushion) * config.Size + config.Edge / 2,
                            (self.BoardPos[1] - config.Cushion) * config.Size + config.Edge / 2)
        self.Colour = colour
        self.type = self.get_type()

    def kill(self):
        self.NextState = config.Dead
        self.Colour = GameState.Colour["Dead"]

    def birth(self, state, colour):
        self.NextState = state
        self.Colour = colour

    def check_fate(self):
        """Checks whether the cell will be dead or alive at the end of this turn,
            and if so what type it will be"""
        total = [0, 0, 0]
        a, b = self.BoardPos
        al = a - 1  # a left (neighbour)
        ar = a + 1  # a right
        bu = b - 1  # b up
        bd = b + 1  # b down
        if Board.Wrap and a == Board.Width - 1:
            ar = 0
        if Board.Wrap and b == Board.Height - 1:
            bd = 0
        if self.CurrentState == config.Dead or self.CurrentState == config.Square or self.CurrentState == config.Hex:
            total[Board.Cell[al][b].CurrentState] += 1
            total[Board.Cell[a][bu].CurrentState] += 1
            total[Board.Cell[ar][b].CurrentState] += 1
            total[Board.Cell[a][bd].CurrentState] += 1
        if self.CurrentState == config.Dead or self.CurrentState == config.Square:
            total[Board.Cell[al][bu].CurrentState] += 1
            total[Board.Cell[ar][bu].CurrentState] += 1
            total[Board.Cell[al][bd].CurrentState] += 1
            total[Board.Cell[ar][bd].CurrentState] += 1
        new = config.Dead
        birth = False
        if self.CurrentState == config.Dead:
            if total[config.Dead] == 5:  # if 5 dead cells; ie. if 3 alive cells
                birth = True
        elif self.CurrentState == config.Square:
            if total[config.Dead] == 5 or total[config.Dead] == 6:
                birth = True
        elif self.CurrentState == config.Hex:
            if total[config.Dead] == 2 or total[config.Dead] == 3:
                birth = True
        if birth:
            del total[0]
            new = total.index(max(total)) + 1
        return new

    def get_type(self):
        pass


class Square(Cell):
    def draw(self, colour=None):
        """Draws a type of cell (Type) at the desired cell (a,b)"""
        if colour == None: colour = self.Colour
        x, y = self.Coordinates
        s = Board.Size - Board.Edge
        pygame.draw.rect(Screen, GameState.Colour["Dead"], (x, y, s, s))
        if self.CurrentState == config.Square:
            pygame.draw.rect(Screen, colour, (x, y, s, s))

    def get_type(self):
        return config.Square


class Hex(Cell):
    def draw(self, colour=None):
        """Draws a type of cell (Type) at the desired cell (a,b)"""
        if colour == None: colour = self.Colour
        x, y = self.Coordinates
        s = Board.Size - Board.Edge
        pygame.draw.rect(Screen, GameState.Colour["Dead"], (x, y, s, s))
        if self.CurrentState == config.Hex:
            t = maths.sqrt(2)
            s /= (1 + t)
            a = x  # a-h are points along the edge of the square
            b = maths.floor(x + (s * t / 2))
            c = maths.floor(x + s + (s * t / 2))
            d = maths.floor(x + s * (1 + t))
            e = y
            f = maths.floor(y + (s * t / 2))
            g = maths.floor(y + s + (s * t / 2))
            h = maths.floor(y + s * (1 + t))

            pygame.draw.polygon(Screen, colour, ((b, e), (c, e),
                                                 (d, f), (d, g),
                                                 (c, h), (b, h),
                                                 (a, g), (a, f)))


class Board:
    def __init__(self):
        self.Width = config.Width
        self.Height = config.Height
        self.Size = config.Size
        self.Wrap = config.Wrap
        self.Edge = config.Edge
        self.Generations = 0
        self.Cushion = config.Cushion
        self.Cell = [[Square(a, b, config.Square, config.Dead, GameState.Colour["Dead"]) for b in range(
            self.Height + (2 * self.Cushion))] for a in range(self.Width + 2 * self.Cushion)]
        pygame.display.set_caption("Game of Life - Generation 0")

    def draw(self):
        """draws the current board onto the screen then updates the display"""
        for a in range(self.Cushion, self.Cushion + self.Width):
            for b in range(self.Cushion, self.Cushion + self.Height):
                self.Cell[a][b].draw((0, 0, 0))
        pygame.display.update()

    def update(self):
        """Puts the NextState variables in the CurrentState variables"""
        for a in range(self.Width + 2 * self.Cushion):
            for b in range(self.Height + 2 * self.Cushion):
                self.Cell[a][b].CurrentState = self.Cell[a][b].NextState

    def take_turn(self):
        """Changes the CurrentState variables & updates display caption"""
        pygame.display.set_caption("Game of Life - Generation " + str(self.Generations))
        if self.Wrap:
            cushion = 0
        else:
            cushion = 1
        for a in range(cushion, self.Width + (2 * self.Cushion) - cushion):  # Goes through all cells and kills
            for b in range(cushion, self.Height + (2 * self.Cushion) - cushion):  # those that will die and births
                fate = Board.Cell[a][b].check_fate()  # those that will be born.
                if fate == config.Dead:
                    self.Cell[a][b].kill()
                else:
                    self.Cell[a][b].birth(fate, GameState.Colour["Alive"])

    def place_preset(self, preset_no, a, b):
        if self.Wrap:
            shape = preset.get(preset_no, a, b)[0]
        else:
            shape, a, b = preset.get(preset_no, a, b)
        for c in range(len(shape)):
            for d in range(len(shape[c])):
                if self.Wrap:
                    if a + c >= self.Width:
                        a -= self.Width
                    if b + d >= self.Height:
                        b -= self.Height
                if shape[c][d] == 0:
                    self.Cell[a + c][b + d].kill()
                else:
                    self.Cell[a + c][b + d].birth(shape[c][d], GameState.Colour["Alive"])
        self.update()
        self.draw()

    def reset(self):
        self.__init__()
        self.update()
        self.draw()


def check_user_input(game_state):
    """Checks for user input and acts accordingly"""

    events = pygame.event.get()
    x, y = pygame.mouse.get_pos()
    a = x // Board.Size + Board.Cushion
    b = y // Board.Size + Board.Cushion
    for event in events:
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            game_state.Paused = not game_state.Paused
        if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
            pygame.quit()
            import sys
            sys.exit(0)
        for key in range(pygame.K_1, pygame.K_9):
            if pygame.key.get_pressed()[key]:
                Board.place_preset(int(pygame.key.name(key)), a, b)
        if pygame.key.get_pressed()[pygame.K_f]:
            game_state.GPSIsLimited = not game_state.GPSIsLimited
            bottom_gps_log = maths.log(game_state.BottomGPS, game_state.TopGPS)
            draw_gps_slider(Widgets.EndOfSlider - ((maths.log(game_state.GPS, game_state.TopGPS) - bottom_gps_log) *
                                                   (Widgets.EndOfSlider - Widgets.StartOfSlider)) /
                            (1 - bottom_gps_log), game_state.GPSIsLimited)
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
                    game_state.GPSIsLimited = True
                draw_gps_slider(y, game_state.GPSIsLimited)
                bottom_gps_log = maths.log(game_state.BottomGPS, game_state.TopGPS)
                game_state.GPS = game_state.TopGPS ** (((1 - bottom_gps_log) * (Widgets.EndOfSlider - y) /
                                                        (Widgets.EndOfSlider - Widgets.StartOfSlider)) + bottom_gps_log)
            elif 0 <= a < Board.Width + Board.Cushion and 0 <= b < Board.Height + Board.Cushion:
                Board.Cell[a][b].birth(config.Square, GameState.Colour["Alive"])
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
    write(Screen, Widgets.SliderY - (12 + Widgets.NotchLength),
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


def write(screen, x, y, text, colour, size, rotate=0, alignment=("left", "top")):
    """Puts text onto the screen at point x,y. the alignment variable, if used, can take first value \"left\",
    \"centre\" or \"right\" and the second value can be \"top\", \"centre\" or \"bottom\".
    note that these values relate to x and y respectively whatever the rotation, which is in degrees."""
    font_obj = pygame.font.Font("freesansbold.ttf", size)
    msg_surface_obj = pygame.transform.rotate(font_obj.render(text, False, colour), rotate)
    msg_rect_obj = msg_surface_obj.get_rect()
    a, b = msg_surface_obj.get_size()
    if alignment[0] == "centre":
        x -= a / 2
    elif alignment[0] == "right":
        x -= a
    if alignment[1] == "centre":
        y -= b / 2
    elif alignment[1] == "bottom":
        y -= b
    msg_rect_obj.topleft = (x, y)
    screen.blit(msg_surface_obj, msg_rect_obj)


def get_menu_choice(game_state, screen):
    size = 50
    border = 4

    centre = [screen.get_width() / 2, (screen.get_height() / 2) - size * 1.5]
    for a in range(2):
        pygame.draw.rect(screen, (255, 255, 255), (centre[0] - 5 * size, centre[1] - size, size * 10, size * 2))
        pygame.draw.rect(screen, game_state.Colour["Background"], (
            (centre[0] - 5 * size + border, centre[1] - size + border, size * 10 - border * 2, size * 2 - border * 2)))
        centre = [screen.get_width() / 2, (screen.get_height() / 2) + size * 1.5]

    write(screen, screen.get_width() / 2, size * 2, "Main Menu", (255, 255, 255), size, alignment=("centre", "centre"))

    while True:
        pygame.event.get()
        x, y = pygame.mouse.get_pos()
        top_colour = (255, 255, 255)
        bottom_colour = (255, 255, 255)
        if screen.get_width() / 2 - 5 * size < x < screen.get_width() / 2 + 5 * size:
            if (screen.get_height() / 2) - size * 1.5 - size < y < (screen.get_height() / 2) - size * 1.5 + size:
                if pygame.mouse.get_pressed()[0]:
                    return "Sim"
                top_colour = game_state.Colour["Highlighter"]
            elif (screen.get_height() / 2) + size * 0.5 < y < (screen.get_height() / 2) + size * 2.5:
                if pygame.mouse.get_pressed()[0]:
                    return "Game"
                bottom_colour = game_state.Colour["Highlighter"]

        write(screen, screen.get_width() / 2, (screen.get_height() / 2) - size * 1.5, "Simulator", top_colour,
              int(size / 1.5), alignment=("centre", "centre"))
        write(screen, screen.get_width() / 2, (screen.get_height() / 2) + size * 1.5, "2-Player Game", bottom_colour,
              int(size / 1.5), alignment=("centre", "centre"))

        pygame.display.update()


pygame.init()
pygame.event.set_allowed(None)
allowed_events = [pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN, pygame.KEYUP, pygame.QUIT]
for event in allowed_events:
    pygame.event.set_allowed(event)
GameState = config.GameState()
Widgets = config.Widgets()
Board = Board()
Screen = pygame.display.set_mode((Board.Size * Board.Width + Widgets.ButtonSize, Board.Size * Board.Height))
Screen.fill(GameState.Colour["Background"])

if get_menu_choice(GameState, Screen) == "Sim":
    Screen.fill(GameState.Colour["Background"])
    draw_gps_slider(
        ((maths.log(GameState.GPS, 10) + 1) / -3) * (
            Widgets.EndOfSlider - Widgets.StartOfSlider) + Widgets.EndOfSlider,
        GameState.GPSIsLimited)
    LastFrame = time.time()  # The time when the last frame update happened
    Board.update()
    for _ in range(int(Board.Width * Board.Height / 10)):
        Board.Cell[random.randint(Board.Cushion, Board.Cushion + Board.Width - 1)][
            random.randint(Board.Cushion, Board.Cushion + Board.Height - 1)].birth(random.randint(1, 2),
                                                                                   GameState.Colour["Alive"])
    Board.update()
    Board.draw()
    
    while True:
        GameState = check_user_input(GameState)
        Board.update()
        if (not GameState.Paused or (GameState.Paused and GameState.OneTurn)) and \
                ((not GameState.GPSIsLimited) or time.time() - LastFrame > 1 / GameState.GPS):
            if GameState.OneTurn:
                GameState.OneTurn = False
            Board.take_turn()
            Board.update()
            Board.Generations += 1
            Board.draw()
            LastFrame = time.time()

else:
    print("Sorry, function not avaliable yet")