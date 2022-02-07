import util
import numpy as np
from copy import deepcopy
from queue import PriorityQueue
from functools import total_ordering
import hashlib

let2num = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
let2pos = {'A': 2, 'B': 4, 'C': 6, 'D': 8}
num2let = {0: 'A', 1: 'B', 2: 'C', 3: 'D'}


class State:
    def __init__(self, row, columns):
        self.row = row.copy()
        self.columns = [[columns[0][0], columns[0][1]], [columns[1][0], columns[1][1]], [columns[2][0], columns[2][1]], [columns[3][0], columns[3][1]]]

    def deepcopy_columns(self):
        return [[self.columns[0][0], self.columns[0][1]], [self.columns[1][0], self.columns[1][1]], [self.columns[2][0], self.columns[2][1]], [self.columns[3][0], self.columns[3][1]]]

    def deepcopy_self(self):
        row = self.row.copy()
        columns = self.deepcopy_columns()
        return State(row, columns)

    def find_follow_states(self):
        nodes = []
        dists = []
        for i in range(11):
            if self.row[i] != '.':
                # Check whether you can move it into final column
                a = min(i, let2pos[self.row[i]])
                b = max(i, let2pos[self.row[i]])
                if a == i:
                    a += 1
                else:
                    b -= 1
                if (np.array(self.row[a:b]) == '.').all():
                    if self.columns[let2num[self.row[i]]] == ['.', '.']:
                        row = self.row.copy()
                        row[i] = '.'
                        columns = self.deepcopy_columns()
                        columns[let2num[self.row[i]]][1] = self.row[i]
                        nodes.append(State(row, columns))
                        dists.append(np.power(10, let2num[self.row[i]])*(np.abs(i - let2pos[self.row[i]]) + 2))
                        return nodes, dists
                    elif self.columns[let2num[self.row[i]]] == ['.', self.row[i]]:
                        row = self.row.copy()
                        row[i] = '.'
                        columns = self.deepcopy_columns()
                        columns[let2num[self.row[i]]][0] = self.row[i]
                        nodes.append(State(row, columns))
                        dists.append(np.power(10, let2num[self.row[i]])*(np.abs(i - let2pos[self.row[i]]) + 1))
                        return nodes, dists
        for i in range(4):
            # Check whether you can move out an element from a column
            if self.columns[i][0] != num2let[i] or self.columns[i][1] != num2let[i]:
                if self.columns[i][0] != '.':
                    j = let2pos[num2let[i]] + 1
                    while j < 11 and self.row[j] == '.':
                        if j not in [2, 4, 6, 8]:
                            row = self.row.copy()
                            row[j] = self.columns[i][0]
                            columns = self.deepcopy_columns()
                            columns[i][0] = '.'
                            nodes.append(State(row, columns))
                            dists.append(np.power(10, let2num[self.columns[i][0]])*(np.abs(j - let2pos[num2let[i]]) + 1))
                        j += 1
                    j = let2pos[num2let[i]] - 1
                    while j >= 0 and self.row[j] == '.':
                        if j not in [2, 4, 6, 8]:
                            row = self.row.copy()
                            row[j] = self.columns[i][0]
                            columns = self.deepcopy_columns()
                            columns[i][0] = '.'
                            nodes.append(State(row, columns))
                            dists.append(np.power(10, let2num[self.columns[i][0]]) * (np.abs(j - let2pos[num2let[i]]) + 1))
                        j -= 1
                elif self.columns[i][1] != '.' and self.columns[i][1] != num2let[i]:
                    j = let2pos[num2let[i]] + 1
                    while j < 11 and self.row[j] == '.':
                        if j not in [2, 4, 6, 8]:
                            row = self.row.copy()
                            row[j] = self.columns[i][1]
                            columns = self.deepcopy_columns()
                            columns[i][1] = '.'
                            nodes.append(State(row, columns))
                            dists.append(np.power(10, let2num[self.columns[i][1]]) * (np.abs(j - let2pos[num2let[i]]) + 2))
                        j += 1
                    j = let2pos[num2let[i]] - 1
                    while j >= 0 and self.row[j] == '.':
                        if j not in [2, 4, 6, 8]:
                            row = self.row.copy()
                            row[j] = self.columns[i][1]
                            columns = self.deepcopy_columns()
                            columns[i][1] = '.'
                            nodes.append(State(row, columns))
                            dists.append(np.power(10, let2num[self.columns[i][1]]) * (np.abs(j - let2pos[num2let[i]]) + 2))
                        j -= 1
        return nodes, dists

    @classmethod
    def from_input_string(cls, data):
        row = np.full(11, '.')
        columns = [['B', 'D'], ['A', 'C'], ['A', 'B'], ['D', 'C']]
        return cls(row, columns)


