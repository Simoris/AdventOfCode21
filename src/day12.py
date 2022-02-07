import util


def is_valid(path, next_node):
    valid = True
    if next_node.islower():
        for node in path:
            if node == next_node:
                valid = False
                break
    return valid


def has_lower_duplicate(path):
    path = [node for node in path[1:] if node.islower()]
    return len(path) != len(set(path))


def is_valid2(path, next_node):
    if next_node == "start":
        return False
    if not has_lower_duplicate(path):
        return True
    if next_node.islower():
        for node in path:
            if node == next_node:
                return False
    return True


def continue_path(data, path, validator=is_valid):
    last_node = path[-1]
    paths = []
    for line in data:
        if last_node in line:
            [node1, node2] = line.split('-')
            if node1 == last_node:
                next_node = node2
            elif node2 == last_node:
                next_node = node1
            else:
                print("Error")

            if validator(path, next_node):
                paths.append(path + [next_node])
    return paths


def check_paths_finished(paths):
    unfinished_paths = []
    finished_paths = []
    for path in paths:
        if path[-1] == "end":
            finished_paths.append(path)
        else:
            unfinished_paths.append(path)
    return unfinished_paths, finished_paths


def find_paths(data, validator=is_valid):
    paths = [["start"]]
    finished_paths = []
    while len(paths) > 0:
        new_paths = []
        for path in paths:
            new_paths += continue_path(data, path, validator)
        paths, new_paths = check_paths_finished(new_paths)
        finished_paths += new_paths
    return finished_paths


def task1():
    data = util.load_data("input/day12.txt")
    paths = find_paths(data)
    print(len(paths))


def task2():
    data = util.load_data("input/day12.txt")
    paths = find_paths(data, is_valid2)
    print(len(paths))
