import random
import math
from decimal import Decimal
from datetime import datetime
from copy import deepcopy

class SimulatedAnnealing:
    # Constructor
    def __init__(self, chessBoard):
        self.chessBoard = chessBoard
        self.T = 60*60      # Temperature
        self.ch = 0.05     # Cooling Schedule
        self.elapsedTime = 0
        self.startTime = datetime.now()

    def run(self):
        self.chessBoard.randomizeBoard()
        current = deepcopy(self.chessBoard)

        stop = Decimal('0.05')
        if self.chessBoard.count_black_pieces == 0 or self.chessBoard.count_white_pieces == 0:
            current_h = current.countSameHeuristic()

            while self.T > stop:
                if current_h == 0:
                    break
                self.chessBoard.randomizeBoard()
                successor = deepcopy(self.chessBoard)
                successor_h = successor.countSameHeuristic()
                delta_h = successor_h - current_h
                if (delta_h <= 0) or math.exp(delta_h / self.T) > random.uniform(0.0, 1.0):
                    current = deepcopy(successor)
                    current_h = successor_h
                self.T -= self.ch
                print(self.T)
        else:
            current_h = current.countDiffHeuristic() - current.countSameHeuristic()
            while self.T > stop:
                self.chessBoard.randomizeBoard()
                successor = deepcopy(self.chessBoard)
                successor_h = successor.countDiffHeuristic() - successor.countSameHeuristic()
                delta_h = successor_h - current_h
                if (delta_h <= 0) or math.exp(delta_h / self.T) > random.uniform(0,1):
                    current = deepcopy(successor)
                    current_h = successor_h
                self.T -= self.ch

        # current.printBoardInfo()
        # self.elapsedTime = self.getElapsedTime()
        # print("Success, Elapsed Time: %sms" % (str(self.elapsedTime)))

        return self.elapsedTime

    def getElapsedTime(self):
        endTime = datetime.now()
        elapsedTime = (endTime - self.startTime).microseconds / 1000
        return elapsedTime