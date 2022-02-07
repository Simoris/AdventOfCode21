import util
import numpy as np


def process_data(data):
    return np.array([[int(num) for num in line] for line in data])


def tile_map(data):
    x, y = data.shape
    full_map = np.empty((5 * x, 5 * y))
    for i in range(2*5 - 1):
        for j in range(min(i + 1, 9 - i)):
            i0 = i - j
            j0 = j
            if i > 4:
                i0 -= i - 4
                j0 += i - 4
            full_map[i0*x:(i0+1)*x, j0*x:(j0+1)*y] = data
        data += 1
        data[data == 10] = 1
    return full_map


def find_safest_path(data):
    value = np.full_like(data, np.inf, dtype=float)
    value[-1, -1] = 0
    old_values = data
    x, y = data.shape

    while (value != old_values).any():
        old_values = value.copy()
        for i in range(x):
            for j in range(y):
                if i > 0 and value[i - 1, j] + data[i - 1, j] < value[i, j]:
                    value[i, j] = value[i - 1, j] + data[i - 1, j]
                if j > 0 and value[i, j - 1] + data[i, j - 1] < value[i, j]:
                    value[i, j] = value[i, j - 1] + data[i, j - 1]
                if i < x - 1 and value[i + 1, j] + data[i + 1, j] < value[i, j]:
                    value[i, j] = value[i + 1, j] + data[i + 1, j]
                if j < y - 1 and value[i, j + 1] + data[i, j + 1] < value[i, j]:
                    value[i, j] = value[i, j + 1] + data[i, j + 1]
    return value[0, 0]


def opt_find_safest_path(data):
    value = np.full_like(data, np.inf, dtype=float)
    value[-1, -1] = 0
    x, y = data.shape

    to_check = [(x - 1, y - 1)]

    while len(to_check) > 0:
        (i, j) = to_check.pop(0)
        if i > 0 and value[i - 1, j] > value[i, j] + data[i, j]:
            value[i - 1, j] = value[i, j] + data[i, j]
            to_check.append((i - 1, j))
        if j > 0 and value[i, j - 1] > value[i, j] + data[i, j]:
            value[i, j - 1] = value[i, j] + data[i, j]
            to_check.append((i, j - 1))
        if i < x - 1 and value[i + 1, j] > value[i, j] + data[i, j]:
            value[i + 1, j] = value[i, j] + data[i, j]
            to_check.append((i + 1, j))
        if j < y - 1 and value[i, j + 1] > value[i, j] + data[i, j]:
            value[i, j + 1] = value[i, j] + data[i, j]
            to_check.append((i, j + 1))
    return value[0, 0]


def task1():
    data = process_data(util.load_data("input/day15.txt"))
    print(find_safest_path(data))


def task2():
    data = process_data(util.load_data("input/day15.txt"))
    data = tile_map(data)
    print(opt_find_safest_path(data))
