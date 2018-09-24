from copy import deepcopy
from random import randint, seed, randrange
from os import urandom

from ChessBoard import ChessBoard


def GeneticAlgorithm(chessboard):
    # generating the population
    fitness_string_population = []
    population_count = 10       # may be changed
    for _ in range(population_count):
        chessboard.randomizeBoard()
        fitness = chessboard.countDiffHeuristic() - chessboard.countSameHeuristic()     # this is the fitness function
        fitness_string_population.append([fitness, _ChessboardToString(chessboard.board)])
    
    # start of genetic algorithm iteration
    fitness_string_population = _GeneticMutation(fitness_string_population)
    # for i in range(len(fitness_string_population)):
    #     fitness_string_population[i] = [fitness_string_population[i], _fitnessFunction(fitness_string_population[i], chessboard.board)]
    # # iterative - TO BE CONTINUED

def _ChessboardToString(board):
    piece_arr =[]
    for row in board:
        for piece in row:
            if piece != {}:
                loc_str = str(piece['location'][0]) + str(piece['location'][1])
                piece_arr.append([piece['id'], loc_str])
    piece_arr = sorted(piece_arr, key=lambda piece:piece[0])
    return ''.join([i[1] for i in piece_arr])

def _GeneticMutation(fitness_string):
    """
    the iterative steps of genetic algoritm
    """

    # choose the best possible mates
    fitness_string = sorted(fitness_string, key=lambda x:x[0], reverse=True)

    # selecting mates
    str_couples = []
    while fitness_string != [] :
        seed(urandom(100))
        if len(fitness_string) > 2:
            index_1 = randint(0, len(fitness_string)-1)
            index_2 = randint(0, len(fitness_string)-1)
            while index_1 == index_2:
                index_1 = randint(0, len(fitness_string)-1)
                index_2 = randint(0, len(fitness_string)-1)
        else:
            index_1 = 0
            index_2 = 1
        string_1 = fitness_string[index_1]
        string_2 = fitness_string[index_2]
        str_couples.append([string_1[1], string_2[1]])
        fitness_string.remove(string_1)
        fitness_string.remove(string_2)

    string_length = len(str_couples[0][0])
    string_result = []
    # split and cross
    for i in range(len(str_couples)):
        seed(urandom(100))
        split_index = randrange(2, string_length-2, 2)      # choose split position
        substring_1 = str_couples[i][0][:split_index]
        substring_2 = str_couples[i][1][:split_index]
        string_result.append(substring_2 + str_couples[i][0][split_index:])
        string_result.append(substring_1 + str_couples[i][1][split_index:])

    # mutation
    for i in range(len(string_result)):
        seed(urandom(100))
        str_temp = list(string_result[i])
        str_temp[randint(0, len(str_temp)-1)] = str(randint(0, 7))
        str_temp = ''.join(str_temp)
        while not(_isStringUnique(str_temp)):
            str_temp = list(string_result[i])
            str_temp[randint(0, len(str_temp)-1)] = str(randint(0, 7))
            str_temp = ''.join(str_temp)
        string_result[i] = str_temp
    # return the modified strings
    return string_result

def _isStringUnique(string):
    str_arr = [string[i:i+2] for i in range(0, len(string), 2)]
    i = 0
    while i <= len(str_arr)-2:
        j = i+1
        while j <= len(str_arr)-1:
            if str_arr[i] == str_arr[j]:
                return False
            j += 1
        i += 1
    return True 

# def _fitnessFunction(string, board):
#     for id in range(board.cou)

if __name__ == '__main__':
    chess = ChessBoard('input.txt')
    # string = _ChessboardToString(chess.board)
    # print(string)
    print('genetic algorithm')
    GeneticAlgorithm(chess)
