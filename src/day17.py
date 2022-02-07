import util
import numpy as np


def parse_target(data):
    data = data[13:]
    [x, y] = data.split(', ')
    x = x[2:]
    y = y[2:]
    [x1, x2] = x.split('..')
    [y1, y2] = y.split('..')
    return int(x1), int(x2), int(y1), int(y2)


def x_is_valid(target, x):
    (x1, x2, _, _) = target
    traveled = 0
    if x1 < traveled < x2:
        return True
    for i in range(x):
        traveled += x - i
        if x1 <= traveled <= x2:
            return True
    return False


def steps_to_hit_x(target, x):
    (x1, x2, _, _) = target
    traveled = 0
    steps = []
    if x1 < traveled < x2:
        steps.append(0)
    for i in range(x):
        traveled += x - i
        if x1 <= traveled <= x2:
            steps.append(i+1)
    if x1 <= traveled <= x2:
        steps.append(np.inf)
    return steps


def hits_target(target, velocity):
    x_velo, y_velo = velocity
    steps = steps_to_hit_x(target, x_velo)
    (_, _, y1, y2) = target
    for step in steps:
        if step != np.inf:
            if y1 <= step*(y_velo - (step - 1)/2) <= y2:
                return True
        else:
            for step0 in range(steps[-2], 2*y_velo + np.abs(y1)):
                if y1 <= step0 * (y_velo - (step0 - 1) / 2) <= y2:
                    return True
    return False


def find_highest_y(velocity):
    _, y_velo = velocity
    return y_velo*(y_velo+1)/2


def generate_valid_x_velo(target):
    (x1, x2, _, _) = target
    max_x = max(abs(x1), abs(x2))
    max_sign = np.sign(x1 + x2)
    x_list = []

    for x in range(max_x + 1):
        if x_is_valid(target, x):
            x_list.append(max_sign*x)
    return x_list


def generate_valid_velo(target):
    (_, _, y1, y2) = target
    velos = []
    x_list = generate_valid_x_velo(target)
    for x_velo in x_list:
        y_list = []
        steps = steps_to_hit_x(target, x_velo)
        m_steps = max(steps)
        if m_steps == np.inf:
            y_ = -1 - y1
        else:
            y_ = int(np.round((y1 + m_steps*(m_steps-1)/2)/m_steps)) + 90  # TODO: That line seems to be bs, just add a high number ^^
        for y in range(y1 - 1, y_ + 1):
            if hits_target(target, (x_velo, y)):
                y_list.append(y)
        for y_velo in y_list:
            velos.append((x_velo, y_velo))
    return velos


def find_highest_trajectory_velo(target):
    velos = generate_valid_velo(target)
    max_y = -np.inf
    max_y_velo = (0, 0)
    for velo in velos:
        y = find_highest_y(velo)
        if y > max_y:
            max_y = y
            max_y_velo = velo
    return max_y_velo, max_y


def task1():
    data = util.load_data("input/day17.txt")[0]
    x1, x2, y1, y2 = parse_target(data)
    velo, max_y = find_highest_trajectory_velo((x1, x2, y1, y2))
    print(max_y)
    # This results in a wrong answer. The only case this code misses, is when the x-movement stops at some point.
    # It's easy to see, that in that case -1-y1 is the best y_velocity.


def task2():
    data = util.load_data("input/day17.txt")[0]
    x1, x2, y1, y2 = parse_target(data)
    velos = generate_valid_velo((x1, x2, y1, y2))
    print(velos)
    print(len(velos))
