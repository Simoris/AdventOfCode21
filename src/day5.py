import util
import numpy as np


def process_data(data):
    return [[[int(x) for x in point.split(',')] for point in line.split(' -> ')] for line in data]


def remove_diagonals(data):
    return [line for line in data if ((line[0][0] == line[1][0]) | (line[0][1] == line[1][1]))]


def find_gridsize(data):
    x = 0
    y = 0
    for line in data:
        for point in line:
            x = max(x, point[0])
            y = max(y, point[1])
    return x + 1, y + 1


def calculate_density(data):
    x, y = find_gridsize(data)
    grid = np.zeros((x, y))
    for line in data:
        [[x1, y1], [x2, y2]] = line
        if x1 == x2:
            for y in range(min(y1, y2), max(y1, y2) + 1):
                grid[x1, y] += 1
        elif y1 == y2:
            for x in range(min(x1, x2), max(x1, x2) + 1):
                grid[x, y1] += 1
        elif abs(x1 - x2) == abs(y1 - y2):
            for x, y in zip(range(x1, x2 + np.sign(x2 - x1), np.sign(x2 - x1)), range(y1, y2 + np.sign(y2 - y1), np.sign(y2 - y1))):
                grid[x, y] += 1
    return grid


def task1():
    data = util.load_data("input/day5.txt")
    data = process_data(data)
    data = remove_diagonals(data)
    grid = calculate_density(data)
    print(np.sum(grid >= 2))


def task2():
    data = util.load_data("input/day5.txt")
    data = process_data(data)
    grid = calculate_density(data)
    print(np.sum(grid >= 2))
