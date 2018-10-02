from random import randint, seed
from os import urandom


class ChessBoard:
    size = 8
    """
    a box object may contain the following
        1. id               --> integer
        2. type             --> string  [QUEEN, BISHOP, KNIGHT, ROOK]
        3. colour           --> sting   [BLACK, WHITE]
        4. heuristic_same   --> integer
        5. heuristic_diff   --> integer
        5. location         --> tuple   (row, coloumn)
    """

    # constructor
    def __init__(self, file_name):
        """
        :param file_name: the name of the input file (e.g. 'input.txt')
        """
        self.board = [[{} for _ in range(8)] for _ in range(8)]
        self.count_black_pieces = 0
        self.count_white_pieces = 0
        count = 0
        # read from file
        with open(file_name, 'r') as f:
            buffer = f.readline()
            while buffer != '':
                buffer_arr = buffer.replace('\n', '').split(' ')
                for _ in range(int(buffer_arr[2])):
                    self._addChessPiece(count, buffer_arr[0], buffer_arr[1])
                    count += 1
                    if buffer_arr[0] == 'BLACK':
                        self.count_black_pieces += 1
                    else:  # buffer_arr[0] == 'WHITE'
                        self.count_white_pieces += 1
                buffer = f.readline()
        for row in self.board:
            for piece in row:
                if piece != {}:
                    self._setPieceHeuristic(piece)
        print('ChessBoard object successfully created')

    def _addChessPiece(self, id, colour, type):
        """
            Adding a piece to the board
            :param id: the id of the given piece
            :param colour: the colour of the piece
            :param type: type of the piece
        """
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

    def _countHorVerAttack(self, board, position, colour):
        """
            :param board: the chessboard
            :param position: (tuple) the position of the piece
            :param colour: the colour of what the piece can attack
            :return:
        """
        count = 0
        row = position[0]
        col = position[1]
        # check to NORTH
        row -= 1
        while (row >= 0) and (board[row][col] == {}):
            row -= 1
        if (row >= 0) and (board[row][col]['colour'] == colour):
            count += 1
        row = position[0]
        # check to SOUTH
        row += 1
        while (row < self.size) and (board[row][col] == {}):
            row += 1
        if (row < self.size) and (board[row][col]['colour'] == colour):
            count += 1
        row = position[0]
        # check to WEST
        col -= 1
        while (col >= 0) and (board[row][col] == {}):
            col -= 1
        if (col >= 0) and (board[row][col]['colour'] == colour):
            count += 1
        col = position[1]
        # check to EAST
        col += 1
        while (col < self.size) and (board[row][col] == {}):
            col += 1
        if (col < self.size) and (board[row][col]['colour'] == colour):
            count += 1
        return count

    def _countDiagonalAttack(self, board, position, colour):
        """
            :param board: the chessboard
            :param position: (tuple) the position of the piece
            :param colour: the colour of what the piece can attack
            :return:
        """
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
        return count

    def _countKnightAttack(self, board, position, colour):
        """
            :param board: the chessboard
            :param position: (tuple) the position of the piece
            :param colour: the colour of what the piece can attack
            :return:
            attack range of a knight
            - o - o -   first row
            o - - - o   second row
            - - K - -   knight's row
            o - - - o   third row
            - o - o -   fourth row
        """
        count = 0
        row = position[0]
        col = position[1]

        # check second row
        if row - 1 >= 0:
            if (col - 2 >= 0) and (board[row - 1][col - 2] != {}) and (board[row - 1][col - 2]['colour'] == colour):
                count += 1
            if (col + 2 < self.size) and (board[row - 1][col + 2] != {}) and (
                    board[row - 1][col + 2]['colour'] == colour):
                count += 1
            # check first row
        if row - 2 >= 0:
            if (col - 1 >= 0) and (board[row - 2][col - 1] != {}) and (board[row - 2][col - 1]['colour'] == colour):
                count += 1
            if (col + 1 < self.size) and (board[row - 2][col + 1] != {}) and (
                    board[row - 2][col + 1]['colour'] == colour):
                count += 1
        # check third row
        if row + 1 < self.size:
            if (col - 2 >= 0) and (board[row + 1][col - 2] != {}) and (board[row + 1][col - 2]['colour'] == colour):
                count += 1
            if (col + 2 < self.size) and (board[row + 1][col + 2] != {}) and (
                    board[row + 1][col + 2]['colour'] == colour):
                count += 1
            #    print(row+1,col+2)
            # check fourth row
        if row + 2 < self.size:
            if (col - 1 >= 0) and (board[row + 2][col - 1] != {}) and (board[row + 2][col - 1]['colour'] == colour):
                count += 1
            if (col + 1 < self.size) and (board[row + 2][col + 1] != {}) and (
                    board[row + 2][col + 1]['colour'] == colour):
                count += 1
        return count

    def _setPieceHeuristic(self, piece):
        """
        :param piece: the piece whose heuristics will be updated
        :return:
        """
        row = piece['location'][0]
        col = piece['location'][1]
        self.board[row][col]['heuristic_same'] = self.countPieceAttack(self.board, piece, piece['location'], piece['colour'])
        if piece['colour'] == 'BLACK':
            self.board[row][col]['heuristic_diff'] = self.countPieceAttack(self.board, piece, piece['location'], 'WHITE')
        else:  # piece['colour'] == 'WHITE'
            self.board[row][col]['heuristic_diff'] = self.countPieceAttack(self.board, piece, piece['location'], 'BLACK')

    def _updateAllHeuristics(self):
        """
            Update all heuristics (same and different colous) of all pieces
            <<< use only when the board have reached desired state to minimize usage >>>
        """
        for row in self.board:
            for piece in row:
                if piece != {}:
                    self._setPieceHeuristic(piece)

    def countPieceAttack(self, board, piece, location, colour):
        """
            :param board: the chessboard (may be temporary)
            :param piece: the piece that its heuristic will be checked
            :param location: the location of piece that will be located (may be the same)
            :param colour: the colour of pieces that will be attacked
            :return:
        """
        if piece['location'] != location:
            # moving piece to new location
            board = self.newTemporaryBoard(board, piece, location)
        # determine type and attack count
        if piece['type'] == 'QUEEN':
            return self._countHorVerAttack(board, location, colour) + self._countDiagonalAttack(board, location, colour)
        elif piece['type'] == 'ROOK':
            return self._countHorVerAttack(board, location, colour)
        elif piece['type'] == 'BISHOP':
            return self._countDiagonalAttack(board, location, colour)
        else:  # piece.type == KNIGHT
            return self._countKnightAttack(board, location, colour)


    def movePiece(self, piece, new_location):
        old_loc = piece['location']
        piece['location'] = new_location
        piece_temp = self.board[new_location[0]][new_location[1]]
        # swap places
        self.board[new_location[0]][new_location[1]] = piece
        if piece_temp != {}:
            piece_temp['location'] = old_loc
        self.board[old_loc[0]][old_loc[1]] = piece_temp
        self._updateAllHeuristics()

    def _randomizePiecePosition(self, piece):
        """
        <<< only for randomizeBoard() usage >>>
        :param piece: the piece whose location will be randomized
        :return:
        """
        seed(urandom(100))
        row = randint(0, self.size - 1)
        col = randint(0, self.size - 1)
        self.movePiece(piece, (row, col))

    def randomizeBoard(self):
        # place pieces in a new, random position
        for piece_id in range(self.count_black_pieces + self.count_white_pieces):
            self._randomizePiecePosition(self.findPieceById(piece_id))
        
    def countSameHeuristic(self):
        """
            Counting the heuristic of attacking the same colour of the board
            :return:
        """
        count = 0
        for row in self.board:
            for piece in row:
                if piece != {}:
                    count += piece['heuristic_same']
        return count

    def countDiffHeuristic(self):
        """
            Counting the heuristic of attacking different colour of the board
            :return:
        """
        count = 0
        for row in self.board:
            for piece in row:
                if piece != {}:
                    count += piece['heuristic_diff']
        return count

    def findPieceById(self, id):
        for row in self.board:
            for piece in row:
                if piece != {} and piece['id'] == id:
                    return piece
        return {}

    def printBoardInfo(self):
        """
            Print the board contents and the information of the overall heuristics
        """
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
                    else:  # piece.type == KNIGHT
                        print('k', end=' ')
                else:  # piece['colour'] == 'WHITE'
                    if piece['type'] == 'QUEEN':
                        print('Q', end=' ')
                    elif piece['type'] == 'ROOK':
                        print('R', end=' ')
                    elif piece['type'] == 'BISHOP':
                        print('B', end=' ')
                    else:  # piece.type == KNIGHT
                        print('K', end=' ')
            print()
        attack_same = self.countSameHeuristic()
        attack_diff = self.countDiffHeuristic()
        print(attack_same, attack_diff)

    def _printAllPieces(self):
        for row in self.board:
            for piece in row:
                if piece != {}:
                    print(piece)
