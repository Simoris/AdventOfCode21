import util
import numpy as np


def process_data(data):
    return np.array([[int(y) for y in x] for x in data])


def get_gamma(data):
    n = len(data[0])
    m = len(data)

    c = np.ones(m)@data

    gamma = 0
    factor = 1
    for x in reversed(c):
        if x > m/2:
            gamma += factor
        factor *= 2
    return gamma


def get_power_consumption(data):
    n = len(data[0])
    gamma = get_gamma(data)
    eps = pow(2, n) - gamma - 1
    return gamma*eps


def get_ogr(data):
    m = len(data)
    candidates = np.arange(m)
    for i in range(len(data[0])):
        keep = 0
        if np.sum(data[candidates, i]) >= len(data[candidates, i])/2:
            keep = 1
        candidates = candidates[data[candidates, i] == keep]

    ogr_bin = data[candidates[0]]
    ogr = 0
    factor = 1
    for x in reversed(ogr_bin):
        ogr += x*factor
        factor *= 2
    return ogr


def get_csr(data):
    m = len(data)
    candidates = np.arange(m)
    for i in range(len(data[0])):
        keep = 1
        if np.sum(data[candidates, i]) >= len(data[candidates, i]) / 2:
            keep = 0
        if not (data[candidates, i] == keep).any():
            break
        candidates = candidates[data[candidates, i] == keep]

    csr_bin = data[candidates[0]]
    csr = 0
    factor = 1
    for x in reversed(csr_bin):
        csr += x * factor
        factor *= 2
    return csr


def task1():
    report = util.load_data("input/day3.txt")
    print(get_power_consumption(process_data(report)))


def task2():
    report = util.load_data("input/day3.txt")
    report = process_data(report)
    ogr = get_ogr(report)
    csr = get_csr(report)
    print(ogr*csr)
