import config

def place(board, shape, a, b):
    """Places a preset shape."""
    if shape == 1:
        if a + 2 >= board.Width + board.Cushion:
            a = board.Width + board.Cushion - 3
        if b + 2 >= board.Height + board.Cushion:
            b = board.Height + board.Cushion - 3
        board.Cell[a][b].kill()
        board.Cell[a + 1][b].birth(config.Square)
        board.Cell[a + 2][b].kill()
        board.Cell[a][b + 1].kill()
        board.Cell[a + 1][b + 1].kill()
        board.Cell[a + 2][b + 1].birth(config.Square)
        board.Cell[a][b + 2].birth(config.Square)
        board.Cell[a + 1][b + 2].birth(config.Square)
        board.Cell[a + 2][b + 2].birth(config.Square)

    elif shape == 2:
        if a + 2 >= board.Width + board.Cushion:
            a = board.Width + board.Cushion - 3
        if b + 3 >= board.Height + board.Cushion:
            b = board.Height + board.Cushion - 4
        board.Cell[a][b].kill()
        board.Cell[a + 1][b].birth(config.Square)
        board.Cell[a + 2][b].kill()
        board.Cell[a][b + 1].birth(config.Square)
        board.Cell[a + 1][b + 1].birth(config.Square)
        board.Cell[a + 2][b + 1].birth(config.Square)
        board.Cell[a][b + 2].birth(config.Square)
        board.Cell[a + 1][b + 2].kill()
        board.Cell[a + 2][b + 2].birth(config.Square)
        board.Cell[a][b + 3].kill()
        board.Cell[a + 1][b + 3].birth(config.Square)
        board.Cell[a + 2][b + 3].kill()

    elif shape == 3:
        if a + 3 >= board.Width + board.Cushion:
            a = board.Width + board.Cushion - 5
        if b + 4 >= board.Height + board.Cushion:
            b = board.Height + board.Cushion - 5
        for c in range(3):
            for d in range(5):
                board.Cell[a + c + 1][b + d].kill()
                board.Cell[a][b + d].birth(config.Square)
                board.Cell[a + 4][b + d].birth(config.Square)
        board.Cell[a + 2][b].birth(config.Square)
        board.Cell[a + 2][b + 4].birth(config.Square)

    elif shape == 4:
        if a + 10 >= board.Width + board.Cushion:
            a = board.Width + board.Cushion - 12
        for c in range(10):
            board.Cell[a + c][b].birth(config.Square)

    elif shape == 5:
        if a + 5 >= board.Width + board.Cushion:
            a = board.Width + board.Cushion - 5
        if b + 4 >= board.Height + board.Cushion:
            b = board.Height + board.Cushion - 4
        for c in range(5):
            for d in range(4):
                board.Cell[a + c][b + d].kill()
        for e in range(4):
            board.Cell[a + e + 1][b].birth(config.Square)
        board.Cell[a][b + 1].birth(config.Square)
        board.Cell[a + 4][b + 1].birth(config.Square)
        board.Cell[a + 4][b + 2].birth(config.Square)
        board.Cell[a][b + 3].birth(config.Square)
        board.Cell[a + 3][b + 3].birth(config.Square)

    elif shape == 6:
        if a + 7 >= board.Width + board.Cushion:
            a = board.Width + board.Cushion - 7
        if b + 6 >= board.Height + board.Cushion:
            b = board.Height + board.Cushion - 6
        for c in range(7):
            for d in range(6):
                board.Cell[a + c][b + d].birth(config.Square)
        board.Cell[a][b].kill()
        board.Cell[a + 3][b].kill()
        board.Cell[a + 6][b].kill()
        board.Cell[a][b + 1].kill()
        board.Cell[a + 3][b + 1].kill()
        board.Cell[a + 6][b + 1].kill()
        board.Cell[a][b + 2].kill()
        board.Cell[a + 1][b + 2].kill()
        board.Cell[a + 3][b + 2].kill()
        board.Cell[a + 5][b + 2].kill()
        board.Cell[a + 6][b + 2].kill()
        board.Cell[a + 1][b + 3].kill()
        board.Cell[a + 3][b + 3].kill()
        board.Cell[a + 5][b + 3].kill()
        board.Cell[a + 1][b + 4].kill()
        board.Cell[a + 3][b + 4].kill()
        board.Cell[a + 5][b + 4].kill()
        board.Cell[a + 2][b + 5].kill()
        board.Cell[a + 3][b + 5].kill()
        board.Cell[a + 4][b + 5].kill()

    elif shape == 7:
        if a + 38 >= board.Width + board.Cushion:
            a = board.Width + board.Cushion - 38
        if b + 15 >= board.Height + board.Cushion:
            b = board.Height + board.Cushion - 15
        for c in range(38):
            for d in range(15):
                board.Cell[a + c][b + d].kill()
        board.Cell[a + 23][b].birth(config.Square)
        board.Cell[a + 24][b].birth(config.Square)
        board.Cell[a + 34][b].birth(config.Square)
        board.Cell[a + 35][b].birth(config.Square)
        board.Cell[a + 22][b + 1].birth(config.Square)
        board.Cell[a + 24][b + 1].birth(config.Square)
        board.Cell[a + 34][b + 1].birth(config.Square)
        board.Cell[a + 35][b + 1].birth(config.Square)
        board.Cell[a][b + 2].birth(config.Square)
        board.Cell[a + 1][b + 2].birth(config.Square)
        board.Cell[a + 9][b + 2].birth(config.Square)
        board.Cell[a + 10][b + 2].birth(config.Square)
        board.Cell[a + 22][b + 2].birth(config.Square)
        board.Cell[a + 23][b + 2].birth(config.Square)
        board.Cell[a][b + 3].birth(config.Square)
        board.Cell[a + 1][b + 3].birth(config.Square)
        board.Cell[a + 8][b + 3].birth(config.Square)
        board.Cell[a + 10][b + 3].birth(config.Square)
        board.Cell[a + 8][b + 4].birth(config.Square)
        board.Cell[a + 9][b + 4].birth(config.Square)
        board.Cell[a + 16][b + 4].birth(config.Square)
        board.Cell[a + 17][b + 4].birth(config.Square)
        board.Cell[a + 16][b + 5].birth(config.Square)
        board.Cell[a + 18][b + 5].birth(config.Square)
        board.Cell[a + 16][b + 6].birth(config.Square)
        board.Cell[a + 35][b + 7].birth(config.Square)
        board.Cell[a + 36][b + 7].birth(config.Square)
        board.Cell[a + 35][b + 8].birth(config.Square)
        board.Cell[a + 37][b + 8].birth(config.Square)
        board.Cell[a + 35][b + 9].birth(config.Square)
        board.Cell[a + 24][b + 12].birth(config.Square)
        board.Cell[a + 25][b + 12].birth(config.Square)
        board.Cell[a + 26][b + 12].birth(config.Square)
        board.Cell[a + 24][b + 13].birth(config.Square)
        board.Cell[a + 25][b + 14].birth(config.Square)

    return board
