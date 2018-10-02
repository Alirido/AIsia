from copy import deepcopy
from random import randint, seed, randrange
from os import urandom
from time import clock


def geneticAlgorithm(chessboard):
    # generating the population
    init_chessboard = deepcopy(chessboard)
    fitness_string_population = []
    population_count = 8 * (chessboard.count_black_pieces + chessboard.count_white_pieces)
    for _ in range(population_count):
        chessboard.randomizeBoard()
        fitness = chessboard.countDiffHeuristic() - chessboard.countSameHeuristic()  # this is the fitness function
        fitness_string_population.append([fitness, _ChessboardToString(chessboard.board)])

    # sort the inviiduals based on fitness function
    fitness_string_population = sorted(fitness_string_population, key=lambda x: x[0], reverse=True)

    # start of genetic algorithm iteration
    fittest_individual = fitness_string_population[0]
    fittest_count = 1

    # start of iteration of genetic algorithm
    while fittest_count < (population_count*3):
        fitness_string_population = _GeneticMutation(fitness_string_population, population_count)
        for i in range(len(fitness_string_population)):
            fitness_string_population[i] = [_fitnessFunction(fitness_string_population[i], deepcopy(init_chessboard)),
                                            fitness_string_population[i]]
        # sort the inviiduals based on fitness function
        fitness_string_population = sorted(fitness_string_population, key=lambda x: x[0], reverse=True)

        # checking whether the result have become convergent or not
        if fittest_individual[0] < fitness_string_population[0][0]:
            fittest_count = 0
            fittest_individual = deepcopy(fitness_string_population[0])
        else:
            fittest_count += 1

    return _StringToChessboard(fittest_individual[1], init_chessboard)


def _ChessboardToString(board):
    piece_arr = []
    for row in board:
        for piece in row:
            if piece != {}:
                loc_str = str(piece['location'][0]) + str(piece['location'][1])
                piece_arr.append([piece['id'], loc_str])
    piece_arr = sorted(piece_arr, key=lambda p: p[0])
    return ''.join([i[1] for i in piece_arr])


def _StringToChessboard(string, chessboard):
    board_temp = deepcopy(chessboard)
    amount_of_piece = chessboard.count_white_pieces + chessboard.count_black_pieces
    for piece_id in range(amount_of_piece):
        row = int(string[piece_id * 2])
        col = int(string[piece_id * 2 + 1])
        piece = board_temp.findPieceById(piece_id)
        chessboard.movePiece(piece, (row, col))
    return chessboard


def _GeneticMutation(fitness_string, population_space):
    """
    the iterative steps of genetic algorithm
    """

    # selecting and crossing
    individual_result = []
    population_space_left = population_space
    for i in range(len(fitness_string)-1):
        individual = fitness_string[i][1]
        potential_mates = fitness_string[i+1:]
        new_individuals, population_space_left = _selectedMates(individual, potential_mates, population_space_left)
        individual_result.extend(new_individuals)
        if population_space_left <= 0:
            break

    # mutation
    for i in range(len(individual_result)):
        seed(urandom(100))
        probability = randint(1, 10)
        str_temp = list(individual_result[i])
        str_temp[randint(0, len(str_temp) - 1)] = str(randint(0, 7))
        str_temp = ''.join(str_temp)
        while not(_isStringUnique(str_temp)) and (probability < 4):
            str_temp = list(individual_result[i])
            str_temp[randint(0, len(str_temp) - 1)] = str(randint(0, 7))
            str_temp = ''.join(str_temp)
            probability = randint(1, 10)
        if probability < 4:     # probability of mutation: 40%
            individual_result[i] = str_temp

    # return the modified strings
    return individual_result


def _isStringUnique(string):
    str_arr = [string[i:i + 2] for i in range(0, len(string), 2)]
    for i in range(len(str_arr)-1):
        for j in range(i+1, len(str_arr)):
            if str_arr[i] == str_arr[j]:
                return False
    return True

def _selectedMates(individual, potential_mates, population_space_left):
    """
    <<< used only for _GeneticMutation() >>>
    :param individual: string of the individual
    :param potential_mates: list of strings of individual's potential mates' string
    :param population_space_left: amount of individuals left to be generated
    :return:
    """
    string_length = len(individual)
    rand_bound = string_length // 2
    new_individuals = []

    seed(clock())
    # i = 0
    for _,mate in potential_mates:
        # print('mate', mate)
        rand_count = 1
        split_index = randrange(2, string_length - 2, 2)  # choose split position
        indv_2 = mate[:split_index] + individual[split_index:]
        indv_1 = individual[:split_index] + mate[split_index:]
        while not(_isStringUnique(indv_1) and _isStringUnique(indv_2)) and (rand_count < rand_bound):
            rand_count += 1
            split_index = randrange(2, string_length - 2, 2)  # choose split position
            indv_2 = mate[:split_index] + individual[split_index:]
            indv_1 = individual[:split_index] + mate[split_index:]
        if rand_count < rand_bound:
            population_space_left -= 2
            new_individuals.extend([indv_1, indv_2])
        if population_space_left <= 0:      # stop the loop if population count is reached
            break
    return new_individuals, population_space_left

def _fitnessFunction(string, chessboard):
    chessboard = _StringToChessboard(string, chessboard)
    return chessboard.countDiffHeuristic() - chessboard.countSameHeuristic()
