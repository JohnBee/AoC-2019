import itertools
import copy

def read_input():
    with open("Day16-input.txt") as f:
        i = f.readline().strip()
        return str_to_list(i)


def unpack(list_of_lists):
    if not list_of_lists:
        return []
    else:
        return list_of_lists[0] + unpack(list_of_lists[1:])

def fft(in_pattern, phases):
    base_pattern = [0, 1, 0, -1]
    res = in_pattern
    for i in range(0, phases):
        print("Phase {}".format(i))
        layer = []
        for passes in range(0, len(in_pattern)):
            p = unpack([[a]*(passes+1) for a in base_pattern])
            pattern = itertools.cycle(p)
            next(pattern)
            a = sum([i*next(pattern) for i in res])
            layer.append(int(str(abs(a))[-1]))
        res = copy.deepcopy(layer)
    return res


def get_next_pattern(base_pattern, pos, passes=0):
    # pass 0 len = 4
    # pass 1 len = 8
    # pass 2 len = 12
    # pos // (passes + 1)
    pos = pos // (passes + 1)
    return base_pattern[pos % len(base_pattern)]


def fast_fft(in_pattern, phases):
    base_pattern = [0, 1, 0, -1]
    res = in_pattern
    res.reverse()
    for i in range(0, phases):
        print("Phase {}".format(i))
        res = list(itertools.accumulate(res))
        layer = []
        for a in res:
            layer.append(int(str(abs(a))[-1]))

        res = copy.deepcopy(layer)
    res.reverse()
    return res


def str_to_list(in_string):
    return list(map(int, list(in_string)))


def load_test1():
    return str_to_list("12345678")


def load_test2():
    return str_to_list("80871224585914546619083218645595")


def load_test3():
    return str_to_list("03036732577212944063491565474664")

def load_test4():
    return str_to_list("02935109699940807407585447034323")

def part2():
    part2_input = read_input()*10000
    location = int("".join(map(str, part2_input[0:7])))
    part2_small = part2_input[location:]
    # part2_input = load_test1()
    # location = 0
    # part2_small = part2_input[location:]

    print(location)
    print("Running fft...")

    final = fast_fft(part2_small, 100)
    print(final[0:8])
    #print("Part2 {}".format(final[location:location+8]))

def part1():
    in_signal = read_input()
    # in_signal = load_test1()
    out = fft(in_signal, 100)
    print("Part1 {}".format(out[0:8]))

if __name__ == "__main__":
    # part1()
    part2()

