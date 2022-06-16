import copy
import itertools

def read_input():
    with open("Day20-input.txt") as f:
        lines = f.readlines()
        for y in range(len(lines)):
            lines[y] = lines[y].rstrip("\n")
    for line in lines:
        print(line)
    return lines


class Warp:
    def __init__(self, point_a, point_b, label=""):
        self.A = point_a
        self.B = point_b
        self.label = label

    def __repr__(self):
        return (self.A, self.B)

    def __str__(self):
        return "W"

def parse_lines(lines):
    def in_map(x,y, lines):
        if 0 < x < len(lines[0]) and 0 < y < len(lines):
            return True
        return False
    def get_label(x, y, warp_locations):
        return [k for k in warp_locations if warp_locations[k] == (x,y)][0]
    warp_locations_1 = {}
    warp_locations_2 = {}
    ignore = []
    # identify warp squares
    for y in range(len(lines)):
        print(lines[y])
        for x in range(len(lines[y])):
            if lines[y][x].isalpha():
                # check surround space
                label = lines[y][x]

                if in_map(x+1, y, lines) and lines[y][x+1] == ".":
                    # A B .
                    label = lines[y][x-1] + label
                    if label in warp_locations_1:
                        warp_locations_2[label] = (x+1, y)
                    else:
                        warp_locations_1[label] = (x+1, y)
                    continue

                if in_map(x-1, y, lines) and lines[y][x-1] == ".":
                    # . A B
                    label = label + lines[y][x+1]
                    if label in warp_locations_1:
                        warp_locations_2[label] = (x-1, y)
                    else:
                        warp_locations_1[label] = (x-1, y)
                    continue

                if in_map(x, y+1, lines) and lines[y+1][x] == ".":
                    # A
                    # B <-
                    # .
                    label = lines[y-1][x] + label
                    if label in warp_locations_1:
                        warp_locations_2[label] = (x, y+1)
                    else:
                        warp_locations_1[label] = (x, y+1)
                    continue

                if in_map(x, y-1, lines) and lines[y-1][x] == ".":
                    # .
                    # A <-
                    # B
                    label = label + lines[y+1][x]
                    if label in warp_locations_1:
                        warp_locations_2[label] = (x, y-1)
                    else:
                        warp_locations_1[label] = (x, y-1)
                    continue
    print(warp_locations_1)
    print(warp_locations_2)
    world_map = {}
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            if lines[y][x] == "#":
                world_map[(x, y)] = "#"

            elif lines[y][x] == "." and (x, y) not in warp_locations_1.values() and (x, y) not in warp_locations_2.values():
                world_map[(x, y)] = "."

            elif lines[y][x] == "." and ((x, y) in warp_locations_1.values() or (x, y) in warp_locations_2.values()):
                if (x, y) in warp_locations_1.values() and get_label(x, y, warp_locations_1) not in warp_locations_2:
                    # must be start or end
                    label = get_label(x, y, warp_locations_1)
                    if label == "AA":
                        world_map[(x, y)] = "S"
                    if label == "ZZ":
                        world_map[(x, y)] = "E"

                elif (x, y) in warp_locations_1.values():
                    start = (x, y)
                    end = warp_locations_2[get_label(x, y, warp_locations_1)]
                    world_map[(x, y)] = Warp(start, end, label=get_label(x, y, warp_locations_1))

                elif (x, y) in warp_locations_2.values():
                    start = (x, y)
                    end = warp_locations_1[get_label(x, y, warp_locations_2)]
                    world_map[(x, y)] = Warp(start, end,get_label(x, y, warp_locations_2))
            else:
                # All chard, spaces to walls
                world_map[(x, y)] = "#"

    return world_map


def print_world_map(world_map):
    top_left = min(world_map)
    bot_right = max(world_map)
    for y in range(top_left[1], bot_right[1]):
        for x in range(top_left[0], bot_right[0]):
            print(world_map[(x, y)], end="")
        print()


