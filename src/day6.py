import util


def get_data(path):
    raw_data = util.load_data(path)[0]
    raw_data = [int(x) for x in raw_data.split(',')]
    data = [0 for i in range(9)]
    for x in raw_data:
        data[x] += 1
    return data


def simulate_day(pop):
    pop[7] += pop[0]
    temp = pop[0]
    pop = pop[1:]
    pop.append(temp)
    return pop


def simulate_n_days(pop, n):
    for _ in range(n):
        pop = simulate_day(pop)
    return pop


def task1():
    data = get_data("input/day6.txt")
    end_pop = simulate_n_days(data, 80)
    print(sum(end_pop))


def task2():
    data = get_data("input/day6.txt")
    end_pop = simulate_n_days(data, 256)
    print(sum(end_pop))
