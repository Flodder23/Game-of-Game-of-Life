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
        to_be_birthed = [[23, 24, 34, 35],  # 0
                         [22, 24, 34, 35],
                         [0, 1, 9, 10, 22, 23],
                         [0, 1, 8, 10],
                         [8, 9, 16, 17],
                         [16, 18],  # 5
                         [16],
                         [35, 36],
                         [35, 37],
                         [35],
                         [],  # 10
                         [],
                         [24, 25, 26],
                         [24],
                         [25]]
        for c in range(len(to_be_birthed)):
            for d in to_be_birthed[c]:
                shape[d][c] = 1

    elif shape_no == 7:
        if a + 10 >= config.Width + config.Cushion:
            a = config.Width + config.Cushion - 12
        shape = [[1], [1], [1], [1], [1], [1], [1], [1], [1], [1]]

    elif shape_no == 8:
        if a + 3 >= config.Width + config.Cushion:
            a = config.Width + config.Cushion - 3
        if b + 3 >= config.Height + config.Cushion:
            b = config.Height + config.Cushion - 3
        shape = [[0, 1, 0], [1, 1, 1], [1, 0, 0]]

    else: shape = [[0]]

    return shape, a, b
