# ---  a,b refers to cell (a,b) whereas x,y refers to pixel coordinates --- #

import pygame
import math as maths
import config
import preset
import time
import random


class Cell:
    def __init__(self, a, b, current_state, next_state, board, player):
        """a,b are the coordinates of the cell the instance represents."""
        self.CurrentState = current_state
        self.NextState = next_state
        self.BoardPos = (a, b)
        self.Coordinates = ((self.BoardPos[0] - board.Cushion) * board.Size + board.Edge / 2,
                            (self.BoardPos[1] - board.Cushion) * board.Size + board.Edge / 2)
        self.CurrentPlayer = 0
        self.NextPlayer = player
        if self.CurrentPlayer == 0:
            self.Colour = board.Colour["Alive"]
        else:
            self.Colour = board.Colour["Player" + str(player)]
    
    def kill(self):
        self.NextState = config.Dead
        self.NextPlayer = 0
    
    def birth(self, state, player):
        self.NextState = state
        self.NextPlayer = player
    
    def check_fate(self, board):
        """Checks whether the cell will be dead or alive at the end of this turn,
            and if so what type it will be"""
        total = [0, 0, 0, 0]
        player = [0, 0, 0, 0, 0]
        a, b = self.BoardPos
        al = a - 1  # a left (neighbour)
        ar = a + 1  # a right
        bu = b - 1  # b up
        bd = b + 1  # b down
        if board.Wrap and a == board.Width - 1:
            ar = 0
        if board.Wrap and b == board.Height - 1:
            bd = 0
        if self.CurrentState == config.Dead or self.CurrentState == config.Square or self.CurrentState == config.Hex:
            total[board.Cell[al][b].CurrentState] += 1
            player[board.Cell[al][b].CurrentPlayer] += 1
            
            total[board.Cell[a][bu].CurrentState] += 1
            player[board.Cell[a][bu].CurrentPlayer] += 1
            
            total[board.Cell[ar][b].CurrentState] += 1
            player[board.Cell[ar][b].CurrentPlayer] += 1
            
            total[board.Cell[a][bd].CurrentState] += 1
            player[board.Cell[a][bd].CurrentPlayer] += 1
        
        if self.CurrentState == config.Dead or self.CurrentState == config.Square:
            total[board.Cell[al][bu].CurrentState] += 1
            player[board.Cell[al][bu].CurrentPlayer] += 1
            
            total[board.Cell[ar][bu].CurrentState] += 1
            player[board.Cell[ar][bu].CurrentPlayer] += 1
            
            total[board.Cell[al][bd].CurrentState] += 1
            player[board.Cell[al][bd].CurrentPlayer] += 1
            
            total[board.Cell[ar][bd].CurrentState] += 1
            player[board.Cell[ar][bd].CurrentPlayer] += 1
        
        new_state = config.Dead
        new_player = 0
        birth = False
        if self.CurrentState == config.Dead:
            if total[config.Dead] == 5:  # if 5 dead cells; ie. if 3 alive cells
                birth = True
        elif self.CurrentState == config.Square:
            if total[config.Dead] in (5, 6):
                birth = True
        elif self.CurrentState == config.Hex:
            if total[config.Dead] in (2, 3):
                birth = True
        if birth:
            del total[0]
            new_state = total.index(max(total)) + 1
            del player[0]
            new_player = player.index(max(player)) + 1
        
        return new_state, new_player
    
    def draw(self, size, board):
        x, y = self.Coordinates
        x += board.Size // 2
        y += board.Size // 2
        pygame.draw.rect(Screen, board.Colour["Dead"], (x - size / 2, y - size / 2, size, size))
        if not self.CurrentState == config.Dead:
            if self.CurrentPlayer == 0:
                self.draw_shape(size, x, y, board.Colour["Alive"])
            else:
                self.draw_shape(size, x, y, board.Colour["Player" + str(self.CurrentPlayer)])
    
    def update(self):
        self.CurrentState = self.NextState
        self.CurrentPlayer = self.NextPlayer


class Square(Cell):
    def draw_shape(self, size, x, y, colour):
        """Draws a type of cell (Type) at the desired cell (a,b)"""
        pygame.draw.rect(Screen, colour, (x - size / 2, y - size / 2, size, size))


