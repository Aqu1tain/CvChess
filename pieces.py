import board
#Les pièces seront stockées dans un dictionnaire qui associe chaque case de l'échiquier à une pièce correspondante. Elle stocke '.' si il n'y a pas de pièce active.
#Les pièces sont une classe python à implémenter. Superclasse pièce et sous-classes pawn, king queen etc... 

#Classe pièce (surclasse), par défaut égale au pion. Les sous-classes viennent surcharger __init__(), is_movement_legal() et is_prise_legale()
class Piece():
    def __init__(self,parent_board: object, position: str,color: str):
        self.symbol = 'p'
        self.name = "pawn"
        self.firstmovedone = False
        self.color = color
        if self.color == "Black": #Initialisation de multiplicator. Si négatif, alors la pièce est noire. Sinon, elle est blanche.
            self.multiplicator = -1
            self.symbol = self.symbol.upper()
        else: 
            self.multiplicator = 1
        self.parent_board = parent_board
        self.position = position
        
    def __str__(self): 
        """
        Affihe la phrase suivante au lieu du traditionnel : <0xf193avF9c9FZdz>
        """
        return f"{self.color} {self.name} piece at {self.position} position"

    def is_movement_legal(self, pos1, pos2):
        x = pos1[0]
        y = int(pos1[1])
        newx = pos2[0]
        newy = int(pos2[1])
        #relatif au pion : 
        if self.multiplicator * (newy - y) == 2 and self.firstmovedone == False and x == newx:
            if not self.parent_board.get_piece_from_pos(x  + str(self.multiplicator + y)):
                return True
            else:
                return False
        elif self.multiplicator * (newy - y) == 2 and self.firstmovedone == True:
            return False
        elif self.multiplicator * (newy - y) == 1 and x == newx:
            if not self.parent_board.get_piece_from_pos(pos2):
                return True
            else: 
                return False
        else:
            return self.is_prise_legale(pos1, self.parent_board.get_piece_from_pos(pos2))

    def is_prise_legale(self,pos1, piece):
        #La prise légale par défaut est celle du pion.
        if piece :
            newposition = piece.position
        else:
            return False
        newx = newposition[0]
        newy = int(newposition[1])
        x = pos1[0]
        y = int(pos1[1])

        if self.multiplicator * (newy - y) == 1 and abs(ord(x) - ord(newx)) == 1 and (self.multiplicator + piece.multiplicator) == 0: #Si la pièce est d'une autre couleur
            return True
        else:
            return False

    def does_move_checks_king(self, pos1, pos2):
        temp_board = self.parent_board.get_board_copy()
        temp_piece = temp_board[pos1]
        temp_board[pos1] = '.'
        temp_board[pos2] = temp_piece
        temp_piece.position = pos2
        
        # Vérifiez si le roi est en échec
        king_pos = '.'
        for position, piece in temp_board.items():
            if piece != '.' and piece.name == 'king' and piece.color == self.color:
                king_pos = position
                break
        if king_pos == '.':
            raise ValueError("King not found on the board")
        
        for position, piece in temp_board.items():
            if piece != '.' and piece.color != self.color and piece.is_movement_legal(position, king_pos):
                return True
        return False

        
    def move(self, newposition):
        """
        Le mouvement légal par défaut est celui du pion.
        Si la pièce est noire, la valeur(2 ème lettre(e4, 4) dans la pos sur l'échiquier), doit monter (e7 -> e5)
        Premier mouvement de 2, tous les autres de 1.
        """
        if not self.does_move_checks_king(self.position, newposition):
            if self.is_movement_legal(self.position, newposition) :
                if not self.firstmovedone:
                    self.firstmovedone = True
                print('mouvement : ' + newposition)
                if self.parent_board.get_piece_from_pos(newposition):
                    self.parent_board.get_piece_from_pos(newposition).quitter()
                self.position = newposition
            else:
                print(f"\nMouvement illégal {self.position} > {newposition} !\n")
            self.parent_board.ascii_board() #DEVELOPPEMENT SEULEMENT
        else:
            print(f"\nMouvement illégal {self.position} > {newposition} !\n")
            self.parent_board.ascii_board() #DEVELOPPEMENT SEULEMENT

    def quitter(self):
        """
        Fonction qui 'tue' une pièce
        """
        self.position = 'z0' #Si une pièce est morte, x = z et y = 0 (deux valeurs inexistantes)

