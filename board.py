import set_up
import pygame
import random
import preset
import copy


class Cell:
    def __init__(self, a, b, current_state, next_state,
                 board, player, part_immune=False, alive_for=0):
        """a,b are the coordinates of the cell the instance represents with respect to the board."""
        self.CurrentState = current_state
        self.NextState = next_state
        self.CurrentPlayer = 0
        self.NextPlayer = player
        self.BoardPos = (a, b)
        self.AliveFor = alive_for
        self.PartImmune = part_immune
        self.FullImmune = False
        self.Coordinates = ((self.BoardPos[0] - board.Cushion) * board.Size
                            + (board.CellGap + board.Size) // 2,
                            (self.BoardPos[1] - board.Cushion) * board.Size
                            + (board.CellGap + board.Size) // 2)
    
    def kill(self):
        """Resets all the relevant attributes for when a cell will die next turn;
        doesn't change the NextState attribute"""
        self.NextState = set_up.Dead
        self.NextPlayer = 0
        self.AliveFor = 0
        self.PartImmune = False
        self.FullImmune = False
    
    def birth(self, state, player):
        """Resets all the relevant attributes for when a cell will be born next turn;
        doesn't change the NextState attribute"""
        self.NextState = state
        self.NextPlayer = player
        self.FullImmune = False
        self.PartImmune = False
    
    def draw(self, screen, size, board, colour=None):
        """Draws the cell"""
        x, y = self.Coordinates
        if colour is None:
            pygame.draw.rect(screen, board.Colour["Dead"],
                             (x - size // 2, y - size // 2, size, size))  # draws the dead cell
            if not self.CurrentState == set_up.Dead:  # which is needed for immune/part immune cells
                if self.PartImmune:  # as they don't cover all of the space, so need a background
                    pygame.draw.circle(screen, board.Colour["Player" + str(self.CurrentPlayer)],
                                       (x, y), size // 2)
                    if not self.FullImmune:
                        pygame.draw.rect(screen, board.Colour["Player" + str(self.CurrentPlayer)],
                                         (x - size // 2, y - size // 2, size, size // 2))
                elif self.CurrentPlayer == 0:
                    pygame.draw.rect(screen, board.Colour["Alive"], (x - size // 2, y - size // 2,
                                                                     size, size))
                else:
                    pygame.draw.rect(screen, board.Colour["Player" + str(self.CurrentPlayer)],
                                     (x - size // 2, y - size // 2, size, size))
        else:
            pygame.draw.rect(screen, colour, (x - size // 2, y - size // 2, size, size))
    
    def update(self, board=None, immunity=False):
        """Puts the NextState attributes into the CurrentState attribute."""
        self.CurrentState = self.NextState
        self.CurrentPlayer = self.NextPlayer
        if immunity and not self.FullImmune and not self.CurrentState == set_up.Dead:
            if self.AliveFor >= board.FullImmuneTime:
                self.FullImmune = True
            elif self.AliveFor >= board.PartImmuneTime:
                self.PartImmune = True
            self.AliveFor += 1

    def check_fate(self, board, players=False):
        """Checks whether the cell will be dead or alive at the end of this turn,
            and if so what type it will be"""
        if self.PartImmune:
            return self.CurrentState, self.CurrentPlayer
        player = [0, 0, 0, 0, 0]
        a, b = self.BoardPos
        al = a - 1  # a left (neighbour)
        ar = a + 1  # a right
        bu = b - 1  # b up
        bd = b + 1  # b down
        if board.Wrap and a == board.Width + 2 * board.Cushion - 1:
            ar = 0
        if board.Wrap and b == board.Height + 2 * board.Cushion - 1:
            bd = 0
        alive = 0
        for c in (a, ar, al):  # checks all cells < 1 away in each direction
            for d in (b, bu, bd):
                if not (c == a and d == b) and board.Cell[c][d].CurrentState == set_up.Square:
                    alive += 1  # if isn't checking itself and the cell its checking is alive
        new_state = self.CurrentState
        new_player = self.CurrentPlayer
        birth = False
        death = False  # assuming no changes
        if self.CurrentState == set_up.Dead and alive == 3:
            birth = True
            new_state = set_up.Square
        elif self.CurrentState == set_up.Square and alive not in (2, 3):
            death = True
            new_state = set_up.Dead
        
        if players:
            if death:
                new_player = 0
            if birth:
                for c in (a, ar, al):
                    for d in (b, bu, bd):
                        if not (c == a and d == b):  # if not checking itself
                            player[board.Cell[c][d].CurrentPlayer] += 1
                del player[0]  # this represents the dead cells, which will have a majority and
                new_player = player.index(max(player)) + 1  # therefore mess up the choice if left
    
        return new_state, new_player


class Board:
    def __init__(self, state, players=False):
        self.Width = state.Width
        self.Height = state.Height
        self.Size = state.Size
        self.Wrap = state.Wrap
        self.CellGap = state.CellGap
        self.Generations = 0
        self.Cushion = state.Cushion
        self.get_square = lambda x, y: (min(x // self.Size, self.Width) + self.Cushion,
                                        min(y // self.Size, self.Height) + self.Cushion)
        self.Colour = state.Colour
        self.PreviewSize = state.PreviewSize
        self.Players = players
        if self.Players:
            self.PartImmuneTime = state.PartImmuneTime
            self.FullImmuneTime = state.FullImmuneTime
        self.Cell = [[Cell(a, b, set_up.Square, set_up.Dead, self, 0)
                      for b in range(self.Height + (2 * self.Cushion))]
                     for a in range(self.Width + 2 * self.Cushion)]
    
    def set_up(self, chances, rotational_symmetry=None):
        """Sets up the board with the chances of cells being born/killed"""
        width = self.Width
        height = self.Height
        if rotational_symmetry == 2:
            if width > height:
                width //= 2
            else:
                height //= 2  # Choosing which half to rotate - looks better if
        elif rotational_symmetry == 4:  # longer side is the one that is split
            width //= 2
            height //= 2
        if sum(chances) != 0:  # if there is a chance that something will actually be born
            for a in range(width):
                for b in range(height):
                    n = random.randint(1, sum(chances))
                    for c in range(len(chances)):  # Randomly assigns a new state/player to cells
                        if sum(chances[:c + 1]) > n:  # according to the chances given in config.py
                            if c != 0:
                                if not self.Players:
                                    c = 0
                                self.Cell[a][b].birth(set_up.Square, c)
                            break
        self.update()
        
        if rotational_symmetry is not None:
            if rotational_symmetry == 4:  # do rotational symmetry for one half of it - fills half
                for a in range(width):   # of the board, so the other half can be done as if it was
                    for b in range(height):  # rotational symmetry with 2 now.
                        if self.Cell[a][b].CurrentPlayer != 0:
                            player = self.Cell[a][b].CurrentPlayer + 1
                            if player > rotational_symmetry:
                                player -= rotational_symmetry  # working out which player's cell
                            if width > height:  # should be born
                                self.Cell[a][height + b].birth(self.Cell[a][b].CurrentState, player)
                            else:
                                self.Cell[width + a][b].birth(self.Cell[a][b].CurrentState, player)
                if width > height:
                    height *= 2
                else:
                    width *= 2
                self.update()
            for a in range(width):
                for b in range(height):
                    if self.Cell[a][b].CurrentPlayer != 0:
                        player = self.Cell[a][b].CurrentPlayer + rotational_symmetry // 2
                        if player > rotational_symmetry:  # working out which player's cell should
                            player -= rotational_symmetry  # be born
                        self.Cell[-1 - a][-1 - b].birth(self.Cell[a][b].CurrentState, player)
            self.update()
    
    def draw(self, screen, preview=False, update_display=True):
        """draws the current board onto the screen then updates the display"""
        if preview:
            size = self.PreviewSize
        else:
            size = self.Size - self.CellGap
        for a in range(self.Cushion, self.Cushion + self.Width):
            for b in range(self.Cushion, self.Cushion + self.Height):
                if not preview or not (self.Cell[a][b].PartImmune or self.Cell[a][b].FullImmune):
                    self.Cell[a][b].draw(screen, size, self)
        if update_display:
            pygame.display.update()
    
    def update(self, immunity=False):
        """Puts the NextState variables in the CurrentState variables,
        updates immunity if applicable"""
        for a in range(self.Width + 2 * self.Cushion):
            for b in range(self.Height + 2 * self.Cushion):
                self.Cell[a][b].update(board=self, immunity=immunity)
    
    def take_turn(self, update_caption=False, players=False):
        """Changes the NextState variables & updates display caption"""
        if update_caption:
            pygame.display.set_caption("Game of Life - Generation " + str(self.Generations))
        if self.Wrap:
            cushion = 0
        else:
            cushion = 1  # goes through all cells and kills/births those who need it.
        for a in range(cushion, self.Width + (2 * self.Cushion) - cushion):
            for b in range(cushion, self.Height + (2 * self.Cushion) - cushion):
                fate, player = self.Cell[a][b].check_fate(self, players=players)
                if self.Cell[a][b].CurrentState != fate or self.Cell[a][b].CurrentPlayer != player:
                    if fate == set_up.Dead:
                        self.Cell[a][b].kill()
                    else:
                        self.Cell[a][b].birth(fate, player)
    
    def reset(self, state):
        """Resets the board to be a plain board with no alive cells"""
        self.__init__(state, players=self.Players)
        self.update()


class SimBoard(Board):
    def place_preset(self, screen, preset_no, a, b):
        """Places desired preset at desired coordinates"""
        if self.Wrap:
            shape = preset.get(preset_no, a, b, self)[0]
        else:
            shape, a, b = preset.get(preset_no, a, b, self)
        for c in range(len(shape)):
            for d in range(len(shape[c])):
                if self.Wrap:
                    if a + c >= self.Width + 2 * self.Cushion:
                        a -= self.Width + 2 * self.Cushion
                    if b + d >= self.Height + 2 * self.Cushion:
                        b -= self.Height + 2 * self.Cushion
                if shape[c][d] == 0:
                    self.Cell[a + c][b + d].kill()
                else:
                    self.Cell[a + c][b + d].birth(shape[c][d], 0)
        self.update()
        self.draw(screen)


class GameBoard(Board):
    def show_future(self, screen, actions, player, smaller=True, immunity=True):
        """Shows how the board will look in a generation"""
        temp_board = copy.deepcopy(self)
        temp_board.impose_turns(actions, player)
        temp_board.draw(screen, update_display=False)
        if smaller:  # draws the board again but smaller and after a generation has passed
            temp_board.take_turn(players=True)
            temp_board.update(immunity=immunity)
            temp_board.draw(screen, preview=True)
    
    def show_alive(self, screen, size, colours, turns, player):
        """instead of displaying cells as squares, it shows them as numbers which show how long
        they have been alive for; this is useful in the game as you can see which cells will soon
        become immune etc."""
        temp_board = copy.deepcopy(self)
        temp_board.impose_turns(turns, player)
        for a in temp_board.Cell:
            for b in a:
                b.draw(screen, self.Size - self.CellGap, self)
                if not b.CurrentPlayer == 0:  # if the cell belongs to a player
                    set_up.write(screen, b.Coordinates[0] + self.Size // 2,
                                 b.Coordinates[1] + self.Size // 2,
                                 str(b.AliveFor), colours["Dead"], size,
                                 alignment=("centre", "centre"))
    
    def impose_turns(self, turns, player_no):
        """Takes the turns specified on the board; turns should look like:
            [generation_at_turn_no, [[a, b, kill?]...]]"""
        for a in range(len(turns[1])):
            if turns[0] == a:  # if the board needs to be generated
                self.take_turn()
                self.update(immunity=True)
            if turns[1][a][2]:
                self.Cell[turns[1][a][0]][turns[1][a][1]].kill()
            else:
                self.Cell[turns[1][a][0]][turns[1][a][1]].birth(set_up.Square, player_no)
            self.Cell[turns[1][a][0]][turns[1][a][1]].update()
        if turns[0] == len(turns[1]):  # if generation was the last thing; the above loop won't
            self.take_turn(players=True)  # catch it so it needs to be dealt with here.
            self.update(immunity=True)