class Hex(Cell):
    def draw_shape(self, colour=None):
        """Draws a type of cell (Type) at the desired cell (a,b)"""
        if colour is None:
            colour = self.Colour
        x, y = self.Coordinates
        s = Board.Size - Board.Edge
        pygame.draw.rect(Screen, Sim.Colour["Dead"], (x, y, s, s))
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
    def __init__(self, state):
        self.Width = state.Width
        self.Height = state.Height
        self.Size = state.Size
        self.Wrap = state.Wrap
        self.Edge = state.Edge
        self.Generations = 0
        self.Cushion = state.Cushion
        self.Colour = state.Colour
        self.PreviewSize = state.PreviewSize
        self.Cell = [[Square(a, b, config.Square, config.Dead, self, 0) for b in range(
            self.Height + (2 * self.Cushion))] for a in range(self.Width + 2 * self.Cushion)]
        pygame.display.set_caption("Game of Life - Generation 0")
    
    def draw(self, preview=False):
        """draws the current board onto the screen then updates the display"""
        if preview:
            size = self.PreviewSize
        else:
            size = self.Size - self.Edge
        for a in range(self.Cushion, self.Cushion + self.Width):
            for b in range(self.Cushion, self.Cushion + self.Height):
                self.Cell[a][b].draw(size, self)
        pygame.display.update()
    
    def update(self):
        """Puts the NextState variables in the CurrentState variables"""
        for a in range(self.Width + 2 * self.Cushion):
            for b in range(self.Height + 2 * self.Cushion):
                self.Cell[a][b].update()
    
    def take_turn(self):
        """Changes the CurrentState variables & updates display caption"""
        pygame.display.set_caption("Game of Life - Generation " + str(self.Generations))
        if self.Wrap:
            cushion = 0
        else:
            cushion = 1
        for a in range(cushion, self.Width + (2 * self.Cushion) - cushion):  # Goes through all cells and kills
            for b in range(cushion, self.Height + (2 * self.Cushion) - cushion):  # those that will die and births
                fate, player = Board.Cell[a][b].check_fate(self)  # those that will be born.
                if fate == config.Dead:
                    self.Cell[a][b].kill()
                else:
                    if player == 0:
                        self.Cell[a][b].birth(fate, 0)
                    else:
                        self.Cell[a][b].birth(fate, player)
    
    def place_preset(self, preset_no, a, b):
        if self.Wrap:
            shape = preset.get(preset_no, a, b, self)[0]
        else:
            shape, a, b = preset.get(preset_no, a, b, self)
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
                    self.Cell[a + c][b + d].birth(shape[c][d], 0)
        self.update()
        self.draw()
    
    def reset(self, state):
        self.__init__(state)
        self.update()
        self.draw()
    
    def show_future(self, a, b, kill, player):
        temp_board = self
        if kill:
            temp_board.Cell[a][b].kill()
        else:
            temp_board.Cell[a][b].birth(config.Square, player)
        temp_board.draw()
        temp_board.take_turn()
        temp_board.update()
        temp_board.draw(preview=True)


class Player:
    def __init__(self, number, colour):
        self.Number = number
        self.Colour = colour
    
    def take_turn(self, board):
        can_end_turn = False
        board.draw()
        pygame.display.update()
        held_down = False
        while True:
            check_quit(pygame.event.get())
            x, y = pygame.mouse.get_pos()
            a, b = get_square(x, y, board)
            last_click = [0, 0, True]
            if 0 <= a < board.Width + board.Cushion and 0 <= b < board.Height + board.Cushion:
                if pygame.mouse.get_pressed()[0] and not held_down:
                    board.show_future(a, b, False, self.Number)
                    can_end_turn = True
                    last_click = [a, b, False]
                    held_down = True
                elif pygame.mouse.get_pressed()[2] and not held_down:
                    board.show_future(a, b, True, self.Number)
                    can_end_turn = True
                    last_click = [a, b, True]
                    held_down = True
                if not (pygame.mouse.get_pressed()[0] or pygame.mouse.get_pressed()[2]) and held_down:
                    held_down = False
            if can_end_turn and pygame.key.get_pressed()[pygame.K_SPACE]:
                return last_click


