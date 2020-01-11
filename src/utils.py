def _generate_sequence(start, direction, maximum):
    dx, dy = direction
    x, y = start
    next_val = x + dx, y + dy

    while next_val[0] in range(maximum[0]) and next_val[1] in range(maximum[1]):
        yield next_val
        x, y = next_val
        next_val = x + dx, y + dy


def connect_in_direction(game, start, direction):
    row, column = start
    piece = game.get_piece_at_position(row=row, column=column)

    count = 1
    #  I am worried I'm getting these game.width and game_height wrong. how can
    #  I make sure I never confuse them.
    for row, column in _generate_sequence(
        start=start, direction=direction, maximum=(game.width, game.height)
    ):
        if game.get_piece_at_position(row=row, column=column) == piece:
            count += 1
        else:
            break

    # reverse direction
    for row, column in _generate_sequence(
        start=start,
        direction=(-direction[0], -direction[1]),
        maximum=(game.width, game.height),
    ):
        if game.get_piece_at_position(row=row, column=column) == piece:
            count += 1
        else:
            break

    if count == 4:
        return True
    return False