#Classe tour
class Rook(Piece):
    #Surcharge de __init__()
    def __init__(self, parent_board, position, color):
        self.symbol = 'r'
        self.name = "rook"
        self.firstmovedone = False
        self.color = color
        if self.color == "Black": #Initialisation de multiplicator. Si négatif, alors la pièce est noire. Sinon, elle est blanche.
            self.multiplicator = -1
            self.symbol = self.symbol.upper()
        else:
            self.multiplicator = 1
        self.parent_board = parent_board
        self.position = position

    #Surcharges de is_movement_legal()
    def is_movement_legal(self, pos1, pos2):
        """
        La méthode vérifie selon la ligne vers laquelle on souhaite déplacer la tour, si la tour a le champ libre pour s'y déplacer.
        Sinon, elle renvoie False. Si la tour n'est pas sur aucune des mêmes lignes ou colonnes que la case ou elle est censée arriver, la fonction renvoie false.
        Sinon, si le champ est libre, alors la fonction renvoie True.

        exemple : 

        tour.is_movement_legal('e4', 'e8')
        > True
        """
        x, y = ord(pos1[0]), int(pos1[1])
        newx, newy = ord(pos2[0]), int(pos2[1])
        
        if self.parent_board.get_piece_from_pos(pos2):
            if self.parent_board.get_piece_from_pos(pos2).color == self.color:
                return False
        if x == newx:
            if y < newy:
                for i in range(y + 1, newy):
                    if self.parent_board.get_piece_from_pos(chr(x) + str(i)):
                        return False
                return True
            else:
                for i in range(newy + 1, y):
                    if self.parent_board.get_piece_from_pos(chr(x) + str(i)):
                        return False
                return True
        elif y == newy:
            if x < newx:
                for i in range(x + 1, newx):
                    if self.parent_board.get_piece_from_pos(chr(i) + str(y)):
                        return False
                return True
            else:
                for i in range(newx + 1, x):
                    if self.parent_board.get_piece_from_pos(chr(i) + str(y)):
                        return False
                return True
        else:
            return False

class Bishop(Piece):
    """La classe Bishop implémente les mouvements et les prises spéciales du fou

    Args:
        Piece (_type_): _description_
    """
    def __init__(self, parent_board, position, color):
        self.symbol = 'b'
        self.name = "bishop"
        self.firstmovedone = False
        self.color = color
        if self.color == "Black": #Initialisation de multiplicator. Si négatif, alors la pièce est noire. Sinon, elle est blanche.
            self.multiplicator = -1
            self.symbol = self.symbol.upper()
        else:
            self.multiplicator = 1
        self.parent_board = parent_board
        self.position = position

    def is_movement_legal(self, pos1, pos2):
        """
        La méthode vérifie si le déplacement du fou est valide en suivant la diagonale.
        Si le fou n'est pas sur une diagonale avec la case où il est censé arriver, la fonction renvoie false.
        Si la diagonale est libre, alors la fonction renvoie True. Si la case de destination contient une pièce ennemi,
        alors la fonction vérifie que le déplacement est une prise valide et renvoie True si c'est le cas.

        exemple : 

        fou.is_movement_legal('e4', 'a8')
        > True
        """
        x, y = ord(pos1[0]), int(pos1[1])
        newx, newy = ord(pos2[0]), int(pos2[1])
        
        if self.parent_board.get_piece_from_pos(pos2):
            if self.parent_board.get_piece_from_pos(pos2).color == self.color:
                return False

        # On vérifie si le fou se déplace sur une diagonale
        if abs(x - newx) == abs(y - newy):
            if x < newx:
                if y < newy:
                    for i in range(1, newx - x):
                        if self.parent_board.get_piece_from_pos(chr(x + i) + str(y + i)):
                            return False
                    return True
                else:
                    for i in range(1, newx - x):
                        if self.parent_board.get_piece_from_pos(chr(x + i) + str(y - i)):
                            return False
                    return True
            else:
                if y < newy:
                    for i in range(1, x - newx):
                        if self.parent_board.get_piece_from_pos(chr(x - i) + str(y + i)):
                            return False
                    return True
                else:
                    for i in range(1, x - newx):
                        if self.parent_board.get_piece_from_pos(chr(x - i) + str(y - i)):
                            return False
                    return True
        return False

