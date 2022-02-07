import math


def load_data():
    file = open("input/day1.txt", "r")
    data = file.read()
    return data


def count_increases(data):
    old_num = math.inf
    count = 0
    for num in data.split('\n'):
        if num == '':
            continue
        num = int(num)
        if num > old_num:
            count += 1
        old_num = num
    return count


def count_offset_increases(data, offset):
    old_nums = [int(num) for num in data.split('\n')[:-1]]
    new_nums = old_nums[offset:]
    old_nums = old_nums[:-offset]

    count = 0
    for old, new in zip(old_nums, new_nums):
        if new > old:
            count += 1
    return count


def task1():
    print(count_increases(load_data()))


def task2():
    print(count_offset_increases(load_data(), 3))
