import util
import numpy as np


def find_corrupted_lines(data):
    corrupted = []
    for line in data:
        corrupted.append(-1)
        stack = []
        for i, c in enumerate(line):
            if (c == '(') or (c == '[') or (c == '<') or (c == '{'):
                stack.append(c)
            else:
                t = stack[-1] + c
                if (t == '()') or (t == '[]') or (t == '<>') or (t == '{}'):
                    stack.pop()
                else:
                    corrupted[-1] = i
                    break

    return corrupted


def compute_tses(data, corrupted):
    score = 0
    for line, cor in zip(data, corrupted):
        if cor == -1:
            continue
        if line[cor] == ')':
            score += 3
        elif line[cor] == ']':
            score += 57
        elif line[cor] == '}':
            score += 1197
        elif line[cor] == '>':
            score += 25137
    return score


def discard_corrupted(data, corrupted):
    for i in reversed(range(len(corrupted))):
        if corrupted[i] != -1:
            del data[i]
    return data


def autocomplete(data):
    scores = []
    for line in data:
        stack = []
        for i, c in enumerate(line):
            if (c == '(') or (c == '[') or (c == '<') or (c == '{'):
                stack.append(c)
            else:
                t = stack[-1] + c
                if (t == '()') or (t == '[]') or (t == '<>') or (t == '{}'):
                    stack.pop()
                else:
                    print('Error')
                    break

        score = 0
        for c in reversed(stack):
            score *= 5
            if c == '(':
                score += 1
            elif c == '[':
                score += 2
            elif c == '{':
                score += 3
            elif c == '<':
                score += 4
        scores.append(score)

    return scores


def task1():
    data = util.load_data("input/day10.txt")
    corrupted = find_corrupted_lines(data)
    print(compute_tses(data, corrupted))


def task2():
    data = util.load_data("input/day10.txt")
    corrupted = find_corrupted_lines(data)
    data = discard_corrupted(data, corrupted)
    scores = np.array(autocomplete(data))
    print(np.median(scores))
