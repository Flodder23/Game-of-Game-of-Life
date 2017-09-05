### a,b refers to cell (a,b) whereas x,y refers to pixel coordinates ###

import pygame as pg, math as m, time as t, random as r

Width=50    #C 50 How many squares wide the board is
Height=30   #C 30 Ditto but with height
Size=20     #C 20 The size of the sides of each square (in pixels)
Cushion=5   #C 10 How far the board extends beyond the visible amount
Edge=m.ceil(Size/7)    #C Size/15 The gap between each cell
Paused=True #Does this need a description?
Board=[]    #A 2d matrix representing the board
Background=(120,120,120)    #C (120,120,120) The colour of the background
Dead=0
Square=1

class Cell():
    def __init__(self):
        self.CurrentState=1
        self.NextState=0
    def Kill(self):
        self.NextState=0
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
    Next=0
    if Type==0:
        if total[0]==5:
            Next=1
    if Type==Square:
        if total[0]==5 or total[0]==6:
            Next=1
    return Next

def Reset():
    global Board
    Board=[[Cell()for a in range(Height+(2*Cushion))]for b in range(Width+2*Cushion)]

def Draw(Type,a,b,colour):
    """Draws a type of cell (Type) at the desired cell (a,b)"""
    x=(a-Cushion)*Size+Edge/2
    y=(b-Cushion)*Size+Edge/2
    s=Size-Edge
    pg.draw.rect(Screen,(255,255,255),(x,y,s,s))

    if Type==Square:
        pg.draw.rect(Screen,colour,(x,y,s,s))

pg.init()
Screen=pg.display.set_mode((Size*Width,Size*Height))
Screen.fill(Background)
pg.display.set_caption("Game of Life")
Reset()

print("""
LEFT CLICK to make a Board "alive".\n
RIGHT CLICK to Kill a cell.\n
Press SPACE to pause/unpause the game.\n""")

while True:
    for event in pg.event.get(): #Checks for SPACE input for pausing/unpausing
        x,y=pg.mouse.get_pos()
        a=m.floor(x/Size)+Cushion
        b=m.floor(y/Size)+Cushion
        if pg.key.get_pressed()[pg.K_SPACE]:
            if Paused:
                Paused = False
            else:
                Paused = True
        if pg.mouse.get_pressed()[0]:
            Board[a][b].Birth(Square)
        if pg.mouse.get_pressed()[2]:
            Board[a][b].Kill()
    if not Paused: 
        for a in range(1,Width+(2*Cushion)-1):      # Goes through all cells and kills
            for b in range(1,Height+(2*Cushion)-1): # those that will die and births
                Fate=Check(a,b)                # those that will be born.
                if Fate==0: #c is the next state and d is False if Cell wasn't
                    Board[a][b].Kill()# "born" and the cell it turns into if
                else: #it was "born".
                    Board[a][b].Birth(Fate)
    for a in range(Cushion,Width+Cushion):#This is seperate to when the values are
        for b in range(Cushion,Height+Cushion):# changed because not all cells are
##            if Board[a][b].CurrentState!=Board[a][b].NextState:# shown due to the
            if Board[a][b].NextState==0:# cushion.
                colour=(255,255,255)
            else:
                colour=(0,0,0)
            Draw(Board[a][b].NextState,a,b,colour) #Draws the cell as desired
    for a in range(0,Width+(2*Cushion)):
        for b in range(0,Height+(2*Cushion)):
            Board[a][b].CurrentState=Board[a][b].NextState #Updates CurrentState variable
    pg.display.update ()
