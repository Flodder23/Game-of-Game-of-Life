Dead = 0
Square = 1
Hex = 2
Font = "boring"


class Menu:
    """Change these values to change how the main menu looks."""
    
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


class Sim:
    """Change these values to change how the game looks and behaves in Simulator mode."""
    
    def __init__(self):
        self.Width = 40  # C 50 How many squares wide the board is
        self.Height = 25  # C 30 Ditto but with height
        self.Size = 22  # C 20 The size of the sides of each square (in pixels)
        self.CellGap = 3  # C Size / 15 The gap between each cell
        self.Wrap = True  # Whether the board wraps around on itself
        self.Cushion = 0  # C 10 How far the board extends beyond the visible amount
        self.PreviewSize = 0
        self.SetUpChances = (10, 1)  # The chances of a cell being dead or alive when game is first loaded
        
        self.NoOfButtons = 0
        self.ButtonSize = 50
        self.HighlightSize = 5
        self.NoOfNotches = 9
        self.NotchLength = self.ButtonSize / 5
        self.StartOfSlider = 2 * self.NotchLength
        self.EndOfSlider = self.Height * self.Size - self.HighlightSize - self.NotchLength
        self.SpaceBetweenNotches = (self.EndOfSlider - self.StartOfSlider) / (self.NoOfNotches - 1)
        self.ButtonStart = self.Size * self.Width
        self.SliderY = self.Size * self.Width + self.CellGap / 2 + self.ButtonSize / 2
        
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
    """Change these values to change how the game looks and behaves in 2-Player mode."""
    
    def __init__(self):
        self.Width = 25  # C 50 How many squares wide the board is
        self.Height = 15  # C 30 Ditto but with height
        self.Size = 35  # C 20 The size of the sides of each square (in pixels)
        self.CellGap = 2  # C 2 The gap between each cell
        self.Wrap = True
        self.Cushion = 0
        self.NoOfPlayers = 2  # C How many players there are - 2 or 4
        self.PlayerNames = ["Joe", "Adam"][:self.NoOfPlayers]  # C Player's names
        self.PreviewSize = self.Size // 2
        self.SetUpChances = (10, 1, 1, 1, 1)[:self.NoOfPlayers+1]
        self.Colour = {"Alive": (0, 0, 0),
                       "Player1": (0, 255, 100),
                       "Player2": (0, 100, 255),
                       "Player3": (100, 255, 0),
                       "Player4": (100, 0, 255),
                       "Dead": (255, 255, 255),
                       "Highlighter": (0, 255, 100),
                       "Background": (120, 120, 120),
                       "Text": (180, 180, 180), }


class Help:
    def __init__(self):
        self.SectionGapSize = 5
        self.TextSize = 16
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
