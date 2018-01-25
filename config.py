Dead = 0
Square = 1
Hex = 2


class Menu:
    """Change these values to change how the main menu looks."""

    def __init__(self):
        self.ButtonSize = 50
        self.ButtonBorder = 4
        self.BorderColour = (255, 255, 255)
        self.TextColour = (255, 255, 255)
        self.HoverColour = (0, 255, 100)
        self.Width = 1000
        self.Height = 600
        self.Colour = {"Border": (255, 255, 255),
                       "Text": (255, 255, 255),
                       "Hover": (0, 255, 100),
                       "Background": (120, 120, 120)}


class Sim:
    """Change these values to change how the game looks in Simulator mode."""

    def __init__(self):
        self.Width = 50  # C 50 How many squares wide the board is
        self.Height = 30  # C 30 Ditto but with height
        self.Size = 20  # C 20 The size of the sides of each square (in pixels)
        self.Edge = self.Size // 7  # C Size / 15 The gap between each cell
        self.Wrap = True  # Whether the board wraps around on itself
        if self.Wrap:
            self.Cushion = 0
        else:
            self.Cushion = 10  # C 10 How far the board extends beyond the visible amount

        self.NoOfButtons = 0
        self.ButtonSize = 50
        self.HighlightSize = 5
        self.NoOfNotches = 9
        self.NotchLength = self.ButtonSize / 5
        self.StartOfSlider = 2 * self.NotchLength
        self.EndOfSlider = self.Height * self.Size - self.HighlightSize - self.NotchLength
        self.SpaceBetweenNotches = (self.EndOfSlider - self.StartOfSlider) / (self.NoOfNotches - 1)
        self.ButtonStart = self.Size * self.Width
        self.SliderY = self.Size * self.Width + self.Edge / 2 + self.ButtonSize / 2

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


class Game:
    """Change these values to change how the game looks in 2-Player mode."""

    def __init__(self):
        self.Width = 50  # C 50 How many squares wide the board is
        self.Height = 30  # C 30 Ditto but with height
        self.Size = 20  # C 20 The size of the sides of each square (in pixels)
        self.Edge = self.Size // 7  # C Size / 15 The gap between each cell
        self.Colour = {"Player1": (0, 255, 100),
                       "Player2": (0, 100, 255),
                       "Player3": (100, 255, 0),
                       "Player4": (100, 0, 255),
                       "Dead": (255, 255, 255),
                       "Highlighter": (0, 255, 100),
                       "Background": (120, 120, 120),
                       "Text": (180, 180, 180), }
