import board

def parse_pgn_move(move: str, color: str, board: object):
    """_summary_

    Args:
        move (str): Le mouvement joué par le joueur
        color (str): La couleur du joueur qui joue ('White' ou 'Black')
        board (object): Le plateau de jeu.

    Returns:
        tuple: La pièce que le joueur à bougée, suivie de là où il l'a bougée.
        exemple : ("e4", "e5")
    """
    multiplicator = 1
    if color == "Black":
        multiplicator = -1
    #Si le mouvement est celui d'un pion
    if len(move) == 2:
        firstPosition = move[0] + str(int(move[1]) - multiplicator)
        piece = board.get_piece_from_pos(firstPosition)
        if piece :
            return firstPosition , move
        else:
            secondposition = move[0] + str(int(move[1]) - multiplicator * 2)
            secondpiece = board.get_piece_from_pos(secondposition)
            if secondpiece:
                return secondposition, move
            else:
                return None
    elif len(move) == 3:
        #Piece qui bouge
        pass
    elif len(move) == 4:
        #Piece qui prend
        pass

newboard = board.Chess_Board()
newboard.move('e2', 'e4')
print(parse_pgn_move("e4", 'White', newboard))