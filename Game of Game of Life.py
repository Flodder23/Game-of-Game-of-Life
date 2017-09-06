### a,b refers to cell (a,b) whereas x,y refers to pixel coordinates ###

import pygame
import math as maths
import config

class Cell():
    def __init__(self):
        self.CurrentState=config.Square
        self.NextState=config.Dead
    def Kill(self):
        self.NextState=config.Dead
    def Birth(self,Type):
        self.NextState=Type

def Check(a,b):
    """Checks whether the cell will be dead or alive at the end of this turn,
    and if so what type it will be"""
    Type=Board[a][b].CurrentState
    total=[0,0]
    total[Board[a+1][b].CurrentState]+=1
    total[Board[a][b+1].CurrentState]+=1
    total[Board[a-1][b].CurrentState]+=1
    total[Board[a][b-1].CurrentState]+=1
    total[Board[a+1][b+1].CurrentState]+=1
    total[Board[a-1][b-1].CurrentState]+=1
    total[Board[a+1][b-1].CurrentState]+=1
    total[Board[a-1][b+1].CurrentState]+=1
    Next=config.Dead
    if Type==config.Dead:
        if total[config.Dead]==5:# if 5 dead cells; ie. if 3 alive cells
            Next=config.Square
    if Type==config.Square:
        if total[config.Dead]==5 or total[config.Dead]==6:
            Next=config.Square
    return Next

def CleanBoard():
    return [[Cell()for a in range(config.Height+(2*config.Cushion))]for b in range(config.Width+2*config.Cushion)]

def Draw(Type,a,b,colour):
    """Draws a type of cell (Type) at the desired cell (a,b)"""
    x=(a-config.Cushion)*config.Size+config.Edge/2
    y=(b-config.Cushion)*config.Size+config.Edge/2
    s=config.Size-config.Edge
    pygame.draw.rect(Screen,(255,255,255),(x,y,s,s))
    if Type==config.Square:
        pygame.draw.rect(Screen,colour,(x,y,s,s))

def CheckUserInput(Paused):
    OneTurn=False
    for event in pygame.event.get():
        x,y=pygame.mouse.get_pos()
        a=maths.floor(x/config.Size)+config.Cushion
        b=maths.floor(y/config.Size)+config.Cushion
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            if Paused:
                Paused = False
            else:
                Paused = True
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            OneTurn=True
        if pygame.mouse.get_pressed()[0]:
            Board[a][b].Birth(config.Square)
        if pygame.mouse.get_pressed()[2]:
            Board[a][b].Kill()
    return Paused, OneTurn

def TakeTurn(Board):
    for a in range(1,config.Width+(2*config.Cushion)-1):      # Goes through all cells and kills
            for b in range(1,config.Height+(2*config.Cushion)-1): # those that will die and births
                Fate=Check(a,b)                     # those that will be born.
                if Fate==config.Dead:
                    Board[a][b].Kill()
                else:
                    Board[a][b].Birth(Fate)
    return Board

def DrawBoard():
    for a in range(config.Cushion,config.Cushion+config.Width):
        for b in range(config.Cushion,config.Cushion+config.Height):
            if Board[a][b].NextState==config.Dead:
                colour=(255,255,255)
            else:
                colour=(0,0,0)
            Draw(Board[a][b].NextState,a,b,colour) #Draws the cell as desired

def UpdateBoard(Board):
    for a in range(config.Width+2*config.Cushion):
        for b in range(config.Height+2*config.Cushion):
            Board[a][b].CurrentState=Board[a][b].NextState
    pygame.display.update ()
    return Board

pygame.init()
Screen=pygame.display.set_mode((config.Size*config.Width,config.Size*config.Height))
Screen.fill(config.Background)
pygame.display.set_caption("Game of Life")
Board=CleanBoard()
Paused=True

while True:
    Paused, OneTurn=CheckUserInput(Paused)#If game is paused OneTurn allows you to go forward one turn at a time
    if not Paused or (Paused and OneTurn):
        if OneTurn:
            OneTurn=False
        Board=TakeTurn(Board)
    DrawBoard()
    Board=UpdateBoard(Board)
        
