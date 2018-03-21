def get(shape_no, a, b, state):
    """Returns a preset shape."""
    if shape_no == 1:
        a, b = correct_coordinates(a, b, 2, 2, state)
        shape = [[0, 1, 0],
                 [0, 0, 1],
                 [1, 1, 1]]

    elif shape_no == 2:
        a, b = correct_coordinates(a, b, 3, 2, state)
        shape = [[0, 1, 0],
                 [1, 1, 1],
                 [1, 0, 1],
                 [0, 1, 0]]

    elif shape_no == 3:
        a, b = correct_coordinates(a, b, 4, 4, state)
        c = [1, 0, 1, 0, 1]
        d = [1, 0, 0, 0, 1]

        shape = [c, d, d, d, c]

    elif shape_no == 4:
        a, b = correct_coordinates(a, b, 3, 4, state)
        shape = [[0, 1, 1, 1, 1],
                 [1, 0, 0, 0, 1],
                 [0, 0, 0, 0, 1],
                 [1, 0, 0, 1, 0]]

    elif shape_no == 5:
        a, b = correct_coordinates(a, b, 5, 6, state)
        shape = [[0, 1, 1, 0, 1, 1, 0],
                 [0, 1, 1, 0, 1, 1, 0],
                 [0, 0, 1, 0, 1, 0, 0],
                 [1, 0, 1, 0, 1, 0, 1],
                 [1, 0, 1, 0, 1, 0, 1],
                 [1, 1, 0, 0, 0, 1, 1]]

    elif shape_no == 6:
        a, b = correct_coordinates(a, b, 37, 14, state)
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
        a, b = correct_coordinates(a, b, 9, 0, state)
        shape = [[1], [1], [1], [1], [1], [1], [1], [1], [1], [1]]

    elif shape_no == 8:
        a, b = correct_coordinates(a, b, 2, 2, state)
        shape = [[0, 1, 0], [1, 1, 1], [1, 0, 0]]

    else: shape = [[0]]

    return shape, a, b


def correct_coordinates(a, b, x_a, x_b, state):
    if a + x_a >= state.Width + state.Cushion:
        a = state.Width + state.Cushion - x_a - 1
    if b + x_b >= state.Height + state.Cushion:
        b = state.Height + state.Cushion - x_b - 1
    return a, b