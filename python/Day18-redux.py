import copy
import itertools

def read_input():
    out = []
    with open("Day18-input.txt") as f:
        lines = f.readlines()
    for line in lines:
        out.append(list(line.strip()))
    return out

def read_input_part2():
    out = []
    with open("Day18-input-part2.txt") as f:
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
        self.cache = []
        self.memoize = {}

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
        self.start = copy.deepcopy(self.cur_pos)
        print("Pre-calculating")
        paths_between = itertools.combinations([self.cur_pos] + list(self.key_locations.keys()), 2)
        for s,e in paths_between:
            print(s,e)
            self.cache.append((s,e) + self.get_dist_keys_doors(self.path_from_to(s, e)))
        print(self.cache)


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
        if self.map[pos[1]][pos[0]] != "#":
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
        return [start]+path

    def door_to_key(self, coord):
        door = self.door_locations[coord]
        key = door.lower()
        for k in self.key_locations:
            if self.key_locations[k] == key:
                return k

    def get_dist_keys_doors(self, path):
        keys_picked_up = []
        required_keys = []
        for p in path:
            if p in self.key_locations:
                keys_picked_up.append(p)
            if p in self.door_locations:
                required_keys.append(self.door_to_key(p))
        dist = len(path)-1
        return (dist, set(keys_picked_up), set(required_keys))

    def get_next_possible_state(self, current_position, current_keys, distance=0):
        states = []
        for start, end, dist, keys_collected, required_keys in self.cache:
            if ((start == current_position and end not in current_keys) or (
                    end == current_position and start not in current_keys)) and required_keys.difference(
                    current_keys.union(keys_collected)) == set():
                if start == current_position:
                    states.append((end, current_keys.union(keys_collected), distance + dist))
                else:
                    states.append((start, current_keys.union(keys_collected), distance + dist))
        return states


    def run(self):
        # get any path that collects all the key


        current_keys = {self.start}
        all_keys = set(list(self.key_locations))
        current_position = self.cur_pos
        distance = 0
        path = [current_position]
        key_pickup_order = []

        # shortest_dist = self.get_distance_to_end(current_position, current_keys)
        shortest_dist = self.distance_to_collect_keys(current_position, current_keys)
        # print(next_states)
        # current_position, distance, current_keys = next_states[0]
        # path.append(current_position)
        # key_pickup_order.append(self.key_locations[current_position])


        print(shortest_dist)

    def distance_to_collect_keys(self, current_position, current_keys):
        if len(current_keys) == len(self.key_locations)+1:
            return 0

        memoize_key = (current_position, tuple(current_keys))
        if memoize_key in self.memoize:
            return self.memoize[memoize_key]

        shortest_dist = float('inf')
        for state in self.get_next_possible_state(current_position, current_keys):
            d = state[2] + self.distance_to_collect_keys(state[0], state[1])
            shortest_dist = min(shortest_dist, d)

        self.memoize[memoize_key] = shortest_dist
        return shortest_dist

    def get_distance_to_end(self, current_position, current_keys, distance=0):
        visited = []
        queue = []
        queue.append((current_position, current_keys, distance))
        shortest_dist = float('inf')
        memoize = {}
        while queue:
            state = queue.pop()
            # get_next_possible_state(current_position, current_keys, distance, path)
            for next_state in self.get_next_possible_state(state[0], state[1], state[2]):
                if next_state not in visited:
                    visited.append(next_state)
                    queue.append(next_state)
                    # if next_state[1] in memoize:
                    #     if next_state[2] + distance < shortest_dist:
                    #         shortest_dist = next_state[2] + distance
                    if len(next_state[1]) == (len(self.key_locations) + 1) and next_state[2] < shortest_dist:
                        shortest_dist = next_state[2]
        return shortest_dist

