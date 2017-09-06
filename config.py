import math as m

Width=50    #C 50 How many squares wide the board is
Height=30   #C 30 Ditto but with height
Size=20     #C 20 The size of the sides of each square (in pixels)
Cushion=5   #C 10 How far the board extends beyond the visible amount
Edge=m.ceil(Size/7)    #C Size/15 The gap between each cell
Background=(120,120,120)    #C (120,120,120) The colour of the background
Dead=0
Square=1
