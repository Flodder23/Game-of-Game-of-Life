##General
Font = "Arial"  # "Arial" # The font used in the game

##MAIN MENU
M_ButtonHeight = 90  # 50 # The height of the buttons
M_ButtonWidth = 450  # 450 # The width of the buttons
M_ButtonBorder = 4  # 4 # The thickness of the borders on the buttons
M_ButtonGapSize = 40  # 40 # The gap between each button
M_SideGapSize = 250  # 250 # The size of the gap at each side (between the button and the edge of the screen)
M_TextSize = 30  # 30 # The size of the text in the buttons
M_TitleGapSize = 60  # 60 # The gap between the title and the top of the screen
M_TitleTextSize = 60  # 60 # The size of the text on the title
M_Colour = {"Border": (0, 0, 0),  # (0, 0, 0) # The colour of the borders on the buttons
            "Text": (0, 0, 0),  # (0, 0, 0) # The colour of all text
            "Hover": (0, 255, 100),  # (0, 255, 100) # The colour of the text when you hover over a button
            "Background": (120, 120, 120)}  # (120, 120, 120) # The colour of the background

##SIMULATOR MODE
S_Width = 40  # 50 # How many squares wide the board is
S_Height = 25  # 30 # Ditto but with height
S_Size = 22  # 20 # The size of the sides of each square (in pixels)
S_CellGap = 2  # 2 # The gap between each cell
S_Wrap = True  # True # Whether the board wraps around on itself
S_Cushion = 0  # 0 # How far the board extends beyond the visible amount
S_SetUpChances = (0, 0)  # (0, 0) # The chances of a cell being dead or alive when game is first loaded
S_SliderSize = 50  # 50 # The gap at the side of the board for the FPS slider
S_HighlightSize = 5  # 5 # The size of the slider pointer
S_NoOfNotches = 9  # 9 # The number of notches on the slider
S_NotchLength = S_SliderSize // 5  # S_SliderSize // 5 # The (horizontal) length of the notches
S_SpeedSize = 20  # 20 # The size of the writing of "Speed" next to the GPS slider
S_GPS = 10  # 10 # How many Generations Per Seconds at the start of the game; this can be changed in-game
S_TopGPS = 50  # 100 # The GPS at the top of the slider.
S_BottomGPS = 0.5  # 0.5 # The GPS at the bottom of slider.
S_Colour = {"Alive": (0, 0, 0),  # (0, 0, 0) # The colour of an alive cell
            "Dead": (255, 255, 255),  # (255, 255, 255) # The colour of a dead cell
            "Highlighter": (0, 255, 100),  # (0, 255, 100) # The colour of the slider pointer when active
            "Background": (120, 120, 120),  # (120, 120, 120) # The colour of the background
            "Text": (0, 0, 0),  # (0, 0, 0) # The colour of the text
            "Unselected": (160, 160, 160)}  # (160, 160, 160) # The colour of the slider pointer whe not active

