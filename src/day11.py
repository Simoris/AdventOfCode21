import util
import numpy as np


def process_data(data):
    return np.array([[int(c) for c in line] for line in data], dtype=float)


def step(data):
    x, y = data.shape
    n_flashes = 0
    data += 1
    while (data > 9).any():
        for i in range(x):
            for j in range(y):
                if data[i, j] > 9:
                    data[i, j] = - np.inf
                    n_x = 3 - max(i - x + 2, 0)
                    n_y = 3 - max(j - y + 2, 0)
                    data[:i + 2, : j + 2][-n_x:, -n_y:] += 1
                    n_flashes += 1

    data[data == -np.inf] = 0
    return data, n_flashes


def make_n_steps(data, n):
    num_flashes = 0
    for i in range(n):
        data, n_flashes = step(data)
        num_flashes += n_flashes
    return data, num_flashes


def first_joint_flash(data):
    i = 1
    while True:
        data, n = step(data)
        if n == data.size:
            break
        i += 1
    return i


def task1():
    data = process_data(util.load_data("input/day11.txt"))
    _, n = make_n_steps(data, 100)
    print(n)


def task2():
    data = process_data(util.load_data("input/day11.txt"))
    print(first_joint_flash(data))
