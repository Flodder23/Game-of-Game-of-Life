import pygame
import math as maths
import time

Width = 50  # C 50 How many squares wide the board is
Height = 30  # C 30 Ditto but with height
Size = 20  # C 20 The size of the sides of each square (in pixels)
Cushion = 5  # C 10 How far the board extends beyond the visible amount
Edge = maths.ceil(Size / 7)  # C Size/15 The gap between each cell
Background = (120, 120, 120)  # C (120,120,120) The colour of the background
Dead = 0
Square = 1
NoOfButtons=0
ButtonSize = 55  # The space at the end currently with the FPs slider but will also include Buttons (hence the name)
Border = 5  # C 5 How much bigger (each side) the highlighter to show selected input on Buttons.
FPS = 10  # C 5 How many FPS
Notches = 9  # C 9 How many notches on the FPS slider
NotchLength = ButtonSize / 5  # C ButtonSize/5 The length of each notch on the FPS slider
StartOfSlider = NoOfButtons * ButtonSize + Border + 2 * NotchLength  # Top of FPS slider (y coordinate)
EndOfSlider = Height * Size - Border - NotchLength  # Bottom of FPS slider (y coordinate)


def write(screen, x, y, text, colour, size):
    fontObj = pygame.font.Font("freesansbold.ttf", size)
    msgSurfaceObj = fontObj.render(text, False, colour)
    msgRectObj = msgSurfaceObj.get_rect()
    msgRectObj.topleft = (x, y)
    screen.blit(msgSurfaceObj, msgRectObj)
