from copy import deepcopy

from ChessBoard import ChessBoard


if __name__ == "__main__":
    chess_1 = ChessBoard('input.txt')
    # start-temp
    print('chessboard 1')
    chess_1.printBoardInfo()

    chess_1.randomizeBoard()
    chess_1.printBoardInfo()
    
    # end-temp