@total_ordering
class State4:
    def __init__(self, row, columns):
        self.row = row.copy()
        self.columns = deepcopy(columns)

    def deepcopy_columns(self):  # TODO
        return deepcopy(self.columns)

    def deepcopy_self(self):
        row = self.row.copy()
        columns = self.deepcopy_columns()
        return State(row, columns)

    def find_follow_states(self):  # TODO?
        nodes = []
        dists = []
        for i in range(11):
            if self.row[i] != '.':
                # Check whether you can move it into final column
                a = min(i, let2pos[self.row[i]])
                b = max(i, let2pos[self.row[i]])
                if a == i:
                    a += 1
                else:
                    b -= 1
                if (np.array(self.row[a:b]) == '.').all():
                    if all([((x == '.') | (x == self.row[i])) for x in self.columns[let2num[self.row[i]]]]):
                        j = sum([x == '.' for x in self.columns[let2num[self.row[i]]]]) - 1
                        row = self.row.copy()
                        row[i] = '.'
                        columns = self.deepcopy_columns()
                        columns[let2num[self.row[i]]][j] = self.row[i]
                        nodes.append(State4(row, columns))
                        dists.append(np.power(10, let2num[self.row[i]])*(np.abs(i - let2pos[self.row[i]]) + j + 1))
        for i in range(4):
            # Check whether you can move out an element from a column
            if not all([((x == '.') | (x == num2let[i])) for x in self.columns[i]]):
                h = sum([x == '.' for x in self.columns[i]])

                j = let2pos[num2let[i]] + 1
                while j < 11 and self.row[j] == '.':
                    if j not in [2, 4, 6, 8]:
                        row = self.row.copy()
                        row[j] = self.columns[i][h]
                        columns = self.deepcopy_columns()
                        columns[i][h] = '.'
                        nodes.append(State4(row, columns))
                        dists.append(np.power(10, let2num[self.columns[i][h]]) * (np.abs(j - let2pos[num2let[i]]) + h + 1))
                    j += 1
                j = let2pos[num2let[i]] - 1
                while j >= 0 and self.row[j] == '.':
                    if j not in [2, 4, 6, 8]:
                        row = self.row.copy()
                        row[j] = self.columns[i][h]
                        columns = self.deepcopy_columns()
                        columns[i][h] = '.'
                        nodes.append(State4(row, columns))
                        dists.append(np.power(10, let2num[self.columns[i][h]]) * (np.abs(j - let2pos[num2let[i]]) + h + 1))
                    j -= 1
        return nodes, dists

    def a_star_helper(self):
        return 0  # TODO

    def is_final(self):
        return self.columns == [['A', 'A', 'A', 'A'], ['B', 'B', 'B', 'B'], ['C', 'C', 'C', 'C'], ['D', 'D', 'D', 'D']]

    def __eq__(self, other):
        return True

    def __le__(self, other):
        return True

    @property
    def state_hash(self):
        return hash((tuple([tuple(column) for column in self.columns]), tuple(self.row)))

    @staticmethod
    def dijkstra():
        row = np.full(11, '.')
        columns = [['B', 'D', 'D', 'D'], ['A', 'C', 'B', 'C'], ['A', 'B', 'A', 'B'], ['D', 'A', 'C', 'C']]
        state = State4(row, columns)

        q = PriorityQueue()
        visited = set()
        q.put((state.a_star_helper(), 0, state))
        while not q.empty():
            _, length, state = q.get()
            if state.state_hash not in visited:
                visited.add(state.state_hash)
                if state.is_final():
                    return length
                nodes, dists = state.find_follow_states()
                for node, dist in zip(nodes, dists):
                    q.put((length+dist+node.a_star_helper(), length+dist, node))
        return state


class Path:
    def __init__(self, states, length):
        self.states = states
        self.length = length

    def deepcopy_states(self):
        states = []
        for state in self.states:
            states.append(state.deepcopy_self())
        return states

    def get_length(self):
        return self.length

    def is_finished(self):
        return self.states[-1].columns == [['A', 'A'], ['B', 'B'], ['C', 'C'], ['D', 'D']]

    def quickest_finish(self):
        nodes, dists = self.states[-1].find_follow_states()
        min_length = np.inf
        path = None
        for node, dist in zip(nodes, dists):
            potential_path = Path.by_addition(self, node, dist)
            if not potential_path.is_finished():
                potential_path = potential_path.quickest_finish()
            if potential_path is None:
                continue
            length = potential_path.get_length()

            if length < min_length:
                min_length = length
                path = potential_path
        return path

    @classmethod
    def quickest_path(cls, init_state):
        return Path([init_state], 0).quickest_finish()

    @classmethod
    def by_addition(cls, path, state, dist):
        states = path.deepcopy_states()
        states.append(state)
        return cls(states, path.length + dist)


def task1():
    data = util.load_data("input/day23.txt")
    data = State.from_input_string(data)
    path = Path.quickest_path(data)
    print(path.get_length())


def task2():
    print(State4.dijkstra())
