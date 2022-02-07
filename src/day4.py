import util
import numpy as np


def process_data(data):
    numbers = [int(x) for x in data[0].split(',')]
    data = data[2:]

    boards = []
    board = []
    for line in data:
        if line == "":
            boards.append(np.array(board))
            board = []
        else:
            board.append([int(x) for x in line.split(' ') if x != ''])

    return boards, numbers


def calculate_score(board, marks, factor):
    return np.ma.array(data=board, mask=marks).sum()*factor


def check_won(marks):
    return np.array([line.all() for line in marks]).any() | np.array([line.all() for line in marks.T]).any()


def find_winner(boards, numbers):
    marks = [np.full_like(board, False, dtype=bool) for board in boards]

    for num in numbers:
        for i, _ in enumerate(boards):
            marks[i] = marks[i] | (boards[i] == num)
            if check_won(marks[i]):
                return boards[i], marks[i], num

    return False, False, False


def find_looser(boards, numbers):
    marks = [np.full_like(board, False, dtype=bool) for board in boards]
    has_won = np.full(len(boards), False)

    for num in numbers:
        for i, won in enumerate(has_won):
            if not won:
                marks[i] = marks[i] | (boards[i] == num)
                if check_won(marks[i]):
                    has_won[i] = True
                    if has_won.all():
                        return boards[i], marks[i], num


def task1():
    data = util.load_data("input/day4.txt")
    boards, numbers = process_data(data)
    w_board, w_mark, factor = find_winner(boards, numbers)

    print(calculate_score(w_board, w_mark, factor))


def task2():
    data = util.load_data("input/day4.txt")
    boards, numbers = process_data(data)
    l_board, l_mark, factor = find_looser(boards, numbers)

    print(calculate_score(l_board, l_mark, factor))