class Pathing_ai_part2:
    def __init__(self, in_map):
        self.cur_pos = []
        self.map = in_map
        self.door_locations = {}
        self.key_locations = {}
        self.cache = []
        self.memoize = {}
        self.paths = []
        # find import locations
        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                if self.map[y][x] == "@":
                    self.cur_pos.append((x, y))
                    self.map[y][x] = "."
                if self.map[y][x].isupper():
                    self.door_locations[(x, y)] = self.map[y][x]
                if self.map[y][x].islower():
                    self.key_locations[(x, y)] = self.map[y][x]
        self.start = copy.deepcopy(self.cur_pos)
        print("Pre-calculating")
        paths_between = itertools.combinations(self.cur_pos + list(self.key_locations.keys()), 2)
        for s,e in paths_between:
            print(s,e)
            path = self.path_from_to(s, e)
            if path:
                self.cache.append((s,e) + self.get_dist_keys_doors(path))
        print(self.cache)


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
        if self.map[pos[1]][pos[0]] != "#":
            return True
        else:
            return False

    def print_map(self):
        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                if (x, y) in self.cur_pos:
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
        return [start]+path

    def door_to_key(self, coord):
        door = self.door_locations[coord]
        key = door.lower()
        for k in self.key_locations:
            if self.key_locations[k] == key:
                return k

    def get_dist_keys_doors(self, path):
        keys_picked_up = []
        required_keys = []
        for p in path:
            if p in self.key_locations:
                keys_picked_up.append(p)
            if p in self.door_locations:
                required_keys.append(self.door_to_key(p))
        dist = len(path)-1
        return (dist, set(keys_picked_up), set(required_keys))

    def get_next_possible_state(self, current_position, current_keys, distance=0):
        states = []
        for start, end, dist, keys_collected, required_keys in self.cache:
            if ((start in current_position and end not in current_keys) or (
                    end in current_position and start not in current_keys)) and required_keys.difference(
                    current_keys.union(keys_collected)) == set():
                if start in current_position:
                    t = list(current_position)
                    pos = t.index(start)
                    t[pos] = end
                    t_current_position = tuple(t)
                    states.append((t_current_position, current_keys.union(keys_collected), distance + dist))
                else:
                    t = list(current_position)
                    pos = t.index(end)
                    t[pos] = start
                    t_current_position = tuple(t)
                    states.append((t_current_position, current_keys.union(keys_collected), distance + dist))
        return states


    def run(self):
        # get any path that collects all the key


        current_keys = set(self.start)
        all_keys = set(list(self.key_locations))
        current_position = tuple(self.cur_pos)
        distance = 0
        path = [current_position]
        key_pickup_order = []

        # shortest_dist = self.get_distance_to_end(current_position, current_keys)
        shortest_dist = self.distance_to_collect_keys(current_position, current_keys)
        # print(next_states)
        # current_position, distance, current_keys = next_states[0]
        # path.append(current_position)
        # key_pickup_order.append(self.key_locations[current_position])


        print(shortest_dist)

    def draw_state(self, current_position, current_keys):
        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                if (x, y) in current_position:
                    print("@", end="")
                elif (x,y) not in current_keys and (x,y) in self.key_locations:
                    print(self.key_locations[(x,y)], end="")
                elif (x,y) in current_keys and (x,y) in self.key_locations:
                    print(".", end="")
                elif (x,y) in self.door_locations and self.door_to_key((x,y)) in current_keys:
                    print(".", end="")
                else:
                    print(self.map[y][x], end="")
            print()

    def distance_to_collect_keys(self, current_position, current_keys, path=[]):
        if len(current_keys) == len(self.key_locations)+len(current_position):
            return 0

        memoize_key = (current_position, tuple(current_keys))
        if memoize_key in self.memoize:
            return self.memoize[memoize_key]

        shortest_dist = float('inf')
        for state in self.get_next_possible_state(current_position, current_keys):
            #print()


            d = state[2] + self.distance_to_collect_keys(state[0], state[1],path+[state])
            shortest_dist = min(shortest_dist, d)

        self.memoize[memoize_key] = shortest_dist
        return shortest_dist

    def get_distance_to_end(self, current_position, current_keys, distance=0):
        visited = []
        queue = []
        queue.append((current_position, current_keys, distance))
        shortest_dist = float('inf')
        memoize = {}
        while queue:
            state = queue.pop()
            # get_next_possible_state(current_position, current_keys, distance, path)
            for next_state in self.get_next_possible_state(state[0], state[1], state[2]):
                if next_state not in visited:
                    visited.append(next_state)
                    queue.append(next_state)
                    # if next_state[1] in memoize:
                    #     if next_state[2] + distance < shortest_dist:
                    #         shortest_dist = next_state[2] + distance
                    if len(next_state[1]) == (len(self.key_locations) + 4) and next_state[2] < shortest_dist:
                        shortest_dist = next_state[2]
        return shortest_dist


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

def load_part2_test1():
    t = ["###############",
        "#d.ABC.#.....a#",
        "######@#@######",
        "###############",
        "######@#@######",
        "#b.....#.....c#",
        "###############"]
    out = []
    for line in t:
        out.append(list(line.strip()))
    return out

def load_part2_test2():
    t = ["#############",
        "#DcBa.#.GhKl#",
        "#.###@#@#I###",
        "#e#d#####j#k#",
        "###C#@#@###J#",
        "#fEbA.#.FgHi#",
        "#############"]
    out = []
    for line in t:
        out.append(list(line.strip()))
    return out

def load_part2_test3():
    t = ["#############",
        "#g#f.D#..h#l#",
        "#F###e#E###.#",
        "#dCba@#@BcIJ#",
        "#############",
        "#nK.L@#@G...#",
        "#M###N#H###.#",
        "#o#m..#i#jk.#",
        "#############"]
    out = []
    for line in t:
        out.append(list(line.strip()))
    return out

if __name__ == "__main__":
    # in_map = read_input()
    # # in_map = load_test4()
    # ai = Pathing_ai(in_map)
    # ai.print_map()
    # ai.run()
    # part 2
    # in_map = load_part2_test3()
    in_map = read_input_part2()
    ai2 = Pathing_ai_part2(in_map)
    ai2.print_map()
    print()
    ai2.run()