def check_user_input(sim, board):
    """Checks for user input and acts accordingly"""
    
    check_quit(pygame.event.get())
    x, y = pygame.mouse.get_pos()
    a, b = get_square(x, y, board)
    if sim.CanBePaused:
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            sim.Paused = not sim.Paused
            sim.CanBePaused = False
    else:
        if not pygame.key.get_pressed()[pygame.K_SPACE]:
            sim.CanBePaused = True
    for key in range(pygame.K_1, pygame.K_9):
        if pygame.key.get_pressed()[key]:
            board.place_preset(int(pygame.key.name(key)), a, b)
    if sim.CanChangeGPSLimit:
        if pygame.key.get_pressed()[pygame.K_f]:
            sim.GPSIsLimited = not sim.GPSIsLimited
            bottom_gps_log = maths.log(sim.BottomGPS, sim.TopGPS)
            draw_gps_slider(Sim.EndOfSlider - ((maths.log(sim.GPS, sim.TopGPS) - bottom_gps_log) *
                                               (Sim.EndOfSlider - Sim.StartOfSlider)) /
                            (1 - bottom_gps_log), sim.GPSIsLimited)
            sim.CanChangeGPSLimit = False
    else:
        if not pygame.key.get_pressed()[pygame.K_f]:
            sim.CanChangeGPSLimit = True
    if pygame.key.get_pressed()[pygame.K_RIGHT]:
        if sim.CanGoForward:
            sim.OneTurn = True
            sim.CanGoForward = False
    else:
        if not sim.CanGoForward:
            sim.CanGoForward = True
        sim.OneTurn = False
    if pygame.key.get_pressed()[pygame.K_RETURN]:
        board.reset(sim)
        sim.Paused = True
    if pygame.mouse.get_pressed()[0]:
        if board.Size * board.Width + board.Edge / 2 < x < board.Size * board.Width + Sim.ButtonSize + \
                        board.Edge / 2:  # within the button+GPS slider area
            if y < Sim.StartOfSlider:
                y = Sim.StartOfSlider
            elif y > Sim.EndOfSlider:
                y = Sim.EndOfSlider
                sim.GPSIsLimited = True
            draw_gps_slider(y, sim.GPSIsLimited)
            bottom_gps_log = maths.log(sim.BottomGPS, sim.TopGPS)
            sim.GPS = sim.TopGPS ** (((1 - bottom_gps_log) * (Sim.EndOfSlider - y) /
                                      (
                                          Sim.EndOfSlider - Sim.StartOfSlider)) + bottom_gps_log)
        elif 0 <= a < board.Width + board.Cushion and 0 <= b < board.Height + board.Cushion:
            board.Cell[a][b].birth(config.Square, 0)
            board.update()
            board.draw()
    if pygame.mouse.get_pressed()[2]:
        board.Cell[a][b].kill()
        board.update()
        board.draw()
    
    return sim


def draw_gps_slider(y, gps_limit):
    """Draws the slider with the y coordinate of the button click
       (How many GPS this corresponds to is not dealt with here.)"""
    if y < Sim.StartOfSlider:
        y = Sim.StartOfSlider
    elif y > Sim.EndOfSlider:
        y = Sim.EndOfSlider
    pygame.draw.rect(Screen, Sim.Colour["Background"],
                     ((Sim.ButtonStart, Sim.StartOfSlider - Sim.NotchLength),
                      (Sim.ButtonStart + Board.Edge + Sim.HighlightSize +
                       Sim.ButtonSize, Sim.EndOfSlider)))
    pygame.draw.line(Screen, Sim.Colour["Text"], (Sim.SliderY, Sim.StartOfSlider),
                     (Sim.SliderY,
                      Sim.EndOfSlider))
    for n in range(Sim.NoOfNotches):
        pygame.draw.line(Screen, Sim.Colour["Text"], (Sim.SliderY - Sim.NotchLength / 2,
                                                      Sim.StartOfSlider + n * Sim.SpaceBetweenNotches),
                         (Sim.SliderY + Sim.NotchLength / 2,
                          Sim.StartOfSlider + n * Sim.SpaceBetweenNotches))
    write(Screen, Sim.SliderY - (12 + Sim.NotchLength),
          (Sim.StartOfSlider + Sim.EndOfSlider) * 0.5,
          "Speed", Sim.Colour["Text"], 20,
          rotate=90, alignment=("left", "centre"))
    if gps_limit:
        colour = "Highlighter"
    else:
        colour = "Unselected"
    pygame.draw.polygon(Screen, Sim.Colour[colour], ((Sim.SliderY + Sim.NotchLength / 2, y),
                                                     (Sim.SliderY + Sim.NotchLength,
                                                      y - Sim.NotchLength / 2),
                                                     (Sim.SliderY + 2 * Sim.NotchLength,
                                                      y - Sim.NotchLength / 2),
                                                     (Sim.SliderY + 2 * Sim.NotchLength,
                                                      y + Sim.NotchLength / 2),
                                                     (Sim.SliderY + Sim.NotchLength,
                                                      y + Sim.NotchLength / 2)))
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


