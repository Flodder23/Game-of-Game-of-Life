# ---  a,b refers to cell (a,b) whereas x,y refers to pixel coordinates --- #

import pygame
import math as maths
import config
import preset
import time
import random
import copy


class Cell:
    def __init__(self, a, b, current_state, next_state, board, player):
        """a,b are the coordinates of the cell the instance represents."""
        self.CurrentState = current_state
        self.NextState = next_state
        self.CurrentPlayer = 0
        self.NextPlayer = player
        self.BoardPos = (a, b)
        self.Coordinates = ((self.BoardPos[0] - board.Cushion) * board.Size + board.CellGap / 2,
                            (self.BoardPos[1] - board.Cushion) * board.Size + board.CellGap / 2)
    
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
        
        new_state = self.CurrentState
        new_player = self.CurrentPlayer
        birth = False
        death = False
        if self.CurrentState == config.Dead:
            if total[config.Dead] == 5:  # if 5 dead cells; ie. if 3 alive cells
                birth = True
        elif self.CurrentState == config.Square:
            if total[config.Dead] not in (5, 6):
                death = True
        elif self.CurrentState == config.Hex:
            if total[config.Dead] not in (2, 3):
                death = True
        if birth:
            del total[0]
            new_state = total.index(max(total)) + 1
            del player[0]
            if sum(player) == 0:
                new_player = 0
            else:
                new_player = player.index(max(player)) + 1
        
        if death:
            new_state = config.Dead
            new_player = 0
        
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
        s = Board.Size - Board.CellGap
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
        self.CellGap = state.CellGap
        self.Generations = 0
        self.Cushion = state.Cushion
        self.Colour = state.Colour
        self.PreviewSize = state.PreviewSize
        self.Cell = [[Square(a, b, config.Square, config.Dead, self, 0) for b in range(
            self.Height + (2 * self.Cushion))] for a in range(self.Width + 2 * self.Cushion)]
        pygame.display.set_caption("Game of Life - Generation 0")
    
    def set_up(self, chances):
        if sum(chances) != 0:
            for a in range(self.Width):
                for b in range(self.Height):
                    n = random.randint(1, sum(chances))
                    for c in range(len(chances)):
                        if sum(chances[:c + 1]) > n:
                            if c != 0:
                                self.Cell[a][b].birth(config.Square, c)
                            break
    
    def draw(self, preview=False):
        """draws the current board onto the screen then updates the display"""
        if preview:
            size = self.PreviewSize
        else:
            size = self.Size - self.CellGap
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
        """Changes the NextState variables & updates display caption"""
        pygame.display.set_caption("Game of Life - Generation " + str(self.Generations))
        if self.Wrap:
            cushion = 0
        else:
            cushion = 1
        for a in range(cushion, self.Width + (2 * self.Cushion) - cushion):  # Goes through all cells and kills
            for b in range(cushion, self.Height + (2 * self.Cushion) - cushion):  # those that will die and births
                fate, player = self.Cell[a][b].check_fate(self)  # those that will be born.
                if self.Cell[a][b].CurrentState != fate or self.Cell[a][b].CurrentPlayer != player:
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
        temp_board = copy.deepcopy(self)
        if kill:
            temp_board.Cell[a][b].kill()
        else:
            temp_board.Cell[a][b].birth(config.Square, player)
        temp_board.Cell[a][b].update()
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
        last_click = [0, 0, True]
        pygame.display.update()
        held_down = False
        while True:
            if check_quit(pygame.event.get()):
                return "Go Back"
            x, y = pygame.mouse.get_pos()
            a, b = get_square(x, y, board)
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
    
    go_back = check_quit(pygame.event.get())
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
                            (1 - bottom_gps_log), sim.GPSIsLimited, board)
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
        if board.Size * board.Width + board.CellGap / 2 < x < board.Size * board.Width + Sim.ButtonSize + \
                        board.CellGap / 2:  # within the button+GPS slider area
            if y < Sim.StartOfSlider:
                y = Sim.StartOfSlider
            elif y > Sim.EndOfSlider:
                y = Sim.EndOfSlider
                sim.GPSIsLimited = True
            draw_gps_slider(y, sim.GPSIsLimited, board)
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
    
    return sim, go_back


