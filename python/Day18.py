import copy
import itertools

def read_input():
    out = []
    with open("Day18-input.txt") as f:
        lines = f.readlines()
    for line in lines:
        out.append(list(line.strip()))
    return out


def dist(pos1, pos2):
    if pos1[0] == pos2[0]:
        return abs(pos1[1]-pos2[1])
    if pos1[1] == pos2[1]:
        return abs(pos1[0]-pos2[0])
    return float('inf')




class Pathing_ai:
    def __init__(self, in_map):
        self.cur_pos = None
        self.map = in_map
        self.door_locations = {}
        self.key_locations = {}
        self.cache = {}

        # find import locations
        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                if self.map[y][x] == "@":
                    self.cur_pos = (x, y)
                    self.map[y][x] = "."
                if self.map[y][x].isupper():
                    self.door_locations[(x, y)] = self.map[y][x]
                if self.map[y][x].islower():
                    self.key_locations[(x, y)] = self.map[y][x]


    def save_state(self):
        return (copy.deepcopy(self.cur_pos),
                copy.deepcopy(self.map),
                copy.deepcopy(self.door_locations),
                copy.deepcopy(self.key_locations))


    def load_state(self, state):
        self.cur_pos = copy.deepcopy(state[0])
        self.map = copy.deepcopy(state[1])
        self.door_locations = copy.deepcopy(state[2])
        self.key_locations = copy.deepcopy(state[3])

    def get_key_location(self, key):
        return [k for k in self.key_locations if self.key_locations[k] == key][0]

    def on_key(self):
        return self.cur_pos in self.key_locations

    def pickup_key(self):
        if self.on_key():
            key = self.key_locations.pop(self.cur_pos)
            self.map[self.cur_pos[1]][self.cur_pos[0]] = "."
            for loc in self.door_locations:
                if self.door_locations[loc] == key.upper():
                    self.door_locations.pop(loc)
                    self.map[loc[1]][loc[0]] = "."
                    return True
            return True
        return False

    def is_in_map(self, pos):
        if 0 <= pos[1] < len(self.map) and 0 <= pos[0] < len(self.map[pos[1]]):
            return True
        else:
            return False

    def is_passable(self,pos):
        if self.map[pos[1]][pos[0]] != "#" and pos not in self.door_locations:
            return True
        else:
            return False

    def print_map(self):
        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                if (x, y) == self.cur_pos:
                    print("@",end="")
                else:
                    print(self.map[y][x], end="")
            print()

    def path_from_to(self, start, end):
        coords = {end: 0}

        def get_neighbours(coord):
            out = {}
            if self.is_in_map((coord[0]-1, coord[1])) and self.is_passable((coord[0]-1, coord[1])):
                out[(coord[0]-1, coord[1])] = coord[2]+1

            if self.is_in_map((coord[0]+1, coord[1])) and self.is_passable((coord[0]+1, coord[1])):
                out[(coord[0]+1, coord[1])] = coord[2]+1

            if self.is_in_map((coord[0], coord[1]-1)) and self.is_passable((coord[0], coord[1]-1)):
                out[(coord[0], coord[1]-1)] = coord[2]+1

            if self.is_in_map((coord[0], coord[1]+1)) and self.is_passable((coord[0], coord[1]+1)):
                out[(coord[0], coord[1]+1)] = coord[2]
            return out


        while start not in coords:
            temp_coords = copy.deepcopy(coords)
            for coord in coords:
                new_coords = get_neighbours((coord[0], coord[1], coords[coord]))
                for n_coord in new_coords:
                    if n_coord in temp_coords:
                        if new_coords[n_coord] < temp_coords[n_coord]:
                            temp_coords[n_coord] = new_coords[n_coord]
                    else:
                        temp_coords[n_coord] = new_coords[n_coord]
            # if we didn't add or update any new coords, then quit
            if temp_coords == coords:
                return None # there is no path
            coords = copy.deepcopy(temp_coords)

        path = []
        last = (start[0],start[1],coords[start])

        while len(path) == 0 or path[-1] != end:
            nearby = [(c, coords[c]) for c in coords if dist((last[0], last[1]),c) == 1]
            assert nearby != []
            smallest_coord = None
            smallest_dist = float('inf')
            for n in nearby:
                if n[1] < smallest_dist:
                    smallest_coord = n[0]
                    smallest_dist = n[1]
            path.append(smallest_coord)
            last = (smallest_coord[0], smallest_coord[1], smallest_dist)
        return path

    def pathable(self, start, key_list, dist=0):
        if not key_list:
            return dist
        else:
            if (start, key_list) in self.cache:
                return dist+self.cache[(start, key_list)]
            path = self.path_from_to(start, key_list[0])
            keys = copy.deepcopy(self.key_locations)
            if path != None:
                self.cur_pos = path[-1]
                test = self.pickup_key()
                assert test
                x = self.pathable(self.cur_pos, key_list[1:], dist+len(path))
                if x:
                    print("cached")
                    self.cache[(self.cur_pos, key_list)] = x
                return x
            else:
                return False

    def run(self):
        # create a permutations list of key pickup order
        # if it's not possible to pickup the first key, then second key etc then fail

        key_perms = itertools.permutations(self.key_locations)
        # check if it's pathable
        possible_key_paths = []
        for key_path in key_perms:
            state = self.save_state()
            dist = self.pathable(self.cur_pos, key_path)
            if dist:
                print(key_path)
                possible_key_paths.append((key_path, dist))
            self.load_state(state)

        # print lowest path
        lowest = float('inf')
        lowest_p = []
        for p in possible_key_paths:
            if p[1] < lowest:
                lowest_p = p
                lowest = p[1]
        print(lowest)
        print(lowest_p)
        # calc_distance of path








def load_test1():
    t = ["########################",
         "#f.D.E.e.C.b.A.@.a.B.c.#",
         "######################.#",
         "#d.....................#",
         "########################"]
    out = []
    for line in t:
        out.append(list(line.strip()))
    return out


def load_test2():
    t = ["########################",
         "#f.D.E.e.............@.#",
         "######################.#",
         "#d.....................#",
         "########################"]
    out = []
    for line in t:
        out.append(list(line.strip()))
    return out

def load_test3():
    t = ["########################",
        "#...............b.C.D.f#",
        "#.######################",
        "#.....@.a.B.c.d.A.e.F.g#",
        "########################"]
    out = []
    for line in t:
        out.append(list(line.strip()))
    return out

def load_test4():
    t = ["#################",
        "#i.G..c...e..H.p#",
        "########.########",
        "#j.A..b...f..D.o#",
        "########@########",
        "#k.E..a...g..B.n#",
        "########.########",
        "#l.F..d...h..C.m#",
        "#################"]
    out = []
    for line in t:
        out.append(list(line.strip()))
    return out


if __name__ == "__main__":
    # in_map = read_input()
    in_map = load_test1()
    ai = Pathing_ai(in_map)
    ai.print_map()
    ai.run()
    print(ai.cache)