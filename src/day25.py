import util
import numpy as np


def step(mat):
    x, y = mat.shape
    new_mat = mat.copy()
    for i in range(x):
        for j in range(y):
            if mat[i, j] == '>':
                jplus = j + 1 if j < y - 1 else 0
                if mat[i, jplus] == '.':
                    new_mat[i, j] = '.'
                    new_mat[i, jplus] = '>'
    mat = new_mat.copy()
    for i in range(x):
        for j in range(y):
            if mat[i, j] == 'v':
                iplus = i + 1 if i < x - 1 else 0
                if mat[iplus, j] == '.':
                    new_mat[i, j] = '.'
                    new_mat[iplus, j] = 'v'
    return new_mat


def task1():
    data = util.load_data("input/day25.txt")
    data = [[x for x in line] for line in data]
    data = np.array(data)
    print(data)

    i = 1
    while True:
        new_data = step(data)
        if (new_data == data).all():
            print(i)
            return
        data = new_data
        i += 1
