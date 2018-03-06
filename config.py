Dead = 0
Square = 1
Font = "Arial"

import pygame
import math as maths


class Menu:
    """Change these values to change how the main self looks."""
    
    def __init__(self):
        self.ButtonHeight = 90
        self.ButtonWidth = 450
        self.ButtonBorder = 4
        self.ButtonGapSize = 40
        self.SideGapSize = 250
        self.TextSize = 30
        self.TitleGapSize = 60
        self.TitleTextSize = 60
        self.Buttons = ("Simulator", "2-Player Game", "Help", "Quit")
        self.Colour = {"Border": (255, 255, 255),
                       "Text": (255, 255, 255),
                       "Hover": (0, 255, 100),
                       "Background": (120, 120, 120)}
    
    def get_choice(self, screen):
        pygame.display.set_caption("Game of Life - Main Menu")
        pygame.display.set_mode((2 * self.SideGapSize + self.ButtonWidth,
                                 2 * self.TitleGapSize + len(self.Buttons) * (self.ButtonHeight + self.ButtonGapSize)))
        screen.fill(self.Colour["Background"])
        
        buttons = [[screen.get_width() / 2,
                    2 * self.TitleGapSize + a * (self.ButtonHeight + self.ButtonGapSize) + self.TitleTextSize,
                    self.Buttons[a], self.Colour["Text"]] for a in range(len(self.Buttons))]
        for a in range(len(self.Buttons)):
            pygame.draw.rect(screen, self.Colour["Border"],
                             (buttons[a][0] - self.ButtonWidth / 2, buttons[a][1] - self.ButtonHeight / 2, self.ButtonWidth,
                              self.ButtonHeight))
            pygame.draw.rect(screen, self.Colour["Background"], ((buttons[a][0] - self.ButtonWidth / 2 + self.ButtonBorder,
                                                                  buttons[a][1] - self.ButtonHeight / 2 + self.ButtonBorder,
                                                                  self.ButtonWidth - self.ButtonBorder * 2,
                                                                  self.ButtonHeight - self.ButtonBorder * 2)))
        
        write(screen, screen.get_width() / 2, self.TitleGapSize, "Main Menu", self.Colour["Text"], self.TitleTextSize,
              alignment=("centre", "centre"))
        
        while True:
            if check_quit(pygame.event.get()):
                quit_game()
            x, y = pygame.mouse.get_pos()
            for a in range(len(self.Buttons)):
                buttons[a][3] = self.Colour["Text"]
            if screen.get_width() / 2 - self.ButtonWidth / 2 < x < screen.get_width() / 2 + self.ButtonWidth / 2:
                for a in range(len(self.Buttons)):
                    if buttons[a][1] - self.ButtonHeight / 2 < y < buttons[a][1] + self.ButtonHeight / 2:
                        if pygame.mouse.get_pressed()[0]:
                            return buttons[a][2]
                        buttons[a][3] = self.Colour["Hover"]
            for a in range(len(self.Buttons)):
                write(screen, screen.get_width() / 2, buttons[a][1], buttons[a][2], buttons[a][3], self.TextSize,
                      alignment=("centre", "centre"))
            pygame.display.update()


