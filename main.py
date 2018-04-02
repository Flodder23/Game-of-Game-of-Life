# a,b refers to cell (a,b) whereas x,y refers to pixel coordinates

import pygame
import set_up
import board

pygame.init()
Screen = pygame.display.set_mode((500, 500))
pygame.display.set_icon(pygame.image.load("Icon.png"))
pygame.event.set_allowed(None)  # PyGame will now not check for any inputs
allowed_events = (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN,
                  pygame.KEYDOWN, pygame.KEYUP, pygame.QUIT)
for event in allowed_events:         # PyGame will now only check inputs for things used in the
    pygame.event.set_allowed(event)  # program, increasing speed and efficiency.
Sim = set_up.Sim()  # Setting up
SimBoard = board.SimBoard(Sim)
SimBoard.set_up(Sim.SetUpChances)
Game = set_up.Game()
GameBoard = board.GameBoard(Game, players=True)
GameBoard.set_up(Game.SetUpChances, rotational_symmetry=Game.NoOfPlayers)
Help = set_up.Help()
Menu = set_up.Menu()
MenuChoice = Menu.get_choice(Screen)

while MenuChoice in (Menu.Buttons[:3]):  # If a button that wasn't the Quit button was pressed
    if MenuChoice == Menu.Buttons[0]:  # If the Simulator button was pressed
        Sim.run(Screen, SimBoard)
    elif MenuChoice == Menu.Buttons[1]:  # If the Game button was pressed
        if Game.run(Screen, GameBoard):  # Runs the game; value returned is boolean value which is
            Game = set_up.Game()         # True if the game has ended and if it did the game is
            GameBoard = board.GameBoard(Game, players=True)  # reset so you can play again
            GameBoard.set_up(Game.SetUpChances, rotational_symmetry=Game.NoOfPlayers)
    elif MenuChoice == Menu.Buttons[2]:  # If the Help Button was pressed
        Help.display(Screen)
    MenuChoice = Menu.get_choice(Screen)  # Another choice is made when menu is returned to
set_up.quit_game()
