from copy import deepcopy

from ChessBoard import ChessBoard
from SimulatedAnnealing import SimulatedAnnealing

if __name__ == "__main__":
    chess_1 = ChessBoard('input2.txt')
    # start-temp
    print('chessboard 1')
    chess_1.printBoardInfo()

    # chess_2 = deepcopy(chess_1)
    # chess_2.printBoardInfo()

    # chess_1.randomizeBoard()
    # print('CHESS 1')
    # chess_1.printBoardInfo()
    # print('CHESS 2')
    # chess_2.printBoardInfo()

    print()
    SimulatedAnnealing(chess_1).run()

    # chess_1.randomizeBoard()
    # chess_1.printBoardInfo()
    
    # end-temp