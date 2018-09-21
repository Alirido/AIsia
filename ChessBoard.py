from random import randint, seed
from copy import deepcopy
from os import urandom

class ChessBoard:
    size = 8
    board = [[{} for _ in range(8)] for _ in range(8)]
    count_black_pieces = 0
    count_white_pieces = 0

    '''
    a box object may contain the following
        1. id               --> integer
        2. type             --> string  [QUEEN, BISHOP, KNIGHT, ROOK]
        3. colour           --> sting   [BLACK, WHITE]
        4. heuristic_same   --> integer
        5. heuristic_diff   --> integer
        5. location         --> tuple   (row, coloumn)
    
    function that may be used:
        countPieceAttack(board, piece, location, colour)
        newTemporaryBoard(self, board, piece, new_location)
    '''

  
    # constructor
    def __init__(self, file_name):
        '''
            file_name = the name of the input file (e.g. 'input.txt')
        '''
        count = 0
        # read from file
        with open(file_name, 'r') as f:
            buffer = f.readline()
            while buffer != '':
                buffer_arr = buffer.replace('\n', '').split(' ')
                for _ in range(int(buffer_arr[2])):
                    self.addChessPiece(count, buffer_arr[0], buffer_arr[1])
                    count += 1
                    if buffer_arr[0] == 'BLACK':
                        self.count_black_pieces += 1
                    else:   # buffer_arr[0] == 'WHITE'
                        self.count_white_pieces += 1
                buffer = f.readline()
        for row in self.board:
            for piece in row:
                if piece != {}:
                    self.setPieceHeuristic(piece)
                    # print(piece)
                    # print()
        print('ChessBoard object successfully created')
  
    def addChessPiece(self, id, colour, type):
        '''
            (for constructor)
            Adding a piece to the board
            id      = the id of the given piece
            colour  = the colour of the piece
            type    = type of the piece
        '''
        row = id // self.size
        col = id % self.size
        piece = {
            'id': id,
            'type': type,
            'colour': colour,
            'heuristic_same': 0,
            'heuristic_diff': 0,
            'location': (row, col)
        }
        self.board[row][col] = piece

    def printBoardInfo(self):
        for row in self.board:
            for piece in row:
                if piece == {}:
                    print('.', end=' ')
                elif piece['colour'] == 'BLACK':
                    if piece['type'] == 'QUEEN':
                        print('q', end=' ')
                    elif piece['type'] == 'ROOK':
                        print('r', end=' ')
                    elif piece['type'] == 'BISHOP':
                        print('b', end=' ')
                    else:   # piece.type == KNIGHT
                        print('k', end=' ')
                else:   # piece['colour'] == 'WHITE'
                    if piece['type'] == 'QUEEN':
                        print('Q', end=' ')
                    elif piece['type'] == 'ROOK':
                        print('R', end=' ')
                    elif piece['type'] == 'BISHOP':
                        print('B', end=' ')
                    else:   # piece.type == KNIGHT
                        print('K', end=' ')
            print()
        attack_same = self.countSameHeuristic()
        attack_diff = self.countDiffHeuristic()
        print(attack_same, attack_diff)
        # start-temp
        print('TOTAL:', attack_same + attack_diff)
        # end-temp

    def countHorVerAttack(self, board, position, colour):
        '''
            position    = (tuple) the position of the piece
            colour      = the colour of what the piece can attack
        '''
        count = 0
        row = position[0]
        col = position[1]
        # check to NORTH
        row -= 1
        while (row >= 0) and (board[row][col] == {}):
            row -= 1
        if (row >= 0) and (board[row][col]['colour'] == colour):
            count += 1
            # print(board[row][col])
        row = position[0]
        # check to SOUTH
        row += 1
        while (row < self.size) and (board[row][col] == {}):
            row += 1
        if (row < self.size) and (board[row][col]['colour'] == colour):
            count += 1
            # print(board[row][col])
        row = position[0]
        # check to WEST
        col -= 1
        while (col >= 0) and (board[row][col] == {}):
            col -= 1
        if (col >= 0) and (board[row][col]['colour'] == colour):
            count += 1
            # print(board[row][col])
        col = position[1]
        # check to EAST
        col += 1
        while (col < self.size) and (board[row][col] == {}):
            col += 1
        if (col < self.size) and (board[row][col]['colour'] == colour):
            count += 1
            # print(board[row][col])
        return count
    
    def countDiagonalAttack(self, board, position, colour):
        '''
            position    = (tuple) the position of the piece
            colour      = the colour of what the piece can attack
        '''
        count = 0
        row = position[0]
        col = position[1]
        # check NORTH-EAST
        row -= 1
        col += 1
        while (row >= 0) and (col < self.size) and (board[row][col] == {}):
            row -= 1
            col += 1
        if (row >= 0) and (col < self.size) and (board[row][col]['colour'] == colour):
            count += 1
            # print(board[row][col])
        row = position[0]
        col = position[1]
        # check NORTH-WEST
        row -= 1
        col -= 1
        while (row >= 0) and (col >= 0) and (board[row][col] == {}):
            row -= 1
            col -= 1
        if (row >= 0) and (col >= 0) and (board[row][col]['colour'] == colour):
            count += 1
            # print(board[row][col])
        row = position[0]
        col = position[1]
        # check SOUTH-EAST
        row += 1
        col += 1
        while (row < self.size) and (col < self.size) and (board[row][col] == {}):
            row += 1
            col += 1
        if (row < self.size) and (col < self.size) and (board[row][col]['colour'] == colour):
            count += 1
            # print(board[row][col])
        row = position[0]
        col = position[1]
        # check SOUTH-WEST
        row += 1
        col -= 1
        while (row < self.size) and (col >= 0) and (board[row][col] == {}):
            row += 1
            col -= 1
        if (row < self.size) and (col >= 0) and (board[row][col]['colour'] == colour):
            count += 1
            # print(board[row][col])         
        return count
    
    def countKnightAttack(self, board, position, colour):
        '''
            position    = (tuple) the position of the piece
            colour      = the colour of what the piece can attack

            attack range of a knight
                - o - o -   first row
                o - - - o   second row
                - - K - -   knight's row
                o - - - o   third row
                - o - o -   fourth row
        '''
        count = 0
        row = position[0]
        col = position[1]
        # check second row
        if row-1 >= 0:
            if (col-2 >= 0) and (board[row-1][col-2] != {}) and (board[row-1][col-2]['colour'] == colour):
                count += 1
                # print(board[row-1][col-2])
            if (col+2 < self.size) and (board[row-1][col+2] != {}) and (board[row-1][col+2]['colour'] == colour):
                count += 1
                # print(board[row-1][col+2])
            # check first row
            if row-2 >= 0:
                if (col-1 >=0) and (board[row-2][col-1] != {}) and (board[row-2][col-1]['colour'] == colour):
                    count += 1
                    # print(board[row-2][col-1])
                if (col+1 < self.size) and (board[row-2][col-1] != {}) and (board[row-2][col-1]['colour'] == colour):
                    count += 1
                    # print(board[row-2][col-1])
        # check third row
        if row+1 < self.size:
            if (col-2 >= 0) and (board[row+1][col-2] != {}) and (board[row+1][col-2]['colour'] == colour):
                count += 1
                # print(board[row+1][col-2])
            if (col+2 < self.size) and (board[row+1][col+2] != {}) and (board[row+1][col+2]['colour'] == colour):
                count += 1
                # print(board[row+1][col+2])
            # check fourth row
            if row+2 < self.size:
                if (col-2 >= 0) and (board[row+2][col-2] != {}) and (board[row+2][col-2]['colour'] == colour):
                    count += 1
                    # print(board[row+2][col-2])
                if (col+2 < self.size) and (board[row+2][col+2] != {}) and (board[row+2][col+2]['colour'] == colour):
                    count += 1
                    # print(board[row+2][col+2])
        return count

    def countPieceAttack(self, board, piece, location, colour):
        '''
            board       = the chessboard (may be temporary)
            piece       = the piece that its heuristic will be checked
            location    = the location of piece that will be located (may be the same)
            colour      = the colour of pieces that will be attacked
        '''
        if piece['location'] != location:
            # moving piece to new location
            board = self.newTemporaryBoard(board, piece, location)
        # determine type and attack count
        if piece['type'] == 'QUEEN':
            return self.countHorVerAttack(board, location, colour) + self.countDiagonalAttack(board, location, colour)
        elif piece['type'] == 'ROOK':
            return self.countHorVerAttack(board, location, colour)
        elif piece['type'] == 'BISHOP':
            return self.countDiagonalAttack(board, location, colour)
        else:   # piece.type == KNIGHT
            return self.countKnightAttack(board, location, colour)

    def newTemporaryBoard(self, board, piece, new_location):
        '''
            board           = the old chessboard
            piece           = the piece that will be moved
            new_location    = the location of piece that will be located
        '''
        board[piece['location'][0]][piece['location'][1]] = {}
        piece['location'] = new_location
        board[new_location[0]][new_location[1]] = piece
        return board

    def setPieceHeuristic(self, piece):
        row = piece['location'][0]
        col = piece['location'][1]
        self.board[row][col]['heuristic_same'] = self.countPieceAttack(self.board, piece, piece['location'], piece['colour'])
        if piece['colour'] == 'BLACK':
            self.board[row][col]['heuristic_diff'] = self.countPieceAttack(self.board, piece, piece['location'], 'WHITE')
        else:   # piece['colour'] == 'WHITE'
            self.board[row][col]['heuristic_diff'] = self.countPieceAttack(self.board, piece, piece['location'], 'BLACK')
    
    def randomizePiecePosition(self, piece):
        self.board[piece['location'][0]][piece['location'][1]] = {}
        seed(urandom(100))
        row = randint(0, self.size-1)
        col = randint(0, self.size-1)
        while self.board[row][col] != {}:
            seed(urandom(100))
            row = randint(0, self.size-1)
            col = randint(0, self.size-1)
        self.board[piece['location'][0]][piece['location'][1]] = {}
        piece['location'] = (row, col)
        self.board[row][col] = piece
        # print((row, col))
        self.setPieceHeuristic(piece)

    def countSameHeuristic(self):
        count = 0
        for row in self.board:
            for piece in row:
                if piece != {}:
                    count += self.countPieceAttack(self.board, piece, piece['location'], piece['colour'])
        return count
    
    def countDiffHeuristic(self):
        count = 0
        for row in self.board:
            for piece in row:
                if piece != {}:
                    if piece['colour'] == 'BLACK':
                        count += self.countPieceAttack(self.board, piece, piece['location'], 'WHITE')
                    else:   # piece['colour'] == 'BLACK'
                        count += self.countPieceAttack(self.board, piece, piece['location'], 'BLACK')
        return count

if __name__ == "__main__":
    chess = ChessBoard('input.txt')
    # start-temp
    chess.printBoardInfo()
    print()
    # for row in chess.board:
    #         for piece in row:
    #             if piece != {}:
    #                 print(piece)

    cont = 'y'
    while cont == 'y':
        print()
        temp_board = deepcopy(chess.board)
        for row in temp_board:
            for piece in row:
                if piece != {}:
                    # print('randomize')
                    chess.randomizePiecePosition(piece)
        chess.printBoardInfo()
        cont = input('Generate papan baru? (y/n) ')
    # end-temp