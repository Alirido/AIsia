import random, math, time
from random import seed, randint
from decimal import Decimal
from datetime import datetime
from copy import deepcopy
from os import urandom
from ChessBoard import ChessBoard

class SimulatedAnnealing:
    # Constructor
    def __init__(self, chessBoard):
        self.chessBoard = chessBoard
        self.iteration = 0
        self.max_it = 10000
        self.T = 100000 # Temperature
        self.ch = 0.98 # Cooling Schedule

    def run(self):
        current = deepcopy(self.chessBoard)
        while (self.T>0 and self.iteration<self.max_it):
            successor = deepcopy(current)
            piece = self.RandomPiece(successor)
            successor._randomizePiecePosition(piece)
            if (self.acceptsuccessor(current,successor)):
                current = successor
            self.T *= self.ch
            self.iteration += 1
        
        self.chessBoard = deepcopy(current)


    def acceptsuccessor(self,current,successor):
        delta_h = (successor.countDiffHeuristic() - successor.countSameHeuristic()) - (current.countDiffHeuristic() - current.countSameHeuristic())
        if(delta_h>0):
            return True
        else:
            return (math.exp(delta_h / self.T) > random.uniform (0.0,1.0))

    def RandomPiece(self,chessboard):
        row = randint(0,7)
        col = randint(0,7)
        while(chessboard.board[row][col] == {}):
            row = randint(0,7)
            col = randint(0,7)
        return chessboard.board[row][col]

# if __name__ == '__main__':

#     chess = ChessBoard('input3.txt')
#     sa = SimulatedAnnealing(chess)
#     sa.run()