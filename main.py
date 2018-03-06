# a,b refers to cell (a,b) whereas x,y refers to pixel coordinates

import pygame
import math as maths
import set_up
import time
import board


class Player:
    def __init__(self, number, colour):
        self.Number = number
        self.Colour = colour
        self.NoOfCells = 0
        self.SpareTurns = 0
    
    def take_turn(self, screen, board, state, players):
        turn_chosen = False
        board.draw(screen)
        turn = []
        pygame.display.update()
        held_down = {"mouse0": True, "mouse2": False, "esc": False, "space": False, "f": False}
        show_future = True
        button_text = "Skip Turn"
        turns_used = [0 for _ in range(state.NoOfPlayers)]
        while not turn_chosen:
            events = pygame.event.get()
            if set_up.check_quit(events) and not held_down["esc"]:  # if ESC is pressed
                if len(turn) == 0:
                    return "Go Back"
                else:
                    del turn[-1]
                    turns_used[self.Number - 1] -= 1
                held_down["esc"] = True
            else:
                held_down["esc"] = False
            x, y = pygame.mouse.get_pos()
            a, b = set_up.get_square(x, y, board)
            if 0 <= a < board.Width + board.Cushion and 0 <= b < board.Height + board.Cushion:
                kill = None
                if len(turn) <= self.SpareTurns:
                    if pygame.mouse.get_pressed()[0] and not held_down["mouse0"] and board.Cell[a][b].CurrentState == set_up.Dead:
                        kill = False
                    elif pygame.mouse.get_pressed()[2] and not held_down["mouse2"] and board.Cell[a][b].CurrentState != 0:
                        kill = True
                if kill is not None:
                    turn.append([a, b, kill])
                    button_text = "Take Turn"
                    turns_used[self.Number - 1] += 1
            if pygame.key.get_pressed()[pygame.K_SPACE] and not held_down["space"]:
                turn_chosen = True
            if pygame.key.get_pressed()[pygame.K_f] and not held_down["f"]:
                show_future = not show_future
            on_button = False
            if 2 * state.ButtonBorderSize < screen.get_width() - x < state.RightColumnSize - 2 * state.ButtonBorderSize:
                if 0 < screen.get_height() - y - 2 * state.ButtonBorderSize < state.ButtonHeight:
                    if pygame.mouse.get_pressed()[0] and not held_down["mouse0"]:
                        turn_chosen = True
                    on_button = True

            births = [0 for _ in range(state.NoOfPlayers)]
            deaths = [0 for _ in range(state.NoOfPlayers)]
            for action in turn:
                if action[2]:
                    deaths[board.Cell[action[0]][action[1]].CurrentPlayer - 1] += 1
                else:
                    births[self.Number - 1] += 1
            
            state.draw_right_column(screen, players, self.Number, on_button, button_text, turns_used, births, deaths)
            board.show_future(screen, turn, self.Number)
            held_down["mouse0"] = pygame.mouse.get_pressed()[0]
            held_down["mouse2"] = pygame.mouse.get_pressed()[2]
            held_down["space"] = pygame.key.get_pressed()[pygame.K_SPACE]
            held_down["f"] = pygame.key.get_pressed()[pygame.K_f]
            pygame.display.update()
        return turn


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
GameBoard.set_up(Game.SetUpChances)
Help = set_up.Help()
Menu = set_up.Menu()
MenuChoice = Menu.get_choice(Screen)

while MenuChoice in ("Simulator", "2-Player Game", "Help"):
    if MenuChoice == "Simulator":
        Screen = pygame.display.set_mode((SimBoard.Size * SimBoard.Width + Sim.SliderSize,
                                          SimBoard.Size * SimBoard.Height))
        Screen.fill(Sim.Colour["Background"])
        Sim.draw_gps_slider(Screen, ((maths.log(Sim.GPS, 10) + 1) / -3)
                            * (Sim.EndOfSlider - Sim.StartOfSlider) + Sim.EndOfSlider, Sim.GPSIsLimited, SimBoard)
        LastFrame = time.time()  # The time when the last frame update happened
        SimBoard.update()
        SimBoard.draw(Screen)
        
        while True:
            if Sim.check_user_input(Screen, SimBoard):
                break
            SimBoard.update()
            if (not Sim.Paused and (not Sim.GPSIsLimited or time.time() - LastFrame > 1 / Sim.GPS)) \
                    or (Sim.Paused and Sim.OneTurn):
                if Sim.OneTurn:
                    Sim.OneTurn = False
                SimBoard.take_turn()
                SimBoard.update()
                SimBoard.Generations += 1
                SimBoard.draw(Screen)
                LastFrame = time.time()
    
    elif MenuChoice == "2-Player Game":
        PlayerNo = Game.NoOfPlayers
        GameBoard.update()
        GameBoard.draw(Screen)
        Screen = pygame.display.set_mode(
            (GameBoard.Size * GameBoard.Width + Game.RightColumnSize, GameBoard.Size * GameBoard.Height))
        Screen.fill(Game.Colour["Background"])
        Players = [Player(n, Game.Colour["Player" + str(n)]) for n in range(1, Game.NoOfPlayers + 1)]
        while True:
            PlayerScores = [0 for _ in range(Game.NoOfPlayers + 1)]
            for a in range(Game.Width):
                for b in range(Game.Height):
                    PlayerScores[GameBoard.Cell[a][b].CurrentPlayer] += 1
            for p in range(Game.NoOfPlayers):
                Players[p].NoOfCells = PlayerScores[p + 1]
            if PlayerNo == Game.NoOfPlayers:
                PlayerNo = 1
            else:
                PlayerNo += 1
            Players[PlayerNo - 1].SpareTurns += 1
            Turn = Players[PlayerNo - 1].take_turn(Screen, GameBoard, Game, Players)
            if Turn == "Go Back":
                break
            else:
                if len(Turn) == 0:
                    Players[PlayerNo - 1].SpareTurns += 1
                else:
                    for action in Turn:
                        if action[2]:
                            GameBoard.Cell[action[0]][action[1]].kill()
                        else:
                            GameBoard.Cell[action[0]][action[1]].birth(set_up.Square, PlayerNo)
                        GameBoard.Cell[action[0]][action[1]].update()
                    GameBoard.take_turn()
                    GameBoard.update()
                    Screen.fill(Game.Colour["Background"])
                GameBoard.draw(Screen)
    
    elif MenuChoice == "Help":
        Help.display(Screen)
    MenuChoice = Menu.get_choice(Screen)
set_up.quit_game()
