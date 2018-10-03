import math, random
from copy import deepcopy
from random import randint
from os import urandom
from ChessBoard import ChessBoard


def SimulatedAnnealing(ChessBoard):
    iteration = 0
    max_iteration = 10000
    T = 100000 # Temperature
    ch = 0.98 # Cooling Schedule
    
    while T > 0 and iteration < max_iteration:
        successor = deepcopy(ChessBoard)
        piece = RandomPiece(successor)
        successor._randomizePiecePosition(piece)
        if AcceptSuccessor(ChessBoard,successor,T):
            ChessBoard = successor
        T *= ch
        iteration += 1
    return ChessBoard


def AcceptSuccessor(current,successor,T):
    '''
        return true if successor accepted as new current state
    '''
    delta_h = (successor.countDiffHeuristic() - successor.countSameHeuristic()) - (current.countDiffHeuristic() - current.countSameHeuristic())
    if delta_h > 0:
        return True
    else:
        return (math.exp(delta_h / T) > random.uniform (0.0,1.0))


def RandomPiece(chessboard):
    '''
        get a random piece on chessboard
    '''
    row = randint(0,7)
    col = randint(0,7)
    while chessboard.board[row][col] == {}:
        row = randint(0,7)
        col = randint(0,7)
    return chessboard.board[row][col]