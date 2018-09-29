from ChessBoard import ChessBoard

if __name__ == "__main__":
    file_path = input('Masukan nama file input: ')
    chess = ChessBoard(file_path)

    print('Pilihan algoritma:')
    print('1. Hill-Climbing')
    print('2. Simulated Annealing')
    print('3. Genetic')
    algo_choice = int(input('Algoritma mana yang ingin dipakai? '))
    while algo_choice not in [1, 2, 3]:
        print()
        print('Input salah. Tolong ulangi.')
        algo_choice = int(input('Algoritma mana yang ingin dipakai? '))

    if algo_choice == 1:        # hill-climbing
        algo_name = 'Hill-Climbing'
    elif algo_choice == 2:      # simulated annealing
        algo_name = 'Simulated Annealing'
    else:                       # genetic (algo_choice == 3)
        algo_name = 'Genetic'

    print('Hasil dari algoritma ' + algo_name)
    chess.printBoardInfo()