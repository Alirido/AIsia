from copy import deepcopy

from ChessBoard import ChessBoard

if __name__ == "__main__":
    chess_1 = ChessBoard('input.txt')
    # start-temp
    print('chessboard 1')
    chess_1.printBoardInfo()

    chess_2 = ChessBoard('input2.txt')
    print('chessboard 2')
    chess_2.printBoardInfo()
    print('chessboard 1')
    chess_1.printBoardInfo()

    chess_3 = ChessBoard('input3.txt')
    print('chessboard 3')
    chess_3.printBoardInfo()
    print('chessboard 2')
    chess_2.printBoardInfo()
    print('chessboard 1')
    chess_1.printBoardInfo()

    print()
    print('randomize chessboard 1')
    temp_board = deepcopy(chess_1.board)
    for row in temp_board:
        for piece in row:
            if piece != {}:
                # print('randomize')
                chess_1.randomizePiecePosition(piece)
    print('chessboard 1')
    chess_1.printBoardInfo()
    print('chessboard 2')
    chess_2.printBoardInfo()
    print('chessboard 3')
    chess_3.printBoardInfo()

    print()
    print('randomize chessboard 2')
    temp_board = deepcopy(chess_2.board)
    for row in temp_board:
        for piece in row:
            if piece != {}:
                # print('randomize')
                chess_2.randomizePiecePosition(piece)
    print('chessboard 1')
    chess_1.printBoardInfo()
    print('chessboard 2')
    chess_2.printBoardInfo()
    print('chessboard 3')
    chess_3.printBoardInfo()

    print()
    print('unchanged chessboard 3')
    chess_3.printBoardInfo()

    # end-temp