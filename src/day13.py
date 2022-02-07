import numpy as np


def load_and_process_data(path):
    file = open(path, "r")
    data = file.read()
    dots, folds = data.split('\n\n')
    # Process dots
    dots = [[int(num) for num in line.split(',')] for line in dots.split('\n')]
    max_x = 0
    max_y = 0
    for line in dots:
        if line[0] > max_x:
            max_x = line[0]
        if line[1] > max_y:
            max_y = line[1]
    dot_array = np.zeros((max_x + 1, max_y + 1))
    for line in dots:
        dot_array[line[0], line[1]] = 1
    # Process folds
    folds = folds.split('\n')[:-1]
    return dot_array, folds


def fold(dots, instruction):
    axis = instruction[11]
    c = int(instruction[13:])
    if axis == 'x':
        dots = dots[:c, :] + np.flipud(dots[c + 1:, :])
    elif axis == 'y':
        dots = dots[:, :c] + np.fliplr(dots[:, c + 1:])
    return dots


def task1():
    dots, folds = load_and_process_data("input/day13.txt")
    dots = fold(dots, folds[0])
    print(np.sum(dots > 0))


def task2():
    dots, folds = load_and_process_data("input/day13.txt")
    for instr in folds:
        dots = fold(dots, instr)
    print(dots.T)