class Sim:
    """Change these values to change how the game looks and behaves in Simulator mode."""
    
    def __init__(self):
        self.Width = 40  # C 50 How many squares wide the board is
        self.Height = 25  # C 30 Ditto but with height
        self.Size = 22  # C 20 The size of the sides of each square (in pixels)
        self.CellGap = 2  # C Size / 15 The gap between each cell
        self.Wrap = True  # Whether the board wraps around on itself
        self.Cushion = 0  # C 10 How far the board extends beyond the visible amount
        self.PreviewSize = 0
        self.SetUpChances = (0, 0)  # The chances of a cell being dead or alive when game is first loaded
        
        self.SliderSize = 50
        self.HighlightSize = 5
        self.NoOfNotches = 9
        self.NotchLength = self.SliderSize / 5
        self.StartOfSlider = 2 * self.NotchLength
        self.EndOfSlider = self.Height * self.Size - self.HighlightSize - self.NotchLength
        self.SpaceBetweenNotches = (self.EndOfSlider - self.StartOfSlider) / (self.NoOfNotches - 1)
        self.ButtonStart = self.Size * self.Width
        self.SliderY = self.Size * self.Width + self.CellGap / 2 + self.SliderSize / 2
        
        self.GPS = 10  # C 10 How many Generations Per Seconds
        self.TopGPS = 100  # The GPS at the top of the slider.
        self.BottomGPS = 0.5  # The GPS at the bottom of slider.
        self.GPSIsLimited = True
        self.Paused = True
        self.OneTurn = False
        self.CanBePaused = True
        self.CanChangeGPSLimit = True
        self.CanGoForward = True
        self.Colour = {"Alive": (0, 0, 0),
                       "Dead": (255, 255, 255),
                       "Highlighter": (0, 255, 100),
                       "Background": (120, 120, 120),
                       "Text": (180, 180, 180),
                       "Unselected": (160, 160, 160)}
    
    def check_user_input(self, screen, board):
        """Checks for user input and acts accordingly"""
        
        go_back = check_quit(pygame.event.get())
        x, y = pygame.mouse.get_pos()
        a, b = get_square(x, y, board)
        if self.CanBePaused:
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                self.Paused = not self.Paused
                self.CanBePaused = False
        else:
            if not pygame.key.get_pressed()[pygame.K_SPACE]:
                self.CanBePaused = True
        for key in range(pygame.K_1, pygame.K_9):
            if pygame.key.get_pressed()[key]:
                board.place_preset(screen, int(pygame.key.name(key)), a, b)
        if self.CanChangeGPSLimit:
            if pygame.key.get_pressed()[pygame.K_f]:
                self.GPSIsLimited = not self.GPSIsLimited
                bottom_gps_log = maths.log(self.BottomGPS, self.TopGPS)
                self.draw_gps_slider(self.EndOfSlider -
                                     ((maths.log(self.GPS, self.TopGPS) - bottom_gps_log) *
                                      (self.EndOfSlider - self.StartOfSlider)) / (1 - bottom_gps_log),
                                     self.GPSIsLimited, board)
                self.CanChangeGPSLimit = False
        else:
            if not pygame.key.get_pressed()[pygame.K_f]:
                self.CanChangeGPSLimit = True
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            if self.CanGoForward:
                self.OneTurn = True
                self.CanGoForward = False
        else:
            if not self.CanGoForward:
                self.CanGoForward = True
            self.OneTurn = False
        if pygame.key.get_pressed()[pygame.K_RETURN]:
            board.reset(self)
            board.draw(screen)
            self.Paused = True
        if pygame.mouse.get_pressed()[0]:
            if board.Size * board.Width + board.CellGap / 2 < x < (
                        board.Size * board.Width) + self.SliderSize + board.CellGap / 2:
                if y < self.StartOfSlider:
                    y = self.StartOfSlider
                elif y > self.EndOfSlider:
                    y = self.EndOfSlider
                    self.GPSIsLimited = True
                self.draw_gps_slider(y, self.GPSIsLimited, board)
                bottom_gps_log = maths.log(self.BottomGPS, self.TopGPS)
                self.GPS = self.TopGPS ** (((1 - bottom_gps_log) * (self.EndOfSlider - y)
                                            / (self.EndOfSlider - self.StartOfSlider)) + bottom_gps_log)
            elif 0 <= a < board.Width + board.Cushion and 0 <= b < board.Height + board.Cushion:
                board.Cell[a][b].birth(Square, 0)
                board.update()
                board.draw(screen)
        if pygame.mouse.get_pressed()[2]:
            board.Cell[a][b].kill()
            board.update()
            board.draw(screen)
        
        return go_back
    
    def draw_gps_slider(self, screen, y, gps_limit, board):
        """Draws the slider with the y coordinate of the button click
           (How many GPS this corresponds to is not dealt with here.)"""
        if y < self.StartOfSlider:
            y = self.StartOfSlider
        elif y > self.EndOfSlider:
            y = self.EndOfSlider
        pygame.draw.rect(screen, self.Colour["Background"],
                         ((self.ButtonStart, self.StartOfSlider - self.NotchLength),
                          (self.ButtonStart + board.CellGap + self.HighlightSize + self.SliderSize, self.EndOfSlider)))
        pygame.draw.line(screen, self.Colour["Text"], (self.SliderY, self.StartOfSlider), (self.SliderY, self.EndOfSlider))
        for n in range(self.NoOfNotches):
            pygame.draw.line(screen, self.Colour["Text"], (self.SliderY - self.NotchLength / 2,
                                                           self.StartOfSlider + n * self.SpaceBetweenNotches),
                             (self.SliderY + self.NotchLength / 2, self.StartOfSlider + n * self.SpaceBetweenNotches))
        write(screen, self.SliderY - (12 + self.NotchLength), (self.StartOfSlider + self.EndOfSlider) * 0.5, "Speed",
              self.Colour["Text"], 20, rotate=90, alignment=("left", "centre"))
        if gps_limit:
            colour = "Highlighter"
        else:
            colour = "Unselected"
        pygame.draw.polygon(screen, self.Colour[colour], ((self.SliderY + self.NotchLength / 2, y),
                                                          (self.SliderY + self.NotchLength, y - self.NotchLength / 2),
                                                          (self.SliderY + 2 * self.NotchLength, y - self.NotchLength / 2),
                                                          (self.SliderY + 2 * self.NotchLength, y + self.NotchLength / 2),
                                                          (self.SliderY + self.NotchLength, y + self.NotchLength / 2)))
        pygame.display.update()


