def get(shape_no, a, b, state):
    """Returns a preset shape,
    and new coordinates if it can't be placed where originally intended."""
    if shape_no == 1:
        shape = [[0, 1, 0],
                 [0, 0, 1],
                 [1, 1, 1]]

    elif shape_no == 2:
        shape = [[0, 1, 0],
                 [1, 1, 1],
                 [1, 0, 1],
                 [0, 1, 0]]

    elif shape_no == 3:
        c = [1, 0, 1, 0, 1]
        d = [1, 0, 0, 0, 1]
        shape = [c, d, d, d, c]

    elif shape_no == 4:
        shape = [[0, 1, 1, 1, 1],
                 [1, 0, 0, 0, 1],
                 [0, 0, 0, 0, 1],
                 [1, 0, 0, 1, 0]]

    elif shape_no == 5:
        shape = [[0, 1, 1, 0, 1, 1, 0],
                 [0, 1, 1, 0, 1, 1, 0],
                 [0, 0, 1, 0, 1, 0, 0],
                 [1, 0, 1, 0, 1, 0, 1],
                 [1, 0, 1, 0, 1, 0, 1],
                 [1, 1, 0, 0, 0, 1, 1]]

    elif shape_no == 6:
        shape = [[0 for _ in range(15)] for _ in range(38)]  # this shape is too big to write out,
        to_be_birthed = [[23, 24, 34, 35],  # line 0         # so it is quicker to make a blank
                         [22, 24, 34, 35],          # sheet of all dead cells and birth certain ones
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

    elif shape_no == 7: shape = [[1], [1], [1], [1], [1], [1], [1], [1], [1], [1]]

    elif shape_no == 8: shape = [[0, 1, 0], [1, 1, 1], [1, 0, 0]]

    else: shape = [[0]]

    return (shape, min(a, state.Width + 2 * state.Cushion - len(shape)),
            min(b, state.Height + 2 * state.Cushion - len(shape[0])))
