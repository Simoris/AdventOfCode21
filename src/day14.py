import util


def generate_insertion_dict(insertion):
    i_dict = dict()
    for line in insertion:
        i_dict[line[:2]] = line[6]
    return i_dict


def generate_counting_dict(insertion, polymer):
    c_dict = dict()
    for line in insertion:
        c_dict[line[:2]] = 0

    old_char = polymer[0]
    for new_char in polymer[1:]:
        c_dict[old_char + new_char] += 1
        old_char = new_char
    return c_dict


def insert(polymer, insertion):
    old_char = polymer[0]
    new_polymer = old_char
    for new_char in polymer[1:]:
        # Insert
        key = old_char + new_char
        new_polymer += insertion[key]
        # Continue
        new_polymer += new_char
        old_char = new_char
    return new_polymer


def insert_n(polymer, insertion, n):
    for i in range(n):
        polymer = insert(polymer, insertion)
    return polymer


def counting_step(c_dict, i_dict):
    new_c_dict = dict()
    for key in i_dict:
        new_c_dict[key] = 0
    for key in c_dict:
        v = i_dict[key]
        key1 = key[0] + v
        key2 = v + key[1]
        new_c_dict[key1] += c_dict[key]
        new_c_dict[key2] += c_dict[key]
    return new_c_dict


def counting_step_n(c_dict, i_dict, n):
    for _ in range(n):
        c_dict = counting_step(c_dict, i_dict)
    return c_dict


def task1():
    data = util.load_data("input/day14.txt")
    polymer = data[0]
    insertion = generate_insertion_dict(data[2:])
    polymer = insert_n(polymer, insertion, 10)

    frequency_dict = dict()
    visited = set()
    for element in polymer:
        if element in visited:
            frequency_dict[element] = frequency_dict[element] + 1
        else:
            frequency_dict[element] = 1
            visited.add(element)
    frequencies = frequency_dict.values()
    print(max(frequencies) - min(frequencies))


def task2():
    data = util.load_data("input/day14.txt")
    polymer = data[0]
    count = generate_counting_dict(data[2:], polymer)
    insertion = generate_insertion_dict(data[2:])

    # Do steps
    count = counting_step_n(count, insertion, 40)

    # Count
    frequency_dict = dict()
    visited = set()
    for key in count:
        if key[0] in visited:
            frequency_dict[key[0]] += count[key]
        else:
            frequency_dict[key[0]] = count[key]
            visited.add(key[0])

        if key[1] in visited:
            frequency_dict[key[1]] += count[key]
        else:
            frequency_dict[key[1]] = count[key]
            visited.add(key[1])
    frequency_dict[polymer[0]] += 1
    frequency_dict[polymer[-1]] += 1
    frequencies = frequency_dict.values()
    print((max(frequencies) - min(frequencies))/2)