def traverse_map(world_map):
    def get_next_states(state, world_map):
        possible_states = []
        if type(world_map[state]) == Warp:
            if world_map[state].A == state:
                possible_states.append(world_map[state].B)
            else:
                possible_states.append(world_map[state].A)

        # up
        if world_map[(state[0], state[1]-1)] != "#":
            possible_states.append((state[0], state[1]-1))
        # down
        if world_map[(state[0], state[1]+1)] != "#":
            possible_states.append((state[0], state[1]+1))
        # left
        if world_map[(state[0]-1, state[1])] != "#":
            possible_states.append((state[0]-1, state[1]))

        # right
        if world_map[(state[0]+1, state[1])] != "#":
            possible_states.append((state[0]+1, state[1]))

        return possible_states

    # find start and end
    start = [k for k in world_map if world_map[k] == "S"][0]
    end = [k for k in world_map if world_map[k] == "E"][0]
    print(start, end)

    # use BFS to explore the map
    visited = []
    queue = [[start]]
    while queue:
        path = queue.pop(0)
        vertex = path[-1]

        if vertex == end:
            return path

        if vertex not in visited:
            for new_state in get_next_states(vertex, world_map):
                new_path = list(path)
                new_path.append(new_state)
                queue.append(new_path)

            visited.append(vertex)


def distance_from_to(start, end, world_map):
    def get_next_states(state, world_map):
        possible_states = []

        # up
        if world_map[(state[0], state[1]-1)] != "#":
            possible_states.append((state[0], state[1]-1))
        # down
        if world_map[(state[0], state[1]+1)] != "#":
            possible_states.append((state[0], state[1]+1))
        # left
        if world_map[(state[0]-1, state[1])] != "#":
            possible_states.append((state[0]-1, state[1]))

        # right
        if world_map[(state[0]+1, state[1])] != "#":
            possible_states.append((state[0]+1, state[1]))

        return possible_states
    # do bfs with path
    # use BFS to explore the map
    if type(world_map[start]) == Warp and type(world_map[end]) == Warp and world_map[start].A == world_map[end].B:
        return 1


    visited = []
    queue = [[start]]
    while queue:
        path = queue.pop(0)
        vertex = path[-1]
        if vertex == end:
            return len(path)-1

        if vertex not in visited:
            for new_state in get_next_states(vertex, world_map):
                new_path = list(path)
                new_path.append(new_state)
                queue.append(new_path)

            visited.append(vertex)

    return None


def precalculate_distances(world_map):
    warps = []
    cache = {}
    for k in world_map:
        if type(world_map[k]) == Warp or world_map[k] in ["S","E"]:
            warps.append(k)
    combs = itertools.combinations(warps, 2)
    for s,e in combs:
        t = distance_from_to(s,e, world_map)
        if t:
            cache[(s,e)] = t

    return cache

def precalculate_inside_or_outside(world_map):
    warps = []
    cache = {}
    for k in world_map:
        if type(world_map[k]) == Warp or world_map[k] in ["S", "E"]:
            cache[k] = is_outside(k, world_map)
    return cache

