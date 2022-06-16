def part1_input():
    lines = [
        "#....",
        "#...#",
        "##.##",
        "....#",
        "#.##."
    ]
    return lines_to_dict(lines)


def lines_to_dict(lines):
    out = {}
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            out[(x, y)] = lines[y][x]
    return out


def draw_world(world):
    bottom_right = max(world)
    for y in range(bottom_right[1] + 1):
        for x in range(bottom_right[0] + 1):
            print(world[(x, y)], end="")
        print()


def check_count_adjacent_is_alive(world, pos):
    x, y = pos
    count = 0
    # left
    if (x - 1, y) in world and world[(x - 1, y)] == "#":
        count += 1
    # right
    if (x + 1, y) in world and world[(x + 1, y)] == "#":
        count += 1
    # up
    if (x, y - 1) in world and world[(x, y - 1)] == "#":
        count += 1
    # down
    if (x, y + 1) in world and world[(x, y + 1)] == "#":
        count += 1

    if count == 1:
        return True

    return False


def check_space_infested(world, pos):
    x, y = pos
    count = 0
    # left
    if (x - 1, y) in world and world[(x - 1, y)] == "#":
        count += 1
    # right
    if (x + 1, y) in world and world[(x + 1, y)] == "#":
        count += 1
    # up
    if (x, y - 1) in world and world[(x, y - 1)] == "#":
        count += 1
    # down
    if (x, y + 1) in world and world[(x, y + 1)] == "#":
        count += 1

    if count in (1, 2):
        return True

    return False


def step_world(world):
    out_world = {}
    bottom_right = max(world)
    for y in range(bottom_right[1] + 1):
        for x in range(bottom_right[0] + 1):
            if world[(x, y)] == "#":
                if check_count_adjacent_is_alive(world, (x, y)):
                    out_world[(x, y)] = "#"
                else:
                    out_world[(x, y)] = "."
            if world[(x, y)] == ".":
                if check_space_infested(world, (x, y)):
                    out_world[(x, y)] = "#"
                else:
                    out_world[(x, y)] = "."

    return out_world


def test_world1():
    lines = [
        "....#",
        "#..#.",
        "#..##",
        "..#..",
        "#...."
    ]
    return lines_to_dict(lines)


def test_world2():
    lines = [
        ".....",
        ".....",
        ".....",
        "#....",
        ".#..."
    ]
    return biodiversity_rating(lines_to_dict(lines))


def biodiversity_rating(world):
    bottom_right = max(world)
    biodiversity_score = 0
    for k in world:
        if world[k] == "#":
            x, y = k
            biodiversity_score += 2 ** ((y) * (bottom_right[0] + 1) + x)
    return biodiversity_score


def calc_part1(world):
    prevs = [world]
    next_world = step_world(world)
    while next_world not in prevs:
        prevs.append(next_world)
        next_world = step_world(next_world)
    return biodiversity_rating(next_world)


def live_or_dies(square, tiles):
    count = 0
    for t in tiles:
        if t == "#":
            count += 1

    if square == "#":
        if count == 1:
            return "#"
        else:
            return "."

    if square == ".":
        if count in (1, 2):
            return "#"
        else:
            return "."


