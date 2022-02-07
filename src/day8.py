import util


def process_data(data):
    return [[num.split(' ') for num in line.split(' | ')] for line in data]


def process_data_sorted_strings(data):
    return [[[''.join(sorted(elem)) for elem in num.split(' ')] for num in line.split(' | ')] for line in data]


def decode_line(line):
    #  Decode one line, return 4-digit number
    [data, number] = line
    let2num = {}
    num2let = {}
    for let in data:  # 1, 4, 7 & 0
        if len(let) == 2:
            let2num.update({let: 1})
            num2let.update({1: let})
        elif len(let) == 3:
            let2num.update({let: 7})
            num2let.update({7: let})
        elif len(let) == 4:
            let2num.update({let: 4})
            num2let.update({4: let})
        elif len(let) == 7:
            let2num.update({let: 8})
            num2let.update({8: let})

    data = [let for let in data if ((len(let) == 5) | (len(let) == 6))]
    for i in reversed(range(6)):  # 3
        let = data[i]
        if set(num2let[1]).issubset(set(let)):
            if len(let) == 5:
                let2num.update({let: 3})
                num2let.update({3: let})
                data.pop(i)
                break

    for i in reversed(range(5)):  # 9
        let = data[i]
        if set(num2let[3]).issubset(set(let)):
            if len(let) == 6:
                let2num.update({let: 9})
                num2let.update({9: let})
                data.pop(i)
                break

    for i in reversed(range(4)):  # 5 & 0
        let = data[i]
        if set(num2let[1]).issubset(set(let)):
            if len(let) == 6:
                let2num.update({let: 0})
                num2let.update({0: let})
                data.pop(i)
        if set(let).issubset(set(num2let[9])):
            if len(let) == 5:
                let2num.update({let: 5})
                num2let.update({5: let})
                data.pop(i)

    for i in reversed(range(2)):  # 2 & 6
        let = data[i]
        if len(let) == 6:
            let2num.update({let: 6})
            num2let.update({6: let})
            data.pop(i)
        elif len(let) == 5:
            let2num.update({let: 2})
            num2let.update({2: let})
            data.pop(i)

    # Decode
    number = [str(let2num[let]) for let in number]
    num = int(''.join(number))
    return num


def task1():
    data = process_data(util.load_data("input/day8.txt"))
    data = [[len(num) for num in line[1]] for line in data]
    data = [sum([1 for num in line if ((num == 2) | (num == 3) | (num == 4) | (num == 7))]) for line in data]
    print(sum(data))


def task2():
    data = process_data_sorted_strings(util.load_data("input/day8.txt"))
    nums = [decode_line(line) for line in data]
    print(sum(nums))
