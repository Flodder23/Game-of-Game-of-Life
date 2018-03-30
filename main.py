# a,b refers to cell (a,b) whereas x,y refers to pixel coordinates

import pygame
import set_up
import board

pygame.init()
Screen = pygame.display.set_mode((500, 500))
pygame.display.set_icon(pygame.image.load("Icon.png"))
pygame.event.set_allowed(None)  # PyGame wil now not check for any inputs
allowed_events = (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN, pygame.KEYUP, pygame.QUIT)
for event in allowed_events:         # PyGame will now only check inputs for things used in the program, increasing speed
    pygame.event.set_allowed(event)  # and efficiency.
Sim = set_up.Sim()  #Setting up
SimBoard = board.SimBoard(Sim)
SimBoard.set_up(Sim.SetUpChances)
Game = set_up.Game()
GameBoard = board.GameBoard(Game, players=True)
GameBoard.set_up(Game.SetUpChances, rotational_symmetry=Game.NoOfPlayers)
Help = set_up.Help()
Menu = set_up.Menu()
MenuChoice = Menu.get_choice(Screen)

while MenuChoice in (Menu.Buttons[:3]):
    if MenuChoice == Menu.Buttons[0]:
        Sim.run(Screen, SimBoard)
    elif MenuChoice == Menu.Buttons[1]:
        if Game.run(Screen, GameBoard):
            Game = set_up.Game()
            GameBoard = board.Board(Game, players=True)
            GameBoard.set_up(Game.SetUpChances, rotational_symmetry=Game.NoOfPlayers)
    elif MenuChoice == Menu.Buttons[2]:
        Help.display(Screen)
    MenuChoice = Menu.get_choice(Screen)
set_up.quit_game()
