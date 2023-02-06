import pieces
import copy
#Chess_Board en POO : 

class Chess_Board():
    def __init__(self ,nbcases=8):
        self.nbcases = nbcases
        self.board = [] #L'échiquier sera représenté par une matrice. Numérotés de a1 à h8. Cf Notation PGN.
        
        for i in range(self.nbcases, 0, -1): #La boucle qui crée l'échiquier, et qui complète self.board
            temp = [] #variable temporaire
            for j in range(self.nbcases):
                temp.append(chr(97 + j) + str(i))
            self.board.append(temp)
        
        self.board_positions = {} 
        self.populate_board(True)

    def cases_echiquier(self):
        """
        Méthode qui donne une représentation console des noms des cases de l'échiquier.
        """
        for i in range(len(self.board)):
            string = ''
            for k in range(len(self.board)):
                string += self.board[i][k] + '  '
            print(string + '\n')

    def populate_board(self, normale=True):
        if normale :
            for i in self.board:
                for k in i:
                    #Noirs
                    y = int(k[1])
                    x = str(k[0])
                    if y == 7 :
                        self.board_positions[k] = pieces.Piece(self, k, 'Black')
                    elif y == 2 :
                        self.board_positions[k] = pieces.Piece(self, k, 'White')
                    elif y == 1 and (x == 'a' or x == 'h'):
                        self.board_positions[k] = pieces.Rook(self, k, 'White')
                    elif y == 8 and (x == 'a' or x == 'h'):
                        self.board_positions[k] = pieces.Rook(self, k, 'Black')
                    elif y == 1 and (x == 'b' or x == 'g'):
                        self.board_positions[k] = pieces.Knight(self, k, 'White')
                    elif y == 8 and (x == 'b' or x == 'g'):
                        self.board_positions[k] = pieces.Knight(self, k, 'Black')
                    elif y == 1 and (x == 'c' or x == 'f'):
                        self.board_positions[k] = pieces.Bishop(self, k, 'White')
                    elif y == 8 and (x == 'c' or x == 'f'):
                        self.board_positions[k] = pieces.Bishop(self, k, 'Black')
                    elif y == 1 and x == 'd':
                        self.board_positions[k] = pieces.Queen(self, k, 'White')
                    elif y == 8 and x == 'd':
                        self.board_positions[k] = pieces.Queen(self, k, 'Black')
                    elif y == 1 and x == 'e':
                        self.board_positions[k] = pieces.King(self, k, 'White')
                    elif y == 8 and x == 'e':
                        self.board_positions[k] = pieces.King(self, k, 'Black')
                    else:
                        self.board_positions[k] = '.'#Implémenter les pièces suivantes
        else:
            pass #Variations du mode de jeu

    def ascii_board(self, changepov=False):
        self.update_board()
        if not changepov:
            ligne = ''
            for i in self.board_positions:
                if not self.board_positions[i] == '.':
                    ligne += self.board_positions[i].symbol + ' '
                else:
                    ligne += '. '
                if i[0] == chr(96 + self.nbcases):
                    print(ligne)
                    ligne = ''

    def get_piece_from_pos(self, position: str):
        self.update_board()
        """Retourne un objet pièce situé à la position demandée, sinon, retourne None."""
        if self.board_positions[position] != '.':
            return self.board_positions[position]
        else:
            return None

    def move(self, pos1, pos2):
        self.get_piece_from_pos(pos1).move(pos2)
        self.update_board()

    def update_board(self):
        actualboard = self.board_positions.copy()
        for i in actualboard:
            actualpos = self.board_positions[i]
            if actualpos != '.':
                if actualpos.position != i:
                    temp = self.board_positions[i]
                    self.board_positions[i] = '.'
                    self.board_positions[actualpos.position] = temp
                else:
                    pass
            else:
                pass
    def get_board_copy(self):
        return copy.deepcopy(self.board_positions)
    def is_valid_move(self, pos1, pos2):
        piece = self.board_positions.get(pos1)
        if not piece or piece == '.':
            return False
        if piece.is_movement_legal(pos1, pos2):
            return True

        return False
    def get_valid_moves(self, piece):
        moves = []
        for i in self.board_positions:
            pos2 = self.board_positions[i]
            if pos2 :
                if self.get_piece_from_pos(piece).is_movement_legal(piece, i):
                    moves.append((piece, i))
        return moves