class Recursive_world:
    def __init__(self, init_world):
        self.worlds = {0: init_world}
        self.worlds[1] = self.create_blank_world()
        self.worlds[-1] = self.create_blank_world()

    def count_bugs(self, layer):
        bugs = 0
        for k in layer:
            if layer[k] == "#":
                bugs +=1
        return bugs

    def count_all_bugs(self):
        total = 0
        for layer in self.worlds:
            total += self.count_bugs(self.worlds[layer])
        return total

    def create_blank_world(self):
        world = {}
        for y in range(5):
            for x in range(5):
                world[(x, y)] = "."
        return world

    def print_all_layers(self):
        def print_layer(layer):
            bottom_right = max(layer)
            for y in range(bottom_right[1] + 1):
                for x in range(bottom_right[0] + 1):
                    if (x, y) != (2, 2):
                        print(layer[(x, y)], end="")
                    else:
                        print('?', end="")
                print()

        start = min(self.worlds)
        end = max(self.worlds)

        for x in range(start,end+1):
            if self.count_bugs(self.worlds[x]) > 0:
                print(f"Depth {x}:")
                print_layer(self.worlds[x])

    def extend_worlds(self):
        edge = (len(self.worlds)-1) // 2
        if self.count_bugs(self.worlds[-edge]) > 0 and self.count_bugs(self.worlds[edge]) > 0:
            self.worlds[-(edge+1)] = self.create_blank_world()
            self.worlds[(edge + 1)] = self.create_blank_world()



    def step_world(self):
        bottom_right = max(self.worlds[0])
        middle = (bottom_right[0] // 2, bottom_right[1] // 2)
        top_edge = [(x, 0) for x in range(bottom_right[0] + 1)]
        bottom_edge = [(x, bottom_right[1]) for x in range(bottom_right[0] + 1)]
        left_edge = [(0, y) for y in range(bottom_right[1] + 1)]
        right_edge = [(bottom_right[0], y) for y in range(bottom_right[1] + 1)]
        around_middle = [(middle[0] - 1, middle[1]), (middle[0] + 1, middle[1]), (middle[0], middle[1] - 1),
                         (middle[0], middle[1] + 1)]

        out_layers = {}
        for layer in self.worlds:
            out_layer = {}
            world = self.worlds[layer]
            for y in range(bottom_right[1] + 1):
                for x in range(bottom_right[0] + 1):
                    if (x, y) == middle:  # we don't calculate for the middle square
                        out_layer[(x, y)] = "?"
                        continue

                    if (x, y) not in top_edge + bottom_edge + left_edge + right_edge + around_middle:
                        if world[(x, y)] == "#":
                            if check_count_adjacent_is_alive(world, (x, y)):
                                out_layer[(x, y)] = "#"
                            else:
                                out_layer[(x, y)] = "."

                        if world[(x, y)] == ".":
                            if check_space_infested(world, (x, y)):
                                out_layer[(x, y)] = "#"
                            else:
                                out_layer[(x, y)] = "."
                        continue

                    if (x, y) in top_edge and (x, y) in left_edge:  # top left corner
                        tiles = []
                        if layer - 1 in self.worlds:
                            tiles.append(self.worlds[layer - 1][(middle[0], middle[1] - 1)])
                            tiles.append(self.worlds[layer - 1][(middle[0] - 1, middle[1])])
                        else:
                            tiles.append('.')

                        tiles.append(self.worlds[layer][(x + 1, y)])
                        tiles.append(self.worlds[layer][(x, y + 1)])
                        out_layer[(x, y)] = live_or_dies(world[(x, y)], tiles)
                        continue

                    if (x, y) in top_edge and (x,y) in right_edge:  # top right corner
                        tiles = []
                        if layer - 1 in self.worlds:
                            tiles.append(self.worlds[layer - 1][(middle[0], middle[1] - 1)])
                            tiles.append(self.worlds[layer - 1][(middle[0] + 1, middle[1])])
                        else:
                            tiles.append('.')
                        tiles.append(self.worlds[layer][(x - 1, y)])
                        tiles.append(self.worlds[layer][(x, y + 1)])
                        out_layer[(x, y)] = live_or_dies(world[(x, y)], tiles)
                        continue

                    if (x, y) in top_edge and (x, y) not in right_edge + left_edge:  # top edge only
                        tiles = []
                        if layer - 1 in self.worlds:
                            tiles.append(self.worlds[layer - 1][(middle[0], middle[1] - 1)])
                        else:
                            tiles.append('.')
                        tiles.append(self.worlds[layer][(x - 1, y)])
                        tiles.append(self.worlds[layer][(x + 1, y)])
                        tiles.append(self.worlds[layer][(x, y + 1)])
                        out_layer[(x, y)] = live_or_dies(world[(x, y)], tiles)
                        continue

                    if (x, y) in left_edge and (x, y) in bottom_edge:  # bottom left corner
                        tiles = []
                        if layer - 1 in self.worlds:
                            tiles.append(self.worlds[layer - 1][(middle[0] - 1, middle[1])])
                            tiles.append(self.worlds[layer - 1][(middle[0], middle[1] + 1)])
                        else:
                            tiles.append('.')
                        tiles.append(self.worlds[layer][(x + 1, y)])
                        tiles.append(self.worlds[layer][(x, y - 1)])
                        out_layer[(x, y)] = live_or_dies(world[(x, y)], tiles)
                        continue

                    if (x, y) in left_edge and (x, y) not in bottom_edge + top_edge:  # left edge
                        tiles = []
                        if layer - 1 in self.worlds:
                            tiles.append(self.worlds[layer - 1][(middle[0] - 1, middle[1])])
                        else:
                            tiles.append('.')
                        tiles.append(self.worlds[layer][(x + 1, y)])
                        tiles.append(self.worlds[layer][(x, y - 1)])
                        tiles.append(self.worlds[layer][(x, y + 1)])
                        out_layer[(x, y)] = live_or_dies(world[(x, y)], tiles)
                        continue

                    if (x, y) in right_edge and (x, y) in bottom_edge:  # bottom right corner
                        tiles = []
                        if layer - 1 in self.worlds:
                            tiles.append(self.worlds[layer - 1][(middle[0] + 1, middle[1])])
                            tiles.append(self.worlds[layer - 1][(middle[0], middle[1] + 1)])
                        else:
                            tiles.append('.')
                        tiles.append(self.worlds[layer][(x, y - 1)])
                        tiles.append(self.worlds[layer][(x - 1, y)])
                        out_layer[(x, y)] = live_or_dies(world[(x, y)], tiles)
                        continue

                    if (x, y) in bottom_edge and (x, y) not in left_edge + right_edge:  # bottom_edge
                        tiles = []
                        if layer - 1 in self.worlds:
                            tiles.append(self.worlds[layer - 1][(middle[0], middle[1] + 1)])
                        else:
                            tiles.append('.')
                        tiles.append(self.worlds[layer][(x - 1, y)])
                        tiles.append(self.worlds[layer][(x, y - 1)])
                        tiles.append(self.worlds[layer][(x + 1, y)])
                        out_layer[(x, y)] = live_or_dies(world[(x, y)], tiles)
                        continue

                    if (x, y) in right_edge and (x, y) not in bottom_edge + top_edge:  # right_edge
                        tiles = []
                        if layer - 1 in self.worlds:
                            tiles.append(self.worlds[layer - 1][(middle[0] + 1, middle[1])])
                        else:
                            tiles.append('.')
                        tiles.append(self.worlds[layer][(x, y - 1)])
                        tiles.append(self.worlds[layer][(x - 1, y)])
                        tiles.append(self.worlds[layer][(x, y + 1)])
                        out_layer[(x, y)] = live_or_dies(world[(x, y)], tiles)
                        continue

                    # middle tiles
                    if (x, y) in around_middle:
                        if (x, y) == (middle[0], middle[1] - 1):  # top of middle
                            tiles = []
                            if layer + 1 in self.worlds:
                                for e in top_edge:
                                    tiles.append(self.worlds[layer + 1][e])  # top edge of internal layer
                            else:
                                tiles.append('.')
                            tiles.append(self.worlds[layer][(x, y - 1)])
                            tiles.append(self.worlds[layer][(x - 1, y)])
                            tiles.append(self.worlds[layer][(x + 1, y)])
                            out_layer[(x, y)] = live_or_dies(world[(x, y)], tiles)

                        if (x, y) == (middle[0] - 1, middle[1]):  # left of middle
                            tiles = []
                            if layer +1 in self.worlds:
                                for e in left_edge:
                                    tiles.append(self.worlds[layer + 1][e])  # top edge of internal layer
                            else:
                                tiles.append('.')
                            tiles.append(self.worlds[layer][(x, y - 1)])
                            tiles.append(self.worlds[layer][(x - 1, y)])
                            tiles.append(self.worlds[layer][(x, y + 1)])
                            out_layer[(x, y)] = live_or_dies(world[(x, y)], tiles)

                        if (x, y) == (middle[0] + 1, middle[1]):  # right of middle
                            tiles = []
                            if layer + 1 in self.worlds:
                                for e in right_edge:
                                    tiles.append(self.worlds[layer + 1][e])  # top edge of internal layer
                            else:
                                tiles.append('.')
                            tiles.append(self.worlds[layer][(x, y - 1)])
                            tiles.append(self.worlds[layer][(x + 1, y)])
                            tiles.append(self.worlds[layer][(x, y + 1)])
                            out_layer[(x, y)] = live_or_dies(world[(x, y)], tiles)

                        if (x, y) == (middle[0], middle[1] + 1):  # bottom of middle
                            tiles = []
                            if layer + 1 in self.worlds:
                                for e in bottom_edge:
                                    tiles.append(self.worlds[layer + 1][e])  # top edge of internal layer
                            else:
                                tiles.append('.')

                            tiles.append(self.worlds[layer][(x + 1, y)])
                            tiles.append(self.worlds[layer][(x - 1, y)])
                            tiles.append(self.worlds[layer][(x, y + 1)])
                            out_layer[(x, y)] = live_or_dies(world[(x, y)], tiles)

            out_layers[layer] = out_layer
        self.worlds = out_layers
        self.extend_worlds()

def test_input3():
    lines = [
        "....#",
        "#..#.",
        "#.?##",
        "..#..",
        "#...."
    ]
    return lines_to_dict(lines)

def part1():
    print(calc_part1(part1_input()))

def part2():
    p2 = Recursive_world(part1_input())
    p2.print_all_layers()
    print("-"*20)
    for i in range(0, 200):
        p2.step_world()
        #p2.print_all_layers()
        #print("-"*20)
    print(len(p2.worlds))
    print(p2.count_all_bugs())

if __name__ == "__main__":
    part2()