class Knight(Piece):
    def __init__(self, parent_board, position, color):
        """
        La classe Knight implémente les mouvements et les prises spéciales du cavalier
        Args:
        Piece (_type_): _description_
        """
        self.symbol = 'n'
        self.name = "knight"
        self.firstmovedone = False
        self.color = color
        if self.color == "Black": #Initialisation de multiplicator. Si négatif, alors la pièce est noire. Sinon, elle est blanche.
            self.multiplicator = -1
            self.symbol = self.symbol.upper()
        else:
            self.multiplicator = 1
        self.parent_board = parent_board
        self.position = position

    def is_movement_legal(self, pos1, pos2):
        """
        La méthode vérifie si le déplacement du cavalier est valide en suivant les mouvements du cavalier dans un échiquier.
        Sinon, elle renvoie False.

        exemple : 

        cavalier.is_movement_legal('b1', 'c3')
        > True
        """
        x, y = ord(pos1[0]), int(pos1[1])
        newx, newy = ord(pos2[0]) , int(pos2[1])

        if abs(x - newx) == 2 and abs(y - newy) == 1:
            piece = self.parent_board.get_piece_from_pos(pos2)
            if piece:
                if piece.color != self.color:
                    return True
                else:
                    return False
            else:
                return True
        elif abs(y - newy) == 2 and abs(x - newx) == 1:
            return True
        else:
            return False

class Queen(Piece):
    """La classe Queen implémente les mouvements et les prises spéciales de la reine

    Args:
        Piece (_type_): _description_
    """
    def __init__(self, parent_board, position, color):
        self.symbol = 'q'
        self.name = "queen"
        self.firstmovedone = False
        self.color = color
        if self.color == "Black":
            self.multiplicator = -1
            self.symbol = self.symbol.upper()
        else:
            self.multiplicator = 1
        self.parent_board = parent_board
        self.position = position
        
    def is_movement_legal(self, pos1, pos2):
        x, y = ord(pos1[0]), int(pos1[1])
        newx, newy = ord(pos2[0]), int(pos2[1])

        piece_on_arrival = self.parent_board.get_piece_from_pos(pos2)
        if piece_on_arrival and piece_on_arrival.color == self.color: #Vérifie qu'aucune pièce ne gène.
            return False

        if x == newx:
            if y < newy:
                for i in range(y + 1, newy):
                    if self.parent_board.get_piece_from_pos(chr(x) + str(i)):
                        return False
                return True
            else:
                for i in range(newy + 1, y):
                    if self.parent_board.get_piece_from_pos(chr(x) + str(i)):
                        return False
                return True
        elif y == newy:
            if x < newx:
                for i in range(x + 1, newx):
                    if self.parent_board.get_piece_from_pos(chr(i) + str(y)):
                        return False
                return True
            else:
                for i in range(newx + 1, x):
                    if self.parent_board.get_piece_from_pos(chr(i) + str(y)):
                        return False
                return True
        elif abs(x - newx) == abs(y - newy):
            if x < newx:
                if y < newy:
                    for i in range(1, newx - x):
                        if self.parent_board.get_piece_from_pos(chr(x + i) + str(y + i)):
                            return False
                    return True
                else:
                    for i in range(1, newx - x):
                        if self.parent_board.get_piece_from_pos(chr(x + i) + str(y - i)):
                            return False
                    return True
            else:
                if y < newy:
                    for i in range(1, x - newx):
                        if self.parent_board.get_piece_from_pos(chr(x - i) + str(y + i)):
                            return False
                    return True
                else:
                    for i in range(1, x - newx):
                        if self.parent_board.get_piece_from_pos(chr(x - i) + str(y - i)):
                            return False
                    return True
        return False

class King(Piece):
    """La classe King implémente les mouvements et les prises spéciales du roi
    Args:
    Piece (_type_): _description_
    """
    def __init__(self, parent_board, position, color):
        self.symbol = 'k'
        self.name = "king"
        self.firstmovedone = False
        self.color = color
        if self.color == "Black":
            self.multiplicator = -1
            self.symbol = self.symbol.upper()
        else:
            self.multiplicator = 1
        self.parent_board = parent_board
        self.position = position
        
    def is_movement_legal(self, pos1, pos2):
        x, y = ord(pos1[0]), int(pos1[1])
        newx, newy = ord(pos2[0]), int(pos2[1])

        piece_on_arrival = self.parent_board.get_piece_from_pos(pos2)
        if piece_on_arrival and piece_on_arrival.color == self.color: #Vérifie qu'aucune pièce ne gène.
            return False

        if abs(x - newx) <= 1 and abs(y - newy) <= 1:
            return True
        return False