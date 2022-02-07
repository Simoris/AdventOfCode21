import util


class Deterministic_Die:
    def __init__(self, size=100):
        self.size = size
        self.rolls = 0
        self.last_roll = 0

    def roll(self):
        self.last_roll += 1
        self.rolls += 1
        if self.last_roll > self.size:
            self.last_roll = 1
        return self.last_roll

    def roll_and_sum(self, n):
        ret = 0
        for _ in range(n):
            ret += self.roll()
        return ret


freq = [0, 0, 0, 1, 3, 6, 7, 6, 3, 1]


def dirac_turn2(p1, p2, s1, s2, max_score, turns=0):
    while p1 > 10:
        p1 -= 10
    s1 += p1
    if s1 >= max_score:
        return 1, 0
    w1, w2 = 0, 0
    for i in range(3, 10):
        a, b = dirac_turn1(p1, p2 + i, s1, s2, max_score, turns + 1)
        w1 += a*freq[i]
        w2 += b*freq[i]
    return w1, w2


def dirac_turn1(p1, p2, s1, s2, max_score, turns=0):
    while p2 > 10:
        p2 -= 10
    s2 += p2
    if s2 >= max_score:
        return 0, 1
    w1, w2 = 0, 0
    for i in range(3, 10):
        a, b = dirac_turn2(p1 + i, p2, s1, s2, max_score, turns + 1)
        w1 += a*freq[i]
        w2 += b*freq[i]
    return w1, w2


def task1():
    data = util.load_data("input/day21.txt")
    p1 = int(data[0][-1])
    p2 = int(data[1][-1])
    s1, s2 = 0, 0

    dice = Deterministic_Die()
    while True:
        p1 += dice.roll_and_sum(3)
        while p1 > 10:
            p1 -= 10
        s1 += p1
        if s1 >= 1000:
            break

        p2 += dice.roll_and_sum(3)
        while p2 > 10:
            p2 -= 10
        s2 += p2
        if s2 >= 1000:
            break

    print(dice.rolls*min(s1, s2))


def task2():
    data = util.load_data("input/day21.txt")
    p1 = int(data[0][-1])
    p2 = int(data[1][-1])

    w1, w2 = dirac_turn1(p1, p2, 0, -p2, 21)
    print(max(w1, w2))
