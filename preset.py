import config


def get(shape_no, a, b):
    """Returns a preset shape."""
    if shape_no == 1:
        if a + 2 >= config.Width + config.Cushion:
            a = config.Width + config.Cushion - 3
        if b + 2 >= config.Height + config.Cushion:
            b = config.Height + config.Cushion - 3
        shape = [[0, 1, 0],
                 [0, 0, 1],
                 [1, 1, 1]]

    elif shape_no == 2:
        if a + 2 >= config.Width + config.Cushion:
            a = config.Width + config.Cushion - 3
        if b + 3 >= config.Height + config.Cushion:
            b = config.Height + config.Cushion - 4
        shape = [[0, 1, 0],
                 [1, 1, 1],
                 [1, 0, 1],
                 [0, 1, 0]]

    elif shape_no == 3:
        if a + 3 >= config.Width + config.Cushion:
            a = config.Width + config.Cushion - 5
        if b + 4 >= config.Height + config.Cushion:
            b = config.Height + config.Cushion - 5
        c = [1, 0, 1, 0, 1]
        d = [1, 0, 0, 0, 1]

        shape = [c, d, d, d, c]

    elif shape_no == 4:
        if a + 5 >= config.Width + config.Cushion:
            a = config.Width + config.Cushion - 5
        if b + 4 >= config.Height + config.Cushion:
            b = config.Height + config.Cushion - 4
        shape = [[0, 1, 1, 1, 1],
                 [1, 0, 0, 0, 1],
                 [0, 0, 0, 0, 1],
                 [1, 0, 0, 1, 0]]

    elif shape_no == 5:
        if a + 7 >= config.Width + config.Cushion:
            a = config.Width + config.Cushion - 7
        if b + 6 >= config.Height + config.Cushion:
            b = config.Height + config.Cushion - 6
        shape = [[0, 1, 1, 0, 1, 1, 0],
                 [0, 1, 1, 0, 1, 1, 0],
                 [0, 0, 1, 0, 1, 0, 0],
                 [1, 0, 1, 0, 1, 0, 1],
                 [1, 0, 1, 0, 1, 0, 1],
                 [1, 1, 0, 0, 0, 1, 1]]

    elif shape_no == 6:
        if a + 38 >= config.Width + config.Cushion:
            a = config.Width + config.Cushion - 38
        if b + 15 >= config.Height + config.Cushion:
            b = config.Height + config.Cushion - 15
        shape = [[0 for _ in range(15)] for _ in range(38)]
        shape[23][0] = 1
        shape[24][0] = 1
        shape[34][0] = 1
        shape[35][0] = 1
        shape[22][1] = 1
        shape[24][1] = 1
        shape[34][1] = 1
        shape[35][1] = 1
        shape[0][2] = 1
        shape[1][2] = 1
        shape[9][2] = 1
        shape[10][2] = 1
        shape[22][2] = 1
        shape[23][2] = 1
        shape[0][3] = 1
        shape[1][3] = 1
        shape[8][3] = 1
        shape[10][3] = 1
        shape[8][4] = 1
        shape[9][4] = 1
        shape[16][4] = 1
        shape[17][4] = 1
        shape[16][5] = 1
        shape[18][5] = 1
        shape[16][6] = 1
        shape[35][7] = 1
        shape[36][7] = 1
        shape[35][8] = 1
        shape[37][8] = 1
        shape[35][9] = 1
        shape[24][12] = 1
        shape[25][12] = 1
        shape[26][12] = 1
        shape[24][13] = 1
        shape[25][14] = 1

    elif shape_no == 7:
        if a + 10 >= config.Width + config.Cushion:
            a = config.Width + config.Cushion - 12
        shape = [[1], [1], [1], [1], [1], [1], [1], [1], [1], [1]]

    return shape, a, b
