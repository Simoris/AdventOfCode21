import util


def get_pos(commands):
    x = 0
    y = 0
    for c in commands:
        [dir, n] = c.split(" ")
        n = int(n)
        if dir == "up":
            y -= n
        elif dir == "down":
            y += n
        elif dir == "forward":
            x += n
        else:
            print("Error")
    return x, y


def get_aimed_pos(commands):
    x = 0
    y = 0
    aim = 0
    for c in commands:
        [dir, n] = c.split(" ")
        n = int(n)
        if dir == "up":
            aim -= n
        elif dir == "down":
            aim += n
        elif dir == "forward":
            x += n
            y += aim*n
        else:
            print("Error")
    return x, y


def task1():
    commands = util.load_data("input/day2.txt")
    x, y = get_pos(commands)
    print(x*y)


def task2():
    commands = util.load_data("input/day2.txt")
    x, y = get_aimed_pos(commands)
    print(x*y)
