import pygame

Dead = 0
Square = 1
Width = 50  # C 50 How many squares wide the board is
Height = 30  # C 30 Ditto but with height
Size = 20  # C 20 The size of the sides of each square (in pixels)
Edge = Size // 7  # C Size / 15 The gap between each cell


class GameState:
    def __init__(self):
        self.GPS = 10  # C 10 How many Generations Per Seconds
        self.TopGPS = 100  # The GPS at the top of the slider.
        self.BottomGPS = 0.5  # The GPS at the bottom of slider.
        self.GPSLimit = True
        self.Paused = True
        self.OneTurn = False
        self.Colour = {"Alive": (0, 0, 0),
                       "Player1": (0, 255, 100),
                       "Player2": (0, 100, 255),
                       "Player3": (100, 255, 0),
                       "Player4": (100, 0, 255),
                       "Dead": (255, 255, 255),
                       "Highlighter": (0, 255, 100),
                       "Background": (120, 120, 120),
                       "Text": (180, 180, 180),
                       "Unselected": (160, 160, 160)}


class Widgets:
    def __init__(self):
        self.NoOfButtons = 0
        self.ButtonSize = 50
        self.HighlightSize = 5
        self.NoOfNotches = 9
        self.NotchLength = self.ButtonSize/5
        self.StartOfSlider = self.NoOfButtons * self.ButtonSize + self.HighlightSize + 2 * self.NotchLength
        self.EndOfSlider = Height * Size - self.HighlightSize - self.NotchLength
        self.SpaceBetweenNotches = (self.EndOfSlider-self.StartOfSlider) / (self.NoOfNotches-1)
        self.ButtonStart = Size * Width
        self.SliderY = Size * Width + Edge / 2 + self.ButtonSize / 2


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