def traverse_redux_part2(warp_cache, i_o_cache, world_map):
    def get_next_states(state, warp_cache, i_o_cache, world_map, max_depth):
        pos = state[0]
        floor = state[1]
        output_states = []
        if floor == 0:
            for k in warp_cache:
                start = pos
                end = None
                if pos in k:
                    if pos == k[0]:
                        start = pos
                        end = k[1]
                    elif pos == k[1]:
                        start = k[1]
                        end  = k[0]

                    if not i_o_cache[end] or ((start, end) in warp_cache and warp_cache[(start, end)] == 1) or ((end, start) in warp_cache and warp_cache[(end, start)] == 1):
                        if ((start, end) in warp_cache and warp_cache[(start, end)] != 1) or ((end, start) in warp_cache and warp_cache[(end, start)] != 1):
                            output_states.append((end, floor))
                        else:
                            output_states.append((end, floor+1))

                    elif world_map[end] == "E":
                        output_states.append((end, floor))
        elif 0 < floor < max_depth:
            for k in warp_cache:
                start = pos
                end = None
                if pos in k:
                    if pos == k[0]:
                        start = pos
                        end = k[1]
                    elif pos == k[1]:
                        start = k[1]
                        end = k[0]
                    if i_o_cache[end]:
                        if ((start, end) in warp_cache and warp_cache[(start, end)] != 1) or ((end, start) in warp_cache and warp_cache[(end, start)] != 1):
                            output_states.append((end, floor))
                        else:
                            output_states.append((end, floor + 1))
                    else:
                        if ((start, end) in warp_cache and warp_cache[(start, end)] != 1) or ((end, start) in warp_cache and warp_cache[(end, start)] != 1):
                            output_states.append((end, floor))
                        else:
                            output_states.append((end, floor - 1))
        return output_states

    start = ([k for k in world_map if world_map[k] == "S"][0], 0)
    end = ([k for k in world_map if world_map[k] == "E"][0], 0)
    # sptSet = {start:0}
    # visited = []


    visited = []
    queue = [[start]]
    out_path = []
    fastest = float('inf')
    max_depth = len([k for k in world_map if type(world_map[k]) == Warp])
    while queue:
        path = queue.pop(0)
        vertex = path[-1]
        if vertex == end:
            if calculate_distance_along_path(path, warp_cache) < fastest:
                out_path = path
                fastest = calculate_distance_along_path(path, warp_cache)

        if vertex not in visited:
            for new_state in get_next_states(vertex, warp_cache, i_o_cache, world_map, max_depth):
                new_path = list(path)
                new_path.append(new_state)
                queue.append(new_path)

            visited.append(vertex)
    return out_path


