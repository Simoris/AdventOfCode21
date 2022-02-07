import util
import numpy as np


def process_data(data):
    return np.array([int(x) for x in data[0].split(',')])


def get_optimal_point(positions):
    return np.median(positions)


def calculate_fuel_cost(positions, point):
    return np.abs(positions - point).sum()


def get_updated_optimal_point(positions):
    a = min(positions)
    b = max(positions)
    c_min = np.inf
    i_min = 0
    for i in range(a, b+1):
        c = calculate_updated_fuel_cost(positions, i)
        if c < c_min:
            c_min, i_min = c, i
    return i_min, c_min


def calculate_updated_fuel_cost(positions, point):
    dif = np.abs(positions - point)
    return (dif*(dif+1)/2).sum()


def task1():
    data = process_data(util.load_data("input/day7.txt"))
    point = get_optimal_point(data)
    cost = calculate_fuel_cost(data, point)
    print(cost)


def task2():
    data = process_data(util.load_data("input/day7.txt"))
    _, cost = get_updated_optimal_point(data)
    print(cost)
