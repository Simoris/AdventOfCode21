import util
import numpy as np


def parse_line(line):
    line = line.split(' ')
    flip = (line[0] == 'on')
    line = line[1].split(',')
    x = line[0][2:].split('..')
    y = line[1][2:].split('..')
    z = line[2][2:].split('..')
    min_cord = [int(x[0]), int(y[0]), int(z[0])]
    max_cord = [int(x[1]), int(y[1]), int(z[1])]
    return flip, min_cord, max_cord


def evaluate_cube(min_cord, max_cord, instructions):
    cube = np.zeros(max_cord - min_cord + [1, 1, 1], dtype=bool)
    offset = -min_cord
    for line in instructions:
        state, l_min, l_max = line
        l_min += offset
        l_max += offset + [1, 1, 1]
        cube[l_min[0]:l_max[0], l_min[1]:l_max[1], l_min[2]:l_max[2]] = state
    return cube


def size_full_cube(instructions):
    size = 0
    for i in range(len(instructions)):
        state, l_min, l_max = instructions[i]
        if state:
            new_instr = instructions[i:]
            new_instr[1:] = [(False, l_min2, l_max2) for (_, l_min2, l_max2) in new_instr[1:]]
            cube = evaluate_cube(np.array(l_min), np.array(l_max), new_instr)
            size += np.sum(cube)
    return size


class Cuboid:
    def __init__(self, x0, x1, y0, y1, z0, z1, state):
        self.x0 = x0
        self.x1 = x1
        self.y0 = y0
        self.y1 = y1
        self.z0 = z0
        self.z1 = z1
        self.state = state

    @classmethod
    def from_string(cls, line):
        line = line.split(' ')
        state = (line[0] == 'on')
        line = line[1].split(',')
        [x0, x1] = line[0][2:].split('..')
        [y0, y1] = line[1][2:].split('..')
        [z0, z1] = line[2][2:].split('..')
        return Cuboid(int(x0), int(x1), int(y0), int(y1), int(z0), int(z1), state)

    def get_size(self):
        r = (self.x1-self.x0+1)*(self.y1-self.y0+1)*(self.z1-self.z0+1)
        return r if self.state else -r

    def intersect(self, other):
        state = not self.state
        x0 = max(self.x0, other.x0)
        x1 = min(self.x1, other.x1)
        y0 = max(self.y0, other.y0)
        y1 = min(self.y1, other.y1)
        z0 = max(self.z0, other.z0)
        z1 = min(self.z1, other.z1)
        if x0 > x1 or y0 > y1 or z0 > z1:
            return None
        return Cuboid(x0, x1, y0, y1, z0, z1, state)


def measure_core(instructions):
    cores = []
    for line in instructions:
        c = Cuboid.from_string(line)
        to_add = []
        for core in cores:
            core = core.intersect(c)
            if core is not None:
                to_add.append(core)
        cores += to_add
        if c.state:
            cores.append(c)

    return sum([core.get_size() for core in cores])


def task1():
    data = util.load_data("input/day22.txt")
    data = [parse_line(line) for line in data]
    cube = evaluate_cube(np.array([-50, -50, -50]), np.array([50, 50, 50]), data)
    print(np.sum(cube))


def task2():
    data = util.load_data("input/day22.txt")
    print(measure_core(data))
