import util
from functools import reduce
import json
import math
from copy import deepcopy


class Snailfish:
    def __init__(self, left, right, parent=None):
        self.left = left
        self.right = right
        self.parent = parent
        self.final = isinstance(left, int) & isinstance(right, int)

    @classmethod
    def parse_from_list(cls, input_list):
        if isinstance(input_list, list):
            [left, right] = input_list
            return cls(Snailfish.parse_from_list(left), Snailfish.parse_from_list(right))
        else:
            return input_list

    def set_parents(self, parent=None):
        self.parent = parent
        if not isinstance(self.left, int):
            self.left.set_parents(self)
        if not isinstance(self.right, int):
            self.right.set_parents(self)

    def __explode_left(self, value, caller):
        if caller == self.left:
            if self.parent is None:
                return
            self.parent.__explode_left(value, self)
        elif caller == self.right:
            if isinstance(self.left, int):
                self.left += value
            else:
                self.left.__explode_left(value, self)
        elif caller == self.parent:
            if isinstance(self.right, int):
                self.right += value
            else:
                self.right.__explode_left(value, self)

    def __explode_right(self, value, caller):
        if caller == self.right:
            if self.parent is None:
                return
            self.parent.__explode_right(value, self)
        elif caller == self.left:
            if isinstance(self.right, int):
                self.right += value
            else:
                self.right.__explode_right(value, self)
        elif caller == self.parent:
            if isinstance(self.left, int):
                self.left += value
            else:
                self.left.__explode_right(value, self)

    def __exploded_this(self, caller):
        if caller == self.left:
            self.left = 0
            if isinstance(self.right, int):
                self.final = True
        elif caller == self.right:
            self.right = 0
            if isinstance(self.left, int):
                self.final = True
        else:
            print("Error")

    def __reduce_explode(self, depth=0):
        if self.final:
            if depth >= 4:
                self.parent.__explode_right(self.right, self)
                self.parent.__explode_left(self.left, self)
                self.parent.__exploded_this(self)
                return True
            return False
        else:
            if (not isinstance(self.left, int)) and self.left.__reduce_explode(depth + 1):
                return True
            else:
                return (not isinstance(self.right, int)) and self.right.__reduce_explode(depth + 1)

    def __reduce_split(self):
        if isinstance(self.left, int):
            if self.left >= 10:
                self.left = Snailfish(math.floor(self.left/2), math.ceil(self.left/2), self)
                self.final = False
                return True
        else:
            if self.left.__reduce_split():
                return True
        if isinstance(self.right, int):
            if self.right >= 10:
                self.right = Snailfish(math.floor(self.right/2), math.ceil(self.right/2), self)
                self.final = False
                return True
        else:
            return self.right.__reduce_split()
        return False

    def reduce(self):
        while self.__reduce_explode() or self.__reduce_split():
            pass

    def __add__(self, other):
        result = Snailfish(self, other)
        self.parent = result
        other.parent = result
        result.reduce()
        return result

    def get_magnitude(self):
        if type(self.left) == type(self):
            left_m = self.left.get_magnitude()
        else:
            left_m = self.left
        if type(self.right) == type(self):
            right_m = self.right.get_magnitude()
        else:
            right_m = self.right
        return 3 * left_m + 2 * right_m


def task1():
    # Parse and format data
    data = util.load_data("input/day18.txt")
    data = [Snailfish.parse_from_list(json.loads(line)) for line in data]
    for point in data:
        point.set_parents()

    # Actual task
    total = reduce(lambda a, b: a + b, data)
    print(total.get_magnitude())


def task2():
    # Parse and format data
    data = util.load_data("input/day18.txt")
    data = [Snailfish.parse_from_list(json.loads(line)) for line in data]
    for point in data:
        point.set_parents()

    max_magnitude = 0
    for x in data:
        for y in data:
            if x != y:
                max_magnitude = max((deepcopy(x) + deepcopy(y)).get_magnitude(), max_magnitude)

    print(max_magnitude)
