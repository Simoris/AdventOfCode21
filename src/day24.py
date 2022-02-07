import util

name2pos = {'w': 0, 'x': 1, 'y': 2, 'z': 3}
pos2name = {0: 'w', 1: 'x', 2: 'y', 3: 'z'}


class ALU:
    def __init__(self):
        self.var = [0, 0, 0, 0]

    def reset(self):
        self.var = [0, 0, 0, 0]

    def was_valid(self):
        return self.var[3] == 0

    def parse_line(self, line, inputs):
        line = line.split(' ')
        a = name2pos[line[1]]
        if line[0] == 'inp':
            self.var[a] = inputs[0]
            return True
        else:
            try:
                b = int(line[2])
            except ValueError:
                b = self.var[name2pos[line[2]]]

            if line[0] == 'add':
                self.var[a] += b
            elif line[0] == 'mul':
                self.var[a] *= b
            elif line[0] == 'div':
                self.var[a] = int(self.var[a]/b)
            elif line[0] == 'mod':
                self.var[a] %= b
            elif line[0] == 'eql':
                self.var[a] = 1 if (self.var[a] == b) else 0
            return False

    def search_highest_valid(self, instructions):
        for i in range(len(instructions)):
            line = instructions[i]
            if line[:3] == 'inp':
                var = self.var.copy()
                for j in range(9, 0, -1):
                    self.var = var.copy()
                    self.parse_line(line, [j])
                    valid, nums = self.search_highest_valid(instructions[i+1:])
                    if valid:
                        return True, nums + [j]
                return False, []
            else:
                self.parse_line(line, None)
        return self.was_valid(), []

    def evaluate(self, instructions, inputs):
        for line in instructions:
            if self.parse_line(line, inputs):
                inputs.pop(0)


class ALUh:
    def __init__(self):
        self.div4 = [1, 1, 1, 1, 26, 1, 1, 26, 1, 26, 26, 26, 26, 26]
        self.add5 = [14, 13, 15, 13, -2, 10, 13, -15, 11, -9, -9, -7, -4, -6]
        self.add15 = [0, 12, 14, 0, 3, 15, 11, 12, 1, 12, 3, 10, 14, 12]
        self.bad_states = set()

    def step(self, inp, z_in, i):
        w = inp
        x = z_in % 26
        z = int(z_in / self.div4[i])
        x += self.add5[i]
        x = 0 if x == w else 1
        y = 25*x + 1
        z *= y
        y = w + self.add15[i]
        z += y*x
        return z

    def search_highest_valid(self, depth, z_in):
        if hash((depth, z_in)) in self.bad_states:
            return False, []

        for inp in range(9, 0, -1):
            z = self.step(inp, z_in, depth)
            if depth == 13 and z == 0:
                return True, [inp]
            if depth < 13:
                b, in_list = self.search_highest_valid(depth + 1, z)
                if b:
                    in_list.append(inp)
                    return b, in_list
        self.bad_states.add(hash((depth, z_in)))
        return False, []

    def search_lowest_valid(self, depth, z_in):
        if hash((depth, z_in)) in self.bad_states:
            return False, []

        for inp in range(1, 10):
            z = self.step(inp, z_in, depth)
            if depth == 13 and z == 0:
                return True, [inp]
            if depth < 13:
                b, in_list = self.search_lowest_valid(depth + 1, z)
                if b:
                    in_list.append(inp)
                    return b, in_list
        self.bad_states.add(hash((depth, z_in)))
        return False, []


def task1_old():
    data = util.load_data("input/day24.txt")
    alu = ALU()
    valid, num = alu.search_highest_valid(data)
    print(valid)
    print(num)


def test():
    data = util.load_data("input/day24.txt")
    alu = ALU()
    alu.evaluate(data, [15, 10])
    print(alu.var)


def task1():
    a = ALUh()
    b, l = a.search_highest_valid(0, 0)
    print(b)
    print(l)


def task2():
    a = ALUh()
    b, l = a.search_lowest_valid(0, 0)
    print(b)
    print(l)
