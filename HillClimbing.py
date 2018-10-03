from copy import deepcopy
from ChessBoard import ChessBoard


def HillClimbingAlgorithm(chessboard):
    chessboard.randomizeBoard()
    empty_loc = EmptyLocation(chessboard)
    piece_list = Pieces(chessboard)
    successor = BestNeighbor(chessboard, empty_loc, piece_list)
    while heuristic(successor) > heuristic(chessboard):
        chessboard = successor
        empty_loc = EmptyLocation(chessboard)
        piece_list = Pieces(chessboard)
        successor = BestNeighbor(chessboard, empty_loc, piece_list)
    return chessboard


def EmptyLocation(chessboard):
    '''
        return list of empty location on chessboard
    '''
    empty_loc = []
    for row in range(8):
        for col in range(8):
            if chessboard.board[row][col] == {}:
                empty_loc.append((row,col))
    return empty_loc


def Pieces(chessboard):
    '''
        return list of piece on chessboard
    '''
    piece_list = []
    for row in chessboard.board:
        for piece in row:
            if piece != {}:
                piece_list.append(piece)
    return piece_list


def BestNeighbor(chessboard, empty_loc, piece_list):
    max_heuristic = heuristic(chessboard)
    best_board = chessboard
    for piece in piece_list:
        for loc in empty_loc:
            temp_piece = deepcopy(piece)
            temp_board = deepcopy(chessboard)
            temp_board.movePiece(temp_piece, loc)
            temp_heuristic = heuristic(temp_board)
            if temp_heuristic > max_heuristic:
                best_board = temp_board
                max_heuristic = temp_heuristic
    return best_board


def heuristic(chessboard):
    return chessboard.countDiffHeuristic() - chessboard.countSameHeuristic()