##GAME MODE
G_Width = 24  # 50 # How many squares wide the board is - Must be divisible by 2
G_Height = 16  # 30 # Ditto but with height - Must be divisible by 2
G_Size = 35  # 20 # The size of the sides of each square (in pixels)
G_CellGap = 2  # 2 # The gap between each cell
G_NoOfPlayers = 2  # 2 # How many players there are - must be 2 or 4
G_PlayerNames = ["Joe", "Adam O'Neal", "Max", "Matej"]  # Player's names
G_PreviewSize = G_Size // 2  # G_Size // 2 # The size of the cells in preview mode
G_SetUpChances = (10, 2, 1, 1, 1)  # (10, 2, 1, 1, 1) # The likleyhood of each player's cells spawning in a cell (first one is chance of none spawning) at the start of a game
G_TextSize = 32  # 32 # The size of the text
G_RightColumnSize = 150  # 150 # The size of the column on the right
G_ButtonHeight = 50  # 50 # The height of the button
G_ButtonBorderSize = 3  # 3 # The size of the border of the button
G_WinMessageWidth = 500  # 500 # The width of the win message
G_WinMessageHeight = 300  # 300 # The height of the win message
G_Colour = {"Player1": (150, 205, 80),  # (150, 205, 80) # The colour of Player 1's cells
            "Player2": (0, 175, 240),  # (0, 175, 240) # The colour of Player 2's cells
            "Player3": (255, 210, 50),  # (255, 210, 50) # The colour of  Player 3's cells
            "Player4": (190, 120, 150),  # (190, 120, 150) # The colour of  Player 4's cells
            "Dead": (255, 255, 255),  # (255, 255, 255) # The colour of dead cells
            "Highlighter": (0, 255, 100),  # (0, 255, 100) # The colour of the button when your mouse is hovering over it
            "Unselectable": (200, 200, 200),  # (200, 200, 200) # The colour of a button that is not clickable
            "Background": (120, 120, 120),  # (120, 120, 120) # The colour of the background
            "Text": (0, 0, 0),  # (0, 0, 0) # The colour of the text
            "ButtonBorder": (0, 0, 0)}  # (0, 0, 0) # The colour of the border of the button

G_PartImmune = True  # True # Whether or not the game creates part immune cells
G_PartImmuneTime = 4  # 4 # The number of turns a cell has to be alive before it becomes part immune (doesn't die unless your opponent kills it)
G_PartImmuneKill = 2  # 2 # The number of turns it costs to kill a part immune cell
G_FullImmune = True  # True # Whether or not the game creates full immune cells
G_FullImmuneTime = 8  # 8 # The number of turns a cell has to be alive before it becomes fully immune (nothing can kill it except you) Must be be bigger than G_PartImmuneTime
G_FullImmuneKill = 4  # 4 # The number of turns it costs to kill a fully immune cell

G_IsTurnLimit = True  # True # Whether there is a limit on the amount of turns in a game
G_TurnLimit = 20  # 30 # The amount of turns each player can have before the game ends
G_IsGenLimit = False  # False # Whether there is a limit on the amount of generations in a game
G_GenLimit = 10  # 15 # THe amount of gens in total before the game ends
G_BoardAmountWin = True  # True # Whether the game ends when a player gets a certain amount of the board
G_BoardAmount = 0.25  # 0.3 # The amount of the board a player must get to win; an amount between 0 and 1
G_PlayerAmountWin = True  # True # Whether the game ends when a player has a certain amount of cells more than the opponent
G_PlayerAmount = 0.25  # 0.25 # If the number of cells a player has timesed by the number is bigger than the other's, the first player wins.

G_StartingTurns = 3  # 3 # The amount of turns each player starts with.
G_FairerTurns = True  # True # if this is True, instead of taking it in turns to go, the players will have 2 turns each in a row, with the first player starting with only one turn but gettting 2 after that.
G_TurnsPerRound = 2  # 2 # How many turns each player gets per round. if FairerTurns is True, the first player gets half this many on their first go.

##HELP SCREEN
H_SectionGapSize = 5  # 5 # The size of the gap between the 2 sections of text
H_TextSize = 20  # 20 # The size of the text
H_TitleSize = 30  # 30 # The size of titles
H_IndentSize = 40  # 40 # The size of indents
H_SliderWidth = 10  # 10 # The width of the slider
H_SliderGapSize = 5  # 5 # The gap between the slider and the edge/text
H_SliderLength = 100  # 100 # The length of the slider
H_Width = 1000 + H_SliderWidth + H_SliderGapSize  # 1000 # The width of the window
H_ScrollAmount = 50  # 50 # The amount scrolled with each turn of the moue wheel
H_Colour = {"Background": (120, 120, 120),  # (120, 120, 120) # The colour of the background
            "Text": (0, 0, 0),  # (0, 0, 0) # The colour of text
            "Slider": (0, 255, 100)}  # (0, 255, 100) # The colour of the slider
