import chess

pice_mapping = {
    key: value
    for key, value in zip(chess.PIECE_SYMBOLS, chess.PIECE_NAMES)
}

def describe_move(move, is_en_passant=False):
    """
    Convert a chess move in UCI format to a human-readable format.

    Args:
        move (str): The chess move in UCI format.
        is_en_passant (bool): Whether the move is an en passant capture. Default to False.
    
    Returns:
        str: The human-readable description of the move.
        
    >>> describe_move('Nxe4#')
    'Knight captures e4 check and mate.'
    """

    move = move.lower()

    is_check = move[-1] == '+'
    is_mate = move[-1] == '#'
    if is_check or is_mate:
        move = move[:-1]

    is_pawn_move = len(move) == 2

    if move == 'o-o':
        return 'castle king size'
    if move == 'o-o-o':
        return 'castle queen size'

    square = move[-2:]

    p = move[0].upper()
    is_pice = False
    if p in [pi.upper() for pi in list(pice_mapping.keys())[1:]]:
        pice = pice_mapping[p.lower()]
        is_pice = True
    else:
        pice = p

    is_capture = False
    if 'x' in move:
        is_capture = True
        move = move.replace('x', '')

    is_doubled_pice = False
    if is_pice and len(move) == 4:
        is_doubled_pice = True

    output = ''
    if is_pawn_move:
        output = move
    else:
        output = pice + ' ' + (move[1] if is_doubled_pice else '') + (
            ' captures ' if is_capture else ' to ') + square

    if is_check:
        output += ' check'

    if is_mate:
        output += ' check and mate'

    if is_en_passant:
        output += ' en passant'

    return output