def draw_gps_slider(y, gps_limit, board):
    """Draws the slider with the y coordinate of the button click
       (How many GPS this corresponds to is not dealt with here.)"""
    if y < Sim.StartOfSlider:
        y = Sim.StartOfSlider
    elif y > Sim.EndOfSlider:
        y = Sim.EndOfSlider
    pygame.draw.rect(Screen, Sim.Colour["Background"],
                     ((Sim.ButtonStart, Sim.StartOfSlider - Sim.NotchLength),
                      (Sim.ButtonStart + board.CellGap + Sim.HighlightSize +
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


def write(screen, x, y, text, colour, size, max_len=None, gap=5, font=config.Font, rotate=0, alignment=("left", "top")):
    """Puts text onto the screen at point x,y. the alignment variable, if used, can take first value \"left\",
    \"centre\" or \"right\" and the second value can be \"top\", \"centre\" or \"bottom\".
    note that these values relate to x and y respectively whatever the rotation, which is in degrees."""
    font_obj = pygame.font.SysFont(font, size)
    if text == "":
        line = 1
    else:
        line = 0
    while len(text.split()) > 0:
        line += 1
        msg_surface_obj = pygame.transform.rotate(font_obj.render(text, False, colour), rotate)
        used = len(text.split())
        while max_len is not None and msg_surface_obj.get_width() > max_len:
            used -= 1
            msg_surface_obj = pygame.transform.rotate(font_obj.render(" ".join(text.split()[:used]), False, colour),
                                                      rotate)
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
        y += size + gap
        text = " ".join(text.split()[used:])
    return line


def get_menu_choice(menu, screen):
    pygame.display.set_caption("Game of Life - Main Menu")
    pygame.display.set_mode((2 * menu.SideGapSize + menu.ButtonWidth,
                             2 * menu.TitleGapSize + len(menu.Buttons) * (menu.ButtonHeight + menu.ButtonGapSize)))
    screen.fill(menu.Colour["Background"])
    
    buttons = [[screen.get_width() / 2,
                2 * menu.TitleGapSize + a * (menu.ButtonHeight + menu.ButtonGapSize) + menu.TitleTextSize,
                menu.Buttons[a], menu.Colour["Text"]] for a in range(len(menu.Buttons))]
    for a in range(len(menu.Buttons)):
        pygame.draw.rect(screen, menu.Colour["Border"], (
        buttons[a][0] - menu.ButtonWidth / 2, buttons[a][1] - menu.ButtonHeight / 2, menu.ButtonWidth,
        menu.ButtonHeight))
        pygame.draw.rect(screen, menu.Colour["Background"], (
            (buttons[a][0] - menu.ButtonWidth / 2 + menu.ButtonBorder,
             buttons[a][1] - menu.ButtonHeight / 2 + menu.ButtonBorder, menu.ButtonWidth - menu.ButtonBorder * 2,
             menu.ButtonHeight - menu.ButtonBorder * 2)))
    
    write(screen, screen.get_width() / 2, menu.TitleGapSize, "Main Menu", menu.Colour["Text"], menu.TitleTextSize,
          alignment=("centre", "centre"))
    
    while True:
        if check_quit(pygame.event.get()):
            quit_game()
        x, y = pygame.mouse.get_pos()
        for a in range(len(menu.Buttons)):
            buttons[a][3] = menu.Colour["Text"]
        if screen.get_width() / 2 - menu.ButtonWidth / 2 < x < screen.get_width() / 2 + menu.ButtonWidth / 2:
            for a in range(len(menu.Buttons)):
                if buttons[a][1] - menu.ButtonHeight / 2 < y < buttons[a][1] + menu.ButtonHeight / 2:
                    if pygame.mouse.get_pressed()[0]:
                        return buttons[a][2]
                    buttons[a][3] = menu.Colour["Hover"]
        for a in range(len(menu.Buttons)):
            write(screen, screen.get_width() / 2, buttons[a][1], buttons[a][2],
                  buttons[a][3], menu.TextSize, alignment=("centre", "centre"))
        
        pygame.display.update()


def check_quit(events):
    for event in events:
        if event.type == pygame.QUIT:
            quit_game()
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            return True
    return False


def quit_game():
    pygame.quit()
    import sys
    sys.exit(0)


def get_square(x, y, board):
    a = min(x // board.Size, board.Width) + board.Cushion
    b = min(y // board.Size, board.Height) + board.Cushion
    return a, b


def draw_help(screen, help_surface, state, slider_centre, slider_range):
    pygame.draw.rect(screen, state.Colour["Background"],
                     (int((state.Width - state.SliderWidth - state.SectionGapSize) / 2) - state.SliderGapSize, 0,
                      state.Width,
                      state.Height))
    pygame.draw.rect(screen, state.Colour["Slider"], (
        state.Width - state.SliderGapSize - state.SliderWidth,
        slider_centre - state.SliderLength / 2,
        state.SliderWidth, state.SliderLength))
    help_rect = help_surface.get_rect()
    text_range = (state.SectionGapSize, help_surface.get_height() - state.Height + 2 * state.SectionGapSize)
    top_y = text_range[0] - (text_range[1] - text_range[0]) * (slider_centre - slider_range[0]) / (
        slider_range[1] - slider_range[0])
    help_rect.topleft = (int((state.Width - state.SliderWidth) / 2) + state.SliderGapSize, top_y)
    screen.blit(help_surface, help_rect)
    pygame.display.update()


def display_help(state, screen, help_surfaces):
    pygame.display.set_caption("Game of Life - Help")
    pygame.display.set_mode((state.Width, help_surfaces[0].get_height()))
    screen.fill(state.Colour["Background"])
    state.Height = screen.get_height()
    slider_range = (
    state.SliderGapSize + state.SliderLength / 2, state.Height - state.SliderGapSize - state.SliderLength / 2)
    slider_centre = slider_range[0]
    help_rect = help_surfaces[0].get_rect()
    help_rect.topleft = (state.SectionGapSize, state.SectionGapSize)
    screen.blit(help_surfaces[0], help_rect)
    draw_help(screen, help_surfaces[1], state, slider_centre, slider_range)
    slider_last_turn = False
    while True:
        events = pygame.event.get()
        if check_quit(events):
            break
        x, y = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            if not slider_last_turn and state.Width - 2 * state.SliderGapSize - state.SliderWidth < x < state.Width and slider_centre - state.SliderLength / 2 < y < slider_centre + state.SliderLength / 2:
                slider_last_turn = True
                mouse_start = y
            if slider_last_turn:
                if slider_centre + y - mouse_start < slider_range[0]:
                    y = slider_range[0] + mouse_start - slider_centre
                elif slider_centre + y - mouse_start > slider_range[1]:
                    y = slider_range[1] + mouse_start - slider_centre
                draw_help(screen, help_surfaces[1], state, slider_centre + y - mouse_start, slider_range)
        elif x > (state.Width - state.SliderWidth - state.SectionGapSize) / 2 - state.SliderGapSize:
            for e in events:
                if e.type == pygame.MOUSEBUTTONDOWN:
                    draw = False
                    if e.button == 4:
                        slider_centre -= state.ScrollAmount
                        slider_centre = max(slider_centre, slider_range[0])
                        draw = True
                    if e.button == 5:
                        slider_centre += state.ScrollAmount
                        slider_centre = min(slider_centre, slider_range[1])
                        draw = True
                    if draw:
                        draw_help(screen, help_surfaces[1], state, slider_centre, slider_range)
        
        else:
            if slider_last_turn:
                slider_last_turn = False
                slider_centre += y - mouse_start
        pygame.display.update()


def get_help_surfaces(state):
    text = open("help.txt").read().split("++")
    for section in range(len(text)):
        text[section] = text[section].split("\n")
    help_surfaces = []
    
    for section in text:
        xtra_line = 0
        bold = 0
        for _ in range(2):
            help_surface = pygame.Surface(
                (int((state.Width - state.SliderWidth) / 2) - state.SectionGapSize - state.SliderGapSize,
                 xtra_line * (state.TextSize + state.SectionGapSize) + bold * (state.TitleSize - state.TextSize)))
            help_surface.fill(state.Colour["Background"])
            xtra_line = 0
            bold = 0
            for line in section:
                if line.startswith("**"):
                    size = state.TitleSize
                    line = line[2:]
                    bold += 1
                else:
                    size = state.TextSize
                indent = 0
                while line.startswith("--"):
                    indent += 1
                    line = line[2:]
                xtra_line += write(help_surface, indent * state.IndentSize,
                                   xtra_line * (state.SectionGapSize + state.TextSize), line, state.Colour["Text"],
                                   size,
                                   max_len=help_surface.get_width() - indent * state.IndentSize,
                                   gap=state.SectionGapSize)
        help_surfaces.append(help_surface)
    return help_surfaces


pygame.init()
pygame.event.set_allowed(None)
allowed_events = (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN, pygame.KEYUP, pygame.QUIT)
for event in allowed_events:
    pygame.event.set_allowed(event)
Screen = pygame.display.set_mode((1, 1))
pygame.display.set_icon(pygame.image.load("Icon.png"))
Sim = config.Sim()
SimBoard = Board(Sim)
SimBoard.set_up(Sim.SetUpChances)
Game = config.Game()
GameBoard = Board(Game)
GameBoard.set_up(Game.SetUpChances)
Help = config.Help()
HelpSurfaces = get_help_surfaces(Help)
MenuChoice = get_menu_choice(config.Menu(), Screen)

while MenuChoice in ("Simulator", "2-Player Game", "Help"):
    if MenuChoice == "Simulator":
        Screen = pygame.display.set_mode(
            (SimBoard.Size * SimBoard.Width + Sim.ButtonSize, SimBoard.Size * SimBoard.Height))
        Screen.fill(Sim.Colour["Background"])
        draw_gps_slider(((maths.log(Sim.GPS, 10) + 1) / -3) * (Sim.EndOfSlider - Sim.StartOfSlider) + Sim.EndOfSlider,
                        Sim.GPSIsLimited, SimBoard)
        LastFrame = time.time()  # The time when the last frame update happened
        SimBoard.update()
        SimBoard.update()
        SimBoard.draw()
        
        while True:
            Sim, GoBack = check_user_input(Sim, SimBoard)
            if GoBack:
                break
            SimBoard.update()
            if (not Sim.Paused and (not Sim.GPSIsLimited or time.time() - LastFrame > 1 / Sim.GPS)) or (
                        Sim.Paused and Sim.OneTurn):
                if Sim.OneTurn:
                    Sim.OneTurn = False
                SimBoard.take_turn()
                SimBoard.update()
                SimBoard.Generations += 1
                SimBoard.draw()
                LastFrame = time.time()
    
    elif MenuChoice == "2-Player Game":
        PlayerNo = 2
        GameBoard.update()
        GameBoard.update()
        GameBoard.draw()
        Screen = pygame.display.set_mode((GameBoard.Size * GameBoard.Width, GameBoard.Size * GameBoard.Height))
        Screen.fill(Game.Colour["Background"])
        Players = [Player(n, Game.Colour["Player" + str(n)]) for n in range(1, Game.NoOfPlayers + 1)]
        while True:
            if PlayerNo == Game.NoOfPlayers:
                PlayerNo = 1
            else:
                PlayerNo += 1
            Turn = Players[PlayerNo - 1].take_turn(GameBoard)
            if Turn == "Go Back":
                break
            if Turn[2]:
                GameBoard.Cell[Turn[0]][Turn[1]].kill()
            else:
                GameBoard.Cell[Turn[0]][Turn[1]].birth(config.Square, PlayerNo)
            GameBoard.Cell[Turn[0]][Turn[1]].update()
            GameBoard.take_turn()
            GameBoard.update()
            GameBoard.draw()
    
    elif MenuChoice == "Help":
        display_help(Help, Screen, HelpSurfaces)
    MenuChoice = get_menu_choice(config.Menu(), Screen)
quit_game()
