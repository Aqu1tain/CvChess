import pygame
import pieces
import board

class ChessGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 800))
        pygame.display.set_caption("Chess Game")
        self.images = {}
        self.turn = "White"
        self.selected_piece = None
        self.chess_board = board.Chess_Board()
        self.create_board()

    def create_board(self):
        size = int(100 * 0.9)
        for row in range(8):
            for col in range(8):
                x0 = col * 100
                y0 = row * 100
                x1 = x0 + 100
                y1 = y0 + 100
                color = (240, 217, 181) if (row + col) % 2 == 0 else (181, 136, 99)
                pygame.draw.rect(self.screen, color, (x0, y0, x1, y1))

        for pos, piece in self.chess_board.board_positions.items():
            if piece == '.':
                continue
            row, col = 8 - int(pos[1]), ord(pos[0]) - ord('a')
            x, y = col * 100 + 50 - size // 2, row * 100 + 50 - size // 2
            self.screen.blit(self.get_image(piece), (x, y))
            
        if self.selected_piece:
            moves = self.chess_board.get_valid_moves(self.selected_piece)
            for move in moves:
                row, col = 8 - int(move[1][1]), ord(move[1][0]) - ord('a')
                x, y = col * 100 + 50 , row * 100 + 50 
                pygame.draw.circle(self.screen, (130,151,105), (x, y), 15)


        pygame.display.update()

    def get_image(self, piece):
        symbol = piece.symbol
        color = piece.color[0].lower()
        filename = f"Images/{color}{symbol}.png"
        if filename in self.images:
            return self.images[filename]

        image = pygame.image.load(filename)
        size = int(100 * 0.9) # 90% de la taille de la case
        image = pygame.transform.scale(image, (size, size))
        self.images[filename] = image
        return image

    def run(self):
        running = True
        self.selected_piece = None
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()
                    row, col = y // 100, x // 100
                    pos = chr(col + ord('a')) + str(8 - row)
                    piece = self.chess_board.get_piece_from_pos(pos)
                    if piece and piece != '.' and not self.selected_piece:
                        if piece.color == self.turn:
                            self.selected_piece = pos
                            self.create_board()
                    elif self.selected_piece:
                        if self.chess_board.is_valid_move(self.selected_piece, pos):
                            self.chess_board.move(self.selected_piece, pos)
                            self.selected_piece = None
                            if self.turn == "White":
                                self.turn = "Black"
                            else:
                                self.turn = "White"
                            self.create_board()
                        else:
                            self.selected_piece = None
        pygame.quit()


if __name__ == "__main__":
    game = ChessGame()
    game.run()