class Game:
    """Change these values to change how the game looks and behaves in 2-Player mode."""
    
    def __init__(self):
        self.Width = 25  # C 50 How many squares wide the board is
        self.Height = 15  # C 30 Ditto but with height
        self.Size = 35  # C 20 The size of the sides of each square (in pixels)
        self.CellGap = 2  # C 2 The gap between each cell
        self.Wrap = True
        self.Cushion = 0
        self.NoOfPlayers = 2  # C How many players there are - 2 or 4
        self.PlayerNames = ["Joe", "Adam O'Neal", "Max", "Matej"][:self.NoOfPlayers]  # C Player's names
        self.PreviewSize = self.Size // 2
        self.SetUpChances = (10, 1, 1, 1, 1)[:self.NoOfPlayers + 1]
        self.TextSize = 32
        self.RightColumnSize = 150
        self.ButtonHeight = 50
        self.ButtonBorderSize = 3
        self.Colour = {"Alive": (0, 0, 0),
                       "Player1": (0, 255, 100),
                       "Player2": (0, 100, 255),
                       "Player3": (255, 100, 0),
                       "Player4": (0, 0, 0),
                       "Dead": (255, 255, 255),
                       "Highlighter": (0, 255, 100),
                       "Background": (120, 120, 120),
                       "Text": (255, 255, 255),
                       "ButtonBorder": (255, 255, 255)}
    
    def draw_right_column(self, screen, players, active_player_no, on_button, button_text, turns_used, births, deaths):
        pygame.draw.rect(screen, self.Colour["Background"], (screen.get_width() - self.RightColumnSize, 0,
                                                             self.RightColumnSize, screen.get_height()))
        
        write(screen, screen.get_width() - self.RightColumnSize / 2, self.ButtonBorderSize,
              self.PlayerNames[active_player_no - 1] + "'s turn", self.Colour["Player" + str(active_player_no)],
              self.TextSize, max_len=self.RightColumnSize, alignment=("centre", "top"))
        pygame.draw.rect(screen, self.Colour["ButtonBorder"],
                         (screen.get_width() - self.RightColumnSize + self.ButtonBorderSize,
                          screen.get_height() - self.ButtonBorderSize - self.ButtonHeight,
                          self.RightColumnSize - 2 * self.ButtonBorderSize, self.ButtonHeight))
        pygame.draw.rect(screen, self.Colour["Background"],
                         (screen.get_width() - self.RightColumnSize + 2 * self.ButtonBorderSize,
                          screen.get_height() - self.ButtonHeight,
                          self.RightColumnSize - 4 * self.ButtonBorderSize,
                          self.ButtonHeight - 2 * self.ButtonBorderSize))
        if on_button:
            button_colour = self.Colour["Highlighter"]
        else:
            button_colour = self.Colour["Text"]
        write(screen, screen.get_width() - self.RightColumnSize / 2,
              screen.get_height() - self.ButtonBorderSize - self.ButtonHeight / 2, button_text,
              button_colour, self.TextSize, max_len=self.RightColumnSize, alignment=("centre", "centre"))
        bottom = [screen.get_width() - self.RightColumnSize + self.ButtonBorderSize,
                  screen.get_height() - 2 * self.ButtonBorderSize - self.ButtonHeight]
        extra_space = 0
        for n in [self.NoOfPlayers - a - 1 for a in range(self.NoOfPlayers)]:
            col = players[n].Colour
            extra_space += 4 * self.ButtonBorderSize
            extra_space += write(screen, bottom[0], bottom[1] - extra_space,
                                 "Spare Turns: " + str(players[n].SpareTurns - turns_used[n]),
                                 col, int(self.TextSize / 1.5), alignment=("left", "bottom")) + 2 * self.ButtonBorderSize
            extra_space += write(screen, bottom[0], bottom[1] - extra_space, "Cells: " + str(players[n].NoOfCells - deaths[n]
                                                                                             + births[n]), col,
                                 int(self.TextSize / 1.5), alignment=("left", "bottom")) + 2 * self.ButtonBorderSize
            extra_space += write(screen, bottom[0], bottom[1] - extra_space, self.PlayerNames[n], col,
                                 int(self.TextSize / 1.2),
                                 max_len=self.RightColumnSize - 2 * self.ButtonBorderSize, alignment=("left", "bottom"))


