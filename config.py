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
M_Colour = {"Border": (255, 255, 255),  # (255, 255, 255) # The colour of the borders on the buttons
            "Text": (255, 255, 255),  # (255, 255, 255) # The colour of all text
            "Hover": (0, 255, 100),  # (0, 255, 100) # The colour of the text when you hover over a button
            "Background": (120, 120, 120)}  # (120, 120, 120) # The colour of the background

##SIMULATOR MODE
S_Width = 40  # 50 # How many squares wide the board is
S_Height = 25  # 30 # Ditto but with height
S_Size = 22  # 20 # The size of the sides of each square (in pixels)
S_CellGap = 2  # 2 # The gap between each cell
S_Wrap = True  # True # Whether the board wraps around on itself
S_Cushion = 0  # 10 # How far the board extends beyond the visible amount
S_SetUpChances = (0, 0)  # (0, 0) # The chances of a cell being dead or alive when game is first loaded

S_SliderSize = 50  # 50 # The gap at the side of the board for the FPS slider
S_HighlightSize = 5  # 5 # The size of the slider pointer
S_NoOfNotches = 9  # 9 # The number of notches on the slider
S_NotchLength = S_SliderSize / 5 # S_SliderSize / 5 # The (horizontal) length of the notches

S_GPS = 10  # 10 # How many Generations Per Seconds at the start of the game; this can be changed in-game
S_TopGPS = 100  # 100 # The GPS at the top of the slider.
S_BottomGPS = 0.5  # 0.5 # The GPS at the bottom of slider.
S_Colour = {"Alive": (0, 0, 0), # (0, 0, 0) # The colour of an alive cell
            "Dead": (255, 255, 255), # (255, 255, 255) # The colour of a dead cell
            "Highlighter": (0, 255, 100),  # (0, 255, 100) # The colour of
            "Background": (120, 120, 120),  # (120, 120, 120) # The colour of the background
            "Text": (180, 180, 180)#,   (180, 180, 180) # The colour of the text
            #"Unselected": (160, 160, 160)}  # (160, 160, 160) # The colour of
            }

##GAME MODE
G_Width = 25  # 50 # How many squares wide the board is
G_Height = 15  # 30 # Ditto but with height
G_Size = 35  # 20 # The size of the sides of each square (in pixels)
G_CellGap = 2  # 2 # The gap between each cell
G_NoOfPlayers = 2  # 2 # How many players there are - 2 or 4
G_PlayerNames = ["Joe", "Adam O'Neal", "Max", "Matej"]  # Player's names
G_PreviewSize = G_Size // 2  # G_Size // 2 # The size of the cells in preview mode
G_SetUpChances = (10, 1, 1, 1, 1)  # (10, 1, 1, 1, 1) # The liklehood of each player's cells spawning in a cell (first one is chance of none spawning) at the start of a game
G_TextSize = 32 # 32 # The size of the text
G_RightColumnSize = 150  # 150 # The size of the column on the right
G_ButtonHeight = 50  # 50 # The height of the button
G_ButtonBorderSize = 3  # 3 # The size of the border of the button
G_Colour = {#"Alive": (0, 0, 0),  # The colour of
            "Player1": (0, 255, 100),  # The colour of Player 1's cells
            "Player2": (0, 100, 255),  # The colour of Player 2's cells
            "Player3": (255, 100, 0),  # The colour of  Player 3's cells
            "Player4": (0, 0, 0),  # The colour of  Player 4's cells
            "Dead": (255, 255, 255),  # The colour of dead cells
            "Highlighter": (0, 255, 100),  # The colour of the button when your mouse is hovering over it
            "Background": (120, 120, 120),  # The colour of the background
            "Text": (255, 255, 255),  # The colour of the text
            "ButtonBorder": (255, 255, 255)}  # The colour of the border of the button

##HELP SCREEN
H_SectionGapSize = 5  # The size of the gap between the 2 sections of text
H_TextSize = 20  # The size of the text
H_TitleSize = int(H_TextSize * 1.5)  # The size of titles
H_IndentSize = 40  # The size of indents
H_SliderWidth = 10  # The width of the slider
H_SliderGapSize = 5  # The gap between the slider and the edge/text
H_SliderLength = 100  # The length of the slider
H_Width = 1000 + H_SliderWidth + H_SliderGapSize  # The width of the window
H_ScrollAmount = 50  # The amount scrolled with each turn of the moue wheel
H_Colour = {"Background": (120, 120, 120),  # The colour of the background
            "Text": (255, 255, 255),  # The colour of text
            "Slider": (0, 255, 100)}  # The colour of the slider
