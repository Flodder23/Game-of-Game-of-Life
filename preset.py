import config

def place(board, shape, a, b):
    """Places a preset shape."""
    if shape == 1:
        if a + 2 >= config.Width + config.Cushion:
            a = config.Width + config.Cushion - 3
        if b + 2 >= config.Height + config.Cushion:
            b = config.Height + config.Cushion - 3
        board[a][b].kill()
        board[a + 1][b].birth(config.Square)
        board[a + 2][b].kill()
        board[a][b + 1].kill()
        board[a + 1][b + 1].kill()
        board[a + 2][b + 1].birth(config.Square)
        board[a][b + 2].birth(config.Square)
        board[a + 1][b + 2].birth(config.Square)
        board[a + 2][b + 2].birth(config.Square)

    elif shape == 2:
        if a + 2 >= config.Width + config.Cushion:
            a = config.Width + config.Cushion - 3
        if b + 3 >= config.Height + config.Cushion:
            b = config.Height + config.Cushion - 4
        board[a][b].kill()
        board[a + 1][b].birth(config.Square)
        board[a + 2][b].kill()
        board[a][b + 1].birth(config.Square)
        board[a + 1][b + 1].birth(config.Square)
        board[a + 2][b + 1].birth(config.Square)
        board[a][b + 2].birth(config.Square)
        board[a + 1][b + 2].kill()
        board[a + 2][b + 2].birth(config.Square)
        board[a][b + 3].kill()
        board[a + 1][b + 3].birth(config.Square)
        board[a + 2][b + 3].kill()

    elif shape == 3:
        if a + 3 >= config.Width + config.Cushion:
            a = config.Width + config.Cushion - 5
        if b + 4 >= config.Height + config.Cushion:
            b = config.Height + config.Cushion - 5
        for c in range(3):
            for d in range(5):
                board[a + c + 1][b + d].kill()
                board[a][b + d].birth(config.Square)
                board[a + 4][b + d].birth(config.Square)
        board[a + 2][b].birth(config.Square)
        board[a + 2][b + 4].birth(config.Square)

    elif shape == 4:
        if a + 10 >= config.Width + config.Cushion:
            a = config.Width + config.Cushion - 12
        for c in range(10):
            board[a + c][b].birth(config.Square)

    elif shape == 5:
        if a + 5 >= config.Width + config.Cushion:
            a = config.Width + config.Cushion - 5
        if b + 4 >= config.Height + config.Cushion:
            b = config.Height + config.Cushion - 4
        for c in range(5):
            for d in range(4):
                board[a + c][b + d].kill()
        for e in range(4):
            board[a + e + 1][b].birth(config.Square)
        board[a][b + 1].birth(config.Square)
        board[a + 4][b + 1].birth(config.Square)
        board[a + 4][b + 2].birth(config.Square)
        board[a][b + 3].birth(config.Square)
        board[a + 3][b + 3].birth(config.Square)

    elif shape == 6:
        if a + 7 >= config.Width + config.Cushion:
            a = config.Width + config.Cushion - 7
        if b + 6 >= config.Height + config.Cushion:
            b = config.Height + config.Cushion - 6
        for c in range(7):
            for d in range(6):
                board[a + c][b + d].birth(config.Square)
        board[a][b].kill()
        board[a + 3][b].kill()
        board[a + 6][b].kill()
        board[a][b + 1].kill()
        board[a + 3][b + 1].kill()
        board[a + 6][b + 1].kill()
        board[a][b + 2].kill()
        board[a + 1][b + 2].kill()
        board[a + 3][b + 2].kill()
        board[a + 5][b + 2].kill()
        board[a + 6][b + 2].kill()
        board[a + 1][b + 3].kill()
        board[a + 3][b + 3].kill()
        board[a + 5][b + 3].kill()
        board[a + 1][b + 4].kill()
        board[a + 3][b + 4].kill()
        board[a + 5][b + 4].kill()
        board[a + 2][b + 5].kill()
        board[a + 3][b + 5].kill()
        board[a + 4][b + 5].kill()

    elif shape == 7:
        if a + 38 >= config.Width + config.Cushion:
            a = config.Width + config.Cushion - 38
        if b + 15 >= config.Height + config.Cushion:
            b = config.Height + config.Cushion - 15
        for c in range(38):
            for d in range(15):
                board[a + c][b + d].kill()
        board[a + 23][b].birth(config.Square)
        board[a + 24][b].birth(config.Square)
        board[a + 34][b].birth(config.Square)
        board[a + 35][b].birth(config.Square)
        board[a + 22][b + 1].birth(config.Square)
        board[a + 24][b + 1].birth(config.Square)
        board[a + 34][b + 1].birth(config.Square)
        board[a + 35][b + 1].birth(config.Square)
        board[a][b + 2].birth(config.Square)
        board[a + 1][b + 2].birth(config.Square)
        board[a + 9][b + 2].birth(config.Square)
        board[a + 10][b + 2].birth(config.Square)
        board[a + 22][b + 2].birth(config.Square)
        board[a + 23][b + 2].birth(config.Square)
        board[a][b + 3].birth(config.Square)
        board[a + 1][b + 3].birth(config.Square)
        board[a + 8][b + 3].birth(config.Square)
        board[a + 10][b + 3].birth(config.Square)
        board[a + 8][b + 4].birth(config.Square)
        board[a + 9][b + 4].birth(config.Square)
        board[a + 16][b + 4].birth(config.Square)
        board[a + 17][b + 4].birth(config.Square)
        board[a + 16][b + 5].birth(config.Square)
        board[a + 18][b + 5].birth(config.Square)
        board[a + 16][b + 6].birth(config.Square)
        board[a + 35][b + 7].birth(config.Square)
        board[a + 36][b + 7].birth(config.Square)
        board[a + 35][b + 8].birth(config.Square)
        board[a + 37][b + 8].birth(config.Square)
        board[a + 35][b + 9].birth(config.Square)
        board[a + 24][b + 12].birth(config.Square)
        board[a + 25][b + 12].birth(config.Square)
        board[a + 26][b + 12].birth(config.Square)
        board[a + 24][b + 13].birth(config.Square)
        board[a + 25][b + 14].birth(config.Square)

    return board
