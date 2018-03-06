# a,b refers to cell (a,b) whereas x,y refers to pixel coordinates

import pygame
import math as maths
import config
import preset
import random
import time
import copy


class Cell:
    def __init__(self, a, b, current_state, next_state, board, player):
        """a,b are the coordinates of the cell the instance represents with respect to the board."""
        self.CurrentState = current_state
        self.NextState = next_state
        self.CurrentPlayer = 0
        self.NextPlayer = player
        self.BoardPos = (a, b)
        self.Coordinates = ((self.BoardPos[0] - board.Cushion) * board.Size + board.CellGap / 2,
                            (self.BoardPos[1] - board.Cushion) * board.Size + board.CellGap / 2)
    
    def kill(self):
        self.NextState = config.Dead
        self.NextPlayer = 0
    
    def birth(self, state, player):
        self.NextState = state
        self.NextPlayer = player
    
    def check_fate(self, board):
        """Checks whether the cell will be dead or alive at the end of this turn,
            and if so what type it will be"""
        total = [0, 0, 0, 0]
        player = [0, 0, 0, 0, 0]
        a, b = self.BoardPos
        al = a - 1  # a left (neighbour)
        ar = a + 1  # a right
        bu = b - 1  # b up
        bd = b + 1  # b down
        if board.Wrap and a == board.Width - 1:
            ar = 0
        if board.Wrap and b == board.Height - 1:
            bd = 0
        total[board.Cell[al][b].CurrentState] += 1
        player[board.Cell[al][b].CurrentPlayer] += 1
        
        total[board.Cell[a][bu].CurrentState] += 1
        player[board.Cell[a][bu].CurrentPlayer] += 1
        
        total[board.Cell[ar][b].CurrentState] += 1
        player[board.Cell[ar][b].CurrentPlayer] += 1
        
        total[board.Cell[a][bd].CurrentState] += 1
        player[board.Cell[a][bd].CurrentPlayer] += 1
    
        total[board.Cell[al][bu].CurrentState] += 1
        player[board.Cell[al][bu].CurrentPlayer] += 1
        
        total[board.Cell[ar][bu].CurrentState] += 1
        player[board.Cell[ar][bu].CurrentPlayer] += 1
        
        total[board.Cell[al][bd].CurrentState] += 1
        player[board.Cell[al][bd].CurrentPlayer] += 1
        
        total[board.Cell[ar][bd].CurrentState] += 1
        player[board.Cell[ar][bd].CurrentPlayer] += 1
        
        new_state = self.CurrentState
        new_player = self.CurrentPlayer
        birth = False
        death = False
        if self.CurrentState == config.Dead:
            if total[config.Dead] == 5:  # if 5 dead cells; ie. if 3 alive cells
                birth = True
        elif self.CurrentState == config.Square:
            if total[config.Dead] not in (5, 6):
                death = True
        if birth:
            del total[0]
            new_state = total.index(max(total)) + 1
            del player[0]
            if sum(player) == 0:
                new_player = 0
            else:
                new_player = player.index(max(player)) + 1
        
        if death:
            new_state = config.Dead
            new_player = 0
        
        return new_state, new_player
    
    def draw(self, screen, size, board):
        x, y = self.Coordinates
        x += board.Size // 2
        y += board.Size // 2
        pygame.draw.rect(screen, board.Colour["Dead"], (x - size / 2, y - size / 2, size, size))
        if not self.CurrentState == config.Dead:
            if self.CurrentPlayer == 0:
                self.draw_shape(screen, size, x, y, board.Colour["Alive"])
            else:
                self.draw_shape(screen, size, x, y, board.Colour["Player" + str(self.CurrentPlayer)])
    
    def update(self):
        self.CurrentState = self.NextState
        self.CurrentPlayer = self.NextPlayer


class Square(Cell):
    def draw_shape(self, screen, size, x, y, colour):
        """Draws a type of cell (Type) at the desired cell (a,b)"""
        pygame.draw.rect(screen, colour, (x - size / 2, y - size / 2, size, size))


