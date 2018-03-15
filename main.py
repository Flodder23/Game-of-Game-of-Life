# a,b refers to cell (a,b) whereas x,y refers to pixel coordinates

import pygame
import set_up
import board

pygame.init()
pygame.event.set_allowed(None)
Screen = pygame.display.set_mode((500, 500))
pygame.display.set_icon(pygame.image.load("Icon.png"))
allowed_events = (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN, pygame.KEYUP, pygame.QUIT)
for event in allowed_events:
    pygame.event.set_allowed(event)
Sim = set_up.Sim()
SimBoard = board.Board(Sim)
SimBoard.set_up(Sim.SetUpChances)
Game = set_up.Game()
GameBoard = board.Board(Game, players=True)
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
