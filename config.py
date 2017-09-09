import pygame
import math as maths
import time

Width = 50  # C 50 How many squares wide the board is
Height = 30  # C 30 Ditto but with height
Size = 20  # C 20 The size of the sides of each square (in pixels)
Wrap = False #Board wraps around on itself
if Wrap:
    Cushion = 0
else:
    Cushion = 10  # C 10 How far the board extends beyond the visible amount
Edge = maths.ceil(Size / 7)  # C Size/15 The gap between each cell
Background = (120, 120, 120)  # C (120,120,120) The colour of the background
Dead = 0
Square = 1
NoOfButtons = 0
ButtonSize = 55  # The space at the end currently with the FPS slider but will also include Buttons (hence the name)
Border = 5  # C 5 How much bigger (each side) the highlighter to show selected input on Buttons.
FPS = 10  # C 5 How many FPS
MaxFPS = 100  # C
MinFPS = 0.5  # C
Notches = 9  # C 9 How many notches on the FPS slider
NotchLength = ButtonSize / 5  # C ButtonSize/5 The length of each notch on the FPS slider
StartOfSlider = NoOfButtons * ButtonSize + Border + 2 * NotchLength  # Top of FPS slider (y coordinate)
EndOfSlider = Height * Size - Border - NotchLength  # Bottom of FPS slider (y coordinate)


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
