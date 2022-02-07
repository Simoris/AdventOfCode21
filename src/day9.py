import util
import numpy as np


def process_data(data):
    return np.array([[int(num) for num in line] for line in data])


def get_bassin_map(raw_data):
    return np.array([[int(num) for num in line] for line in raw_data]) == 9


def find_low_points(data):
    mask = np.full_like(data, False, dtype=bool)
    x, y = data.shape
    for i in range(x):
        for j in range(y):
            if (i == 0) or (data[i, j] < data[i - 1, j]):
                if (j == 0) or (data[i, j] < data[i, j - 1]):
                    if (i == x - 1) or (data[i, j] < data[i + 1, j]):
                        if (j == y - 1) or (data[i, j] < data[i, j + 1]):
                            mask[i, j] = True
    return mask


def sum_risk_levels(data, mask):
    return np.ma.array(data=(data + 1), mask=np.invert(mask)).sum()


def find_bassins(data, low_point):
    bassins = np.full_like(data, 0)
    x, y = data.shape
    c = 1
    for i in range(x):
        for j in range(y):
            if data[i, j] == 9:
                bassins[i, j] = -1
            if low_point[i, j]:
                bassins[i, j] = c
                c += 1

    while (bassins == 0).any():
        end_loop = True
        for i in range(x):
            for j in range(y):
                if bassins[i, j] == 0:
                    # Look for neighbouring positive value to add
                    if bassins[i - 1, j] > 0:
                        bassins[i, j] = bassins[i - 1, j]
                    elif bassins[i + 1, j] > 0:
                        bassins[i, j] = bassins[i + 1, j]
                    elif bassins[i, j - 1] > 0:
                        bassins[i, j] = bassins[i, j - 1]
                    elif bassins[i, j + 1] > 0:
                        bassins[i, j] = bassins[i, j + 1]
    return bassins


def get_bassin_sizes(bassins):
    n = np.max(bassins)
    sizes = np.zeros(n)
    for i in range(n):
        sizes[i] = (bassins == i + 1).sum()
    return sizes


def task1():
    data = process_data(util.load_data("input/day9.txt"))
    mask = find_low_points(data)
    print(sum_risk_levels(data, mask))


def task2():
    data = process_data(util.load_data("input/day9.txt"))
    # Surround with 9s to make border checks unnecessary
    x, y = data.shape
    data = np.vstack((np.full(y + 2, 9), np.hstack((np.full((x, 1), 9), data, np.full((x, 1), 9))), np.full(y + 2, 9)))
    low_points = find_low_points(data)
    bassins = find_bassins(data, low_points)
    bassin_sizes = get_bassin_sizes(bassins)
    b = sorted(bassin_sizes, reverse=True)
    print(b[0]*b[1]*b[2])