def get_menu_choice(menu, screen):
    pygame.display.set_mode((menu.Width, menu.Height))
    screen.fill(menu.Colour["Background"])
    size = menu.ButtonSize
    border = menu.ButtonBorder
    border_col = menu.Colour["Border"]
    text_col = menu.Colour["Text"]
    hover_col = menu.Colour["Hover"]
    
    centre = [screen.get_width() / 2, (screen.get_height() / 2) - size * 1.5]
    for a in range(2):
        pygame.draw.rect(screen, border_col, (centre[0] - 5 * size, centre[1] - size, size * 10, size * 2))
        pygame.draw.rect(screen, menu.Colour["Background"], (
            (centre[0] - 5 * size + border, centre[1] - size + border, size * 10 - border * 2, size * 2 - border * 2)))
        centre = [screen.get_width() / 2, (screen.get_height() / 2) + size * 1.5]
    
    write(screen, screen.get_width() / 2, size * 2, "Main Menu", text_col, size, alignment=("centre", "centre"))
    
    while True:
        check_quit(pygame.event.get())
        x, y = pygame.mouse.get_pos()
        top_colour = text_col
        bottom_colour = text_col
        if screen.get_width() / 2 - 5 * size < x < screen.get_width() / 2 + 5 * size:
            if (screen.get_height() / 2) - size * 1.5 - size < y < (screen.get_height() / 2) - size * 1.5 + size:
                if pygame.mouse.get_pressed()[0]:
                    return "Sim"
                top_colour = hover_col
            elif (screen.get_height() / 2) + size * 0.5 < y < (screen.get_height() / 2) + size * 2.5:
                if pygame.mouse.get_pressed()[0]:
                    return "Game"
                bottom_colour = hover_col
        
        write(screen, screen.get_width() / 2, (screen.get_height() / 2) - size * 1.5, "Simulator", top_colour,
              int(size / 1.5), alignment=("centre", "centre"))
        write(screen, screen.get_width() / 2, (screen.get_height() / 2) + size * 1.5, "2-Player Game", bottom_colour,
              int(size / 1.5), alignment=("centre", "centre"))
        
        pygame.display.update()


def check_quit(events):
    for event in events:
        if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
            pygame.quit()
            import sys
            sys.exit(0)


def get_square(x, y, board):
    return x // board.Size + board.Cushion, y // board.Size + board.Cushion


pygame.init()
pygame.event.set_allowed(None)
allowed_events = [pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN, pygame.KEYUP, pygame.QUIT]
for event in allowed_events:
    pygame.event.set_allowed(event)
Screen = pygame.display.set_mode((1, 1))

if get_menu_choice(config.Menu(), Screen) == "Sim":
    Sim = config.Sim()
    Board = Board(Sim)
    Screen = pygame.display.set_mode((Board.Size * Board.Width + Sim.ButtonSize, Board.Size * Board.Height))
    Screen.fill(Sim.Colour["Background"])
    draw_gps_slider(((maths.log(Sim.GPS, 10) + 1) / -3) * (Sim.EndOfSlider - Sim.StartOfSlider) + Sim.EndOfSlider,
                    Sim.GPSIsLimited)
    LastFrame = time.time()  # The time when the last frame update happened
    Board.update()
    for _ in range(int(Board.Width * Board.Height / 10)):
        Board.Cell[random.randint(Board.Cushion, Board.Cushion + Board.Width - 1)][
            random.randint(Board.Cushion, Board.Cushion + Board.Height - 1)].birth(random.randint(1, 2), 0)
    Board.update()
    Board.draw()
    
    while True:
        Sim = check_user_input(Sim, Board)
        Board.update()
        if (not Sim.Paused and (not Sim.GPSIsLimited or time.time() - LastFrame > 1 / Sim.GPS)) or (
                    Sim.Paused and Sim.OneTurn):
            if Sim.OneTurn:
                Sim.OneTurn = False
            Board.take_turn()
            Board.update()
            Board.Generations += 1
            Board.draw()
            LastFrame = time.time()

else:
    Game = config.Game()
    PlayerNo = 2
    Board = Board(Game)
    Board.update()
    for _ in range(int(Board.Width * Board.Height / 10)):
        p = random.randint(1, Game.NoOfPlayers)
        Board.Cell[random.randint(Board.Cushion, Board.Cushion + Board.Width - 1)][
            random.randint(Board.Cushion, Board.Cushion + Board.Height - 1)].birth(config.Square, p)
    Board.update()
    Board.draw()
    Screen = pygame.display.set_mode((Board.Size * Board.Width, Board.Size * Board.Height))
    Screen.fill(Game.Colour["Background"])
    Players = [Player(n, Game.Colour["Player" + str(n)]) for n in range(1, Game.NoOfPlayers + 1)]
    while True:
        if PlayerNo == Game.NoOfPlayers:
            PlayerNo = 1
        else:
            PlayerNo += 1
        Players[PlayerNo - 1].take_turn(Board)