class Help:
    def __init__(self):
        self.SectionGapSize = 5
        self.TextSize = 20
        self.TitleSize = int(self.TextSize * 1.5)
        self.IndentSize = 40
        self.SliderWidth = 10
        self.SliderGapSize = 5
        self.SliderLength = 100
        self.Width = 1000 + self.SliderWidth + self.SliderGapSize
        self.Height = 600  # gets changed in the program depending on space taken up by help
        self.ScrollAmount = 50
        self.Colour = {"Background": (120, 120, 120),
                       "Text": (255, 255, 255),
                       "Slider": (0, 255, 100)}
        self.Surfaces = self.get_surfaces()
    
    def draw(self, screen, help_surface, slider_centre, slider_range):
        pygame.draw.rect(screen, self.Colour["Background"],
                         (int((self.Width - self.SliderWidth - self.SectionGapSize) / 2) - self.SliderGapSize, 0,
                          self.Width, self.Height))
        pygame.draw.rect(screen, self.Colour["Slider"],
                         (self.Width - self.SliderGapSize - self.SliderWidth, slider_centre - self.SliderLength / 2,
                          self.SliderWidth, self.SliderLength))
        help_rect = help_surface.get_rect()
        text_range = (self.SectionGapSize, help_surface.get_height() - self.Height + 2 * self.SectionGapSize)
        top_y = text_range[0] - (text_range[1] - text_range[0]) * (slider_centre - slider_range[0]) / (slider_range[1]
                                                                                                       - slider_range[0])
        help_rect.topleft = (int((self.Width - self.SliderWidth) / 2) + self.SliderGapSize, top_y)
        screen.blit(help_surface, help_rect)
        pygame.display.update()
    
    def display(self, screen):
        pygame.display.set_caption("Game of Life - Help")
        pygame.display.set_mode((self.Width, self.Surfaces[0].get_height()))
        screen.fill(self.Colour["Background"])
        self.Height = screen.get_height()
        slider_range = (
            self.SliderGapSize + self.SliderLength / 2, self.Height - self.SliderGapSize - self.SliderLength / 2)
        slider_centre = slider_range[0]
        help_rect = self.Surfaces[0].get_rect()
        help_rect.topleft = (self.SectionGapSize, self.SectionGapSize)
        screen.blit(self.Surfaces[0], help_rect)
        self.draw(screen, self.Surfaces[1], slider_centre, slider_range)
        slider_last_turn = False
        while True:
            events = pygame.event.get()
            if check_quit(events):
                break
            x, y = pygame.mouse.get_pos()
            if pygame.mouse.get_pressed()[0]:
                if not slider_last_turn and self.Width - 2 * self.SliderGapSize - self.SliderWidth < x < self.Width \
                        and slider_centre - self.SliderLength / 2 < y < slider_centre + self.SliderLength / 2:
                    slider_last_turn = True
                    mouse_start = y
                if slider_last_turn:
                    if slider_centre + y - mouse_start < slider_range[0]:
                        y = slider_range[0] + mouse_start - slider_centre
                    elif slider_centre + y - mouse_start > slider_range[1]:
                        y = slider_range[1] + mouse_start - slider_centre
                    self.draw(screen, self.Surfaces[1], slider_centre + y - mouse_start, slider_range)
            elif x > (self.Width - self.SliderWidth - self.SectionGapSize) / 2 - self.SliderGapSize:
                for e in events:
                    if e.type == pygame.MOUSEBUTTONDOWN:
                        draw = False
                        if e.button == 4:
                            slider_centre -= self.ScrollAmount
                            slider_centre = max(slider_centre, slider_range[0])
                            draw = True
                        if e.button == 5:
                            slider_centre += self.ScrollAmount
                            slider_centre = min(slider_centre, slider_range[1])
                            draw = True
                        if draw:
                            self.draw(screen, self.Surfaces[1], slider_centre, slider_range)
            
            else:
                if slider_last_turn:
                    slider_last_turn = False
                    slider_centre += y - mouse_start
            pygame.display.update()
    
    def get_surfaces(self):
        text = open("help.txt").read().split("++")
        for section in range(len(text)):
            text[section] = text[section].split("\n")
        help_surfaces = []
        
        for section in text:
            extra = 0
            for _ in range(2):
                help_surface = pygame.Surface(((self.Width - self.SliderWidth)
                                               // 2 - self.SectionGapSize - self.SliderGapSize, extra))
                help_surface.fill(self.Colour["Background"])
                extra = 0
                for line in section:
                    if line.startswith("**"):
                        size = self.TitleSize
                        line = line[2:]
                    else:
                        size = self.TextSize
                    indent = 0
                    while line.startswith("--"):
                        indent += 1
                        line = line[2:]
                    extra += write(help_surface, indent * self.IndentSize, extra, line, self.Colour["Text"], size,
                                   max_len=help_surface.get_width() - indent * self.IndentSize) + self.SectionGapSize
            help_surfaces.append(help_surface)
        return help_surfaces


def write(screen, x, y, text, colour, size, max_len=None, gap=0, font=Font, rotate=0, alignment=("left", "top")):
    """Puts text onto the screen at point x,y. the alignment variable, if used, can take first value \"left\",
    \"centre\" or \"right\" and the second value can be \"top\", \"centre\" or \"bottom\".
    note that these values relate to x and y respectively whatever the rotation, which is in degrees.
    max_len allows you to wrap a line if it becomes too long; the text will be restricted to being that many pixels long,
    and if it gets longer a new line will be started"""
    font_obj = pygame.font.SysFont(font, size)
    if text == "":
        line = 1
        extra_space = size
    else:
        line = 0
        extra_space = 0
    while len(text.split()) > 0:
        line += 1
        msg_surface_obj = pygame.transform.rotate(font_obj.render(text, False, colour), rotate)
        used = len(text.split())
        while max_len is not None and msg_surface_obj.get_width() > max_len:
            used -= 1
            msg_surface_obj = pygame.transform.rotate(font_obj.render(" ".join(text.split()[:used]), False, colour), rotate)
        msg_rect_obj = msg_surface_obj.get_rect()
        a, b = msg_surface_obj.get_size()
        if alignment[0] == "centre":
            new_x = x - a / 2
        elif alignment[0] == "right":
            new_x = x - a
        else:
            new_x = x
        if alignment[1] == "centre":
            new_y = y - b / 2
        elif alignment[1] == "bottom":
            new_y = y - b
        else:
            new_y = y
        msg_rect_obj.topleft = (new_x, new_y)
        screen.blit(msg_surface_obj, msg_rect_obj)
        y += msg_surface_obj.get_height() + gap
        extra_space += msg_surface_obj.get_height() + gap
        text = " ".join(text.split()[used:])
    return extra_space


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