class Board:
    def __init__(self, state, players=False):
        self.Width = state.Width
        self.Height = state.Height
        self.Size = state.Size
        self.Wrap = state.Wrap
        self.CellGap = state.CellGap
        self.Generations = 0
        self.Cushion = state.Cushion
        self.Colour = state.Colour
        self.PreviewSize = state.PreviewSize
        self.Players = players
        self.Cell = [[Square(a, b, config.Square, config.Dead, self, 0) for b in range(
            self.Height + (2 * self.Cushion))] for a in range(self.Width + 2 * self.Cushion)]
        pygame.display.set_caption("Game of Life - Generation 0")
    
    def set_up(self, chances):
        if sum(chances) != 0:
            for a in range(self.Width):
                for b in range(self.Height):
                    n = random.randint(1, sum(chances))
                    for c in range(len(chances)):
                        if sum(chances[:c + 1]) > n:
                            if c != 0:
                                if not self.Players:
                                    c = 0
                                self.Cell[a][b].birth(config.Square, c)
                            break
    
    def draw(self, screen, preview=False, update_display=True):
        """draws the current board onto the screen then updates the display"""
        if preview:
            size = self.PreviewSize
        else:
            size = self.Size - self.CellGap
        for a in range(self.Cushion, self.Cushion + self.Width):
            for b in range(self.Cushion, self.Cushion + self.Height):
                self.Cell[a][b].draw(screen, size, self)
        if update_display:
            pygame.display.update()
    
    def update(self):
        """Puts the NextState variables in the CurrentState variables"""
        for a in range(self.Width + 2 * self.Cushion):
            for b in range(self.Height + 2 * self.Cushion):
                self.Cell[a][b].update()
    
    def take_turn(self):
        """Changes the NextState variables & updates display caption"""
        pygame.display.set_caption("Game of Life - Generation " + str(self.Generations))
        if self.Wrap:
            cushion = 0
        else:
            cushion = 1
        for a in range(cushion, self.Width + (2 * self.Cushion) - cushion):  # Goes through all cells and kills
            for b in range(cushion, self.Height + (2 * self.Cushion) - cushion):  # those that will die and births
                fate, player = self.Cell[a][b].check_fate(self)  # those that will be born.
                if self.Cell[a][b].CurrentState != fate or self.Cell[a][b].CurrentPlayer != player:
                    if fate == config.Dead:
                        self.Cell[a][b].kill()
                    else:
                        if player == 0:
                            self.Cell[a][b].birth(fate, 0)
                        else:
                            self.Cell[a][b].birth(fate, player)
    
    def place_preset(self, screen, preset_no, a, b):
        if self.Wrap:
            shape = preset.get(preset_no, a, b, self)[0]
        else:
            shape, a, b = preset.get(preset_no, a, b, self)
        for c in range(len(shape)):
            for d in range(len(shape[c])):
                if self.Wrap:
                    if a + c >= self.Width:
                        a -= self.Width
                    if b + d >= self.Height:
                        b -= self.Height
                if shape[c][d] == 0:
                    self.Cell[a + c][b + d].kill()
                else:
                    self.Cell[a + c][b + d].birth(shape[c][d], 0)
        self.update()
        self.draw(screen)
    
    def reset(self, state):
        self.__init__(state, players=self.Players)
        self.update()
    
    def show_future(self, screen, actions, player):
        temp_board = copy.deepcopy(self)
        for action in actions:
            if action[2]:
                temp_board.Cell[action[0]][action[1]].kill()
            else:
                temp_board.Cell[action[0]][action[1]].birth(config.Square, player)
            temp_board.Cell[action[0]][action[1]].update()
        temp_board.draw(screen, update_display=False)
        temp_board.take_turn()
        temp_board.update()
        temp_board.draw(screen, preview=True)


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
            if config.check_quit(events) and not held_down["esc"]:  # if ESC is pressed
                if len(turn) == 0:
                    return "Go Back"
                else:
                    del turn[-1]
                    turns_used[self.Number - 1] -= 1
                held_down["esc"] = True
            else:
                held_down["esc"] = False
            x, y = pygame.mouse.get_pos()
            a, b = config.get_square(x, y, board)
            if 0 <= a < board.Width + board.Cushion and 0 <= b < board.Height + board.Cushion:
                kill = None
                if len(turn) <= self.SpareTurns:
                    if pygame.mouse.get_pressed()[0] and not held_down["mouse0"] and board.Cell[a][b].CurrentState == config.Dead:
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
Sim = config.Sim()
SimBoard = Board(Sim)
SimBoard.set_up(Sim.SetUpChances)
Game = config.Game()
GameBoard = Board(Game, players=True)
GameBoard.set_up(Game.SetUpChances)
Help = config.Help()
Menu = config.Menu()
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
                            GameBoard.Cell[action[0]][action[1]].birth(config.Square, PlayerNo)
                        GameBoard.Cell[action[0]][action[1]].update()
                    GameBoard.take_turn()
                    GameBoard.update()
                    Screen.fill(Game.Colour["Background"])
                GameBoard.draw(Screen)
    
    elif MenuChoice == "Help":
        Help.display(Screen)
    MenuChoice = Menu.get_choice(Screen)
config.quit_game()