def is_outside(position, world_map):
    top_left = min(world_map)
    bottom_right = max(world_map)
    middle = ((bottom_right[0] // 2), (bottom_right[1] // 2))
    # test if warp is on the left side of something
    if world_map[(position[0] - 1, position[1])] == "#" and world_map[(position[0] + 1, position[1])] == ".":
        # left side if wall, must be on the left side of either the outside or the indie
        if position[0] < middle[0]:
            return True
        else:
            return False
    # test if warp on the right side of something
    if world_map[(position[0] + 1, position[1])] == "#" and world_map[(position[0] - 1, position[1])] == ".":
        if position[0] > middle[0]:
            return True
        else:
            return False

    # test if warp on the top side of something
    if world_map[(position[0], position[1] - 1)] == "#" and world_map[(position[0], position[1] + 1)] == ".":
        if position[1] < middle[1]:
            return True
        else:
            return False

    # test if warp on the bottom side of something
    if world_map[(position[0], position[1] + 1)] == "#" and world_map[(position[0], position[1] - 1)] == ".":
        if position[1] > middle[1]:
            return True
        else:
            return False
    # must be one of the above
    # ERROR!
    assert False


def get_inside_or_outside(position, world_map):
    top_left = min(world_map)
    bottom_right = max(world_map)
    middle = ((bottom_right[0] // 2), (bottom_right[1] // 2))
    # test if warp is on the left side of something
    if world_map[(position[0] - 1, position[1])] == "#" and world_map[(position[0] + 1, position[1])] == ".":
        # left side if wall, must be on the left side of either the outside or the indie
        if position[0] < middle[0]:
            return "outside"
        else:
            return "inside"
    # test if warp on the right side of something
    if world_map[(position[0] + 1, position[1])] == "#" and world_map[(position[0] - 1, position[1])] == ".":
        if position[0] > middle[0]:
            return "outside"
        else:
            return "inside"

    # test if warp on the top side of something
    if world_map[(position[0], position[1] - 1)] == "#" and world_map[(position[0], position[1] + 1)] == ".":
        if position[1] < middle[1]:
            return "outside"
        else:
            return "inside"

    # test if warp on the bottom side of something
    if world_map[(position[0], position[1] + 1)] == "#" and world_map[(position[0], position[1] - 1)] == ".":
        if position[1] > middle[1]:
            return "outside"
        else:
            return "inside"
    # must be one of the above
    # ERROR!
    assert False

def calculate_distance_along_path(path, warp_cache):
    steps = [(path[x][0],path[x+1][0]) for x in range(len(path)-1)]
    dist = 0
    for s,e in steps:
        for k in warp_cache:
            if s in k and e in k:
                dist += warp_cache[k]
    return dist

def traverse_map_part2(world_map):
    def get_next_states(state, world_map):
        possible_states = []
        position = state[0]
        floor = state[1]

        if type(world_map[position]) == Warp:
            if floor > 54:
                return possible_states
            if floor == 0:
                if get_inside_or_outside(position, world_map) == "inside":
                    if world_map[position].A == position:
                        possible_states.append((world_map[position].B, floor+1))
                    else:
                        possible_states.append((world_map[position].A, floor+1))
            else:
                if get_inside_or_outside(position, world_map) == "inside":
                    if world_map[position].A == position:
                        possible_states.append((world_map[position].B,floor+1))
                    else:
                        possible_states.append((world_map[position].A, floor+1))
                else:
                    if world_map[position].A == position:
                        possible_states.append((world_map[position].B, floor-1))
                    else:
                        possible_states.append((world_map[position].A, floor-1))


        # up
        if world_map[(position[0], position[1] - 1)] != "#":
            possible_states.append(((position[0], position[1] - 1), floor))

        # down
        if world_map[(position[0], position[1] + 1)] != "#":
            possible_states.append(((position[0], position[1] + 1), floor))
        # left
        if world_map[(position[0] - 1, position[1])] != "#":
            possible_states.append(((position[0] - 1, position[1]), floor))

        # right
        if world_map[(position[0] + 1, position[1])] != "#":
            possible_states.append(((position[0] + 1, position[1]), floor))

        return possible_states

    # find start and end
    # positions are now made from (pos, floor)
    start = ([k for k in world_map if world_map[k] == "S"][0], 0)
    end = ([k for k in world_map if world_map[k] == "E"][0], 0)
    print(start, end)

    # use BFS to explore the map
    visited = []
    queue = [[start]]
    while queue:
        path = queue.pop(0)
        vertex = path[-1]
        if vertex == end:
            return path
        print(path)

        if vertex not in visited:
            for new_state in get_next_states(vertex, world_map):
                new_path = list(path)
                new_path.append(new_state)
                queue.append(new_path)

            visited.append(vertex)


def test_input():
    lines = [
        "         A           ",
        "         A           ",
        "  #######.#########  ",
        "  #######.........#  ",
        "  #######.#######.#  ",
        "  #######.#######.#  ",
        "  #######.#######.#  ",
        "  #####  B    ###.#  ",
        "BC...##  C    ###.#  ",
        "  ##.##       ###.#  ",
        "  ##...DE  F  ###.#  ",
        "  #####    G  ###.#  ",
        "  #########.#####.#  ",
        "DE..#######...###.#  ",
        "  #.#########.###.#  ",
        "FG..#########.....#  ",
        "  ###########.#####  ",
        "             Z       ",
        "             Z       "

    ]
    return lines

def test_input2():
    lines = [
        "                   A               ",
        "                   A               ",
        "  #################.#############  ",
        "  #.#...#...................#.#.#  ",
        "  #.#.#.###.###.###.#########.#.#  ",
        "  #.#.#.......#...#.....#.#.#...#  ",
        "  #.#########.###.#####.#.#.###.#  ",
        "  #.............#.#.....#.......#  ",
        "  ###.###########.###.#####.#.#.#  ",
        "  #.....#        A   C    #.#.#.#  ",
        "  #######        S   P    #####.#  ",
        "  #.#...#                 #......VT",
        "  #.#.#.#                 #.#####  ",
        "  #...#.#               YN....#.#  ",
        "  #.###.#                 #####.#  ",
        "DI....#.#                 #.....#  ",
        "  #####.#                 #.###.#  ",
        "ZZ......#               QG....#..AS",
        "  ###.###                 #######  ",
        "JO..#.#.#                 #.....#  ",
        "  #.#.#.#                 ###.#.#  ",
        "  #...#..DI             BU....#..LF",
        "  #####.#                 #.#####  ",
        "YN......#               VT..#....QG",
        "  #.###.#                 #.###.#  ",
        "  #.#...#                 #.....#  ",
        "  ###.###    J L     J    #.#.###  ",
        "  #.....#    O F     P    #.#...#  ",
        "  #.###.#####.#.#####.#####.###.#  ",
        "  #...#.#.#...#.....#.....#.#...#  ",
        "  #.#####.###.###.#.#.#########.#  ",
        "  #...#.#.....#...#.#.#.#.....#.#  ",
        "  #.###.#####.###.###.#.#.#######  ",
        "  #.#.........#...#.............#  ",
        "  #########.###.###.#############  ",
        "           B   J   C               ",
        "           U   P   P               "

    ]
    return lines

def test_input3():
    lines = [
        "             Z L X W       C                 ",
        "             Z P Q B       K                 ",
        "  ###########.#.#.#.#######.###############  ",
        "  #...#.......#.#.......#.#.......#.#.#...#  ",
        "  ###.#.#.#.#.#.#.#.###.#.#.#######.#.#.###  ",
        "  #.#...#.#.#...#.#.#...#...#...#.#.......#  ",
        "  #.###.#######.###.###.#.###.###.#.#######  ",
        "  #...#.......#.#...#...#.............#...#  ",
        "  #.#########.#######.#.#######.#######.###  ",
        "  #...#.#    F       R I       Z    #.#.#.#  ",
        "  #.###.#    D       E C       H    #.#.#.#  ",
        "  #.#...#                           #...#.#  ",
        "  #.###.#                           #.###.#  ",
        "  #.#....OA                       WB..#.#..ZH",
        "  #.###.#                           #.#.#.#  ",
        "CJ......#                           #.....#  ",
        "  #######                           #######  ",
        "  #.#....CK                         #......IC",
        "  #.###.#                           #.###.#  ",
        "  #.....#                           #...#.#  ",
        "  ###.###                           #.#.#.#  ",
        "XF....#.#                         RF..#.#.#  ",
        "  #####.#                           #######  ",
        "  #......CJ                       NM..#...#  ",
        "  ###.#.#                           #.###.#  ",
        "RE....#.#                           #......RF",
        "  ###.###        X   X       L      #.#.#.#  ",
        "  #.....#        F   Q       P      #.#.#.#  ",
        "  ###.###########.###.#######.#########.###  ",
        "  #.....#...#.....#.......#...#.....#.#...#  ",
        "  #####.#.###.#######.#######.###.###.#.#.#  ",
        "  #.......#.......#.#.#.#.#...#...#...#.#.#  ",
        "  #####.###.#####.#.#.#.#.###.###.#.###.###  ",
        "  #.......#.....#.#...#...............#...#  ",
        "  #############.#.#.###.###################  ",
        "               A O F   N                     ",
        "               A A D   M                     "
    ]
    return lines

def part1():
    t = read_input()
    wm = parse_lines(t)
    max_portals = len([k for k in wm if type(wm[k]) == Warp])
    print(max_portals)
    print_world_map(wm)
    path = traverse_map(wm)
    print(path)
    print(len(path) - 1)

def part2():
    # t = read_input()
    t = read_input()
    wm = parse_lines(t)
    max_portals = len([k for k in wm if type(wm[k]) == Warp])
    print(max_portals)
    print_world_map(wm)
    warp_cache = precalculate_distances(wm)
    i_o_cache = precalculate_inside_or_outside(wm)
    print(warp_cache)
    print(i_o_cache)

    p = traverse_redux_part2(warp_cache, i_o_cache, wm)
    print(calculate_distance_along_path(p, warp_cache))

if __name__ == "__main__":
    # t = test_input3()
    # part1()
    part2()

    # bfs too slow, precalculate the shortest paths between all pairs of warps including the start and end
    # go from warp to warp deciding if you can take a certain warp being on the inside or outside with what floor

