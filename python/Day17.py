import pprint
import copy

def prog_to_dict(program):
    return dict(zip(range(len(program)), program))


def read_input():
    with open("Day17-input.txt") as f:
        input = f.readline()
        prog = list(map(int, input.split(",")))
    return prog


class Interpreter:
    def __init__(self, program, debug=False, input_buffer=[]):
        self.program = program
        self.pos = 0
        self.debug = debug
        self.parameter_mode = 0
        self.relative_base = 0
        self.output_buffer = []
        self.map = []
        self.input_buffer = input_buffer

    def flush_output_buffer(self):
        for char in self.output_buffer:
            print(chr(char), end="")
        print()
        self.map.append(list(map(chr, self.output_buffer)))
        self.output_buffer = []

    def incr(self):
        self.pos += 1
        return

    def retrieve(self, pos):
        # returns value dependant on parameter mode
        if self.parameter_mode == 0:
            if pos in self.program.keys():
                return self.program[pos]
            else:
                # pos outside of memory
                return 0
        if self.parameter_mode == 1:
            return pos
        if self.parameter_mode == 2:
            if self.relative_base + pos in self.program.keys():
                return self.program[self.relative_base + pos]
            else:
                # pos outside of memory
                return 0

    def get_next(self):
        self.incr()
        out = self.program[self.pos]
        return out

    def write(self, pos, val):
        if self.debug:
            print("@{} Write {} to {}".format(self.pos, val, pos))
        self.program[pos] = val

    def add(self, modes):
        self.parameter_mode = modes.pop()
        a_1 = self.get_next()
        a = self.retrieve(a_1)
        self.parameter_mode = modes.pop()
        b_1 = self.get_next()
        b = self.retrieve(b_1)
        self.parameter_mode = modes.pop()
        # writes are always position mode
        c = self.get_next()
        if self.parameter_mode == 2:
            c += self.relative_base

        if self.debug:
            print("@{} #{} = ({}){} + ({}){}".format(self.pos, c, a_1, a, b_1, b))
        self.write(c, a + b)

    def mul(self, modes):
        self.parameter_mode = modes.pop()
        a_1 = self.get_next()
        a = self.retrieve(a_1)
        self.parameter_mode = modes.pop()
        b_1 = self.get_next()
        b = self.retrieve(b_1)
        self.parameter_mode = modes.pop()
        # writes are always position mode
        c = self.get_next()
        if self.parameter_mode == 2:
            c += self.relative_base

        if self.debug:
            print("@{} #{} = ({}){} * ({}){}".format(self.pos, c, a_1, a, b_1, b))
        self.write(c, a * b)

    def get_input(self, modes):
        self.parameter_mode = modes.pop()
        dst = self.get_next()
        if self.parameter_mode == 2:
            dst += self.relative_base
        # get input should return a value from some input
        if self.input_buffer == []:
            get_input = ord(input("Input: "))
        else:
            i = self.input_buffer.pop(0)
            if i != 10:
                    get_input = ord(i)
            else:
                get_input = 10
            print("Input: {}".format(i))
        if self.debug:
            if self.parameter_mode != 2:
                print("@{} Input {} to ({}){}".format(self.pos, get_input, dst, dst))
            else:
                print("@{} Input {} to ({}){}".format(self.pos, get_input, dst + self.relative_base, dst))
        self.write(dst, get_input)

    def output(self, modes):
        self.parameter_mode = modes.pop()
        src = self.get_next()
        # output the value at src
        a = self.retrieve(src)
        # print("\t@{} Output: ({}){}".format(self.pos, src, a))
        if a != 10:
            self.output_buffer.append(a)
        else:
            self.flush_output_buffer()

    def jump_if_true(self, modes):
        # if true then set program pointer to val
        self.parameter_mode = modes.pop()
        a_1 = self.get_next()
        a = self.retrieve(a_1)
        self.parameter_mode = modes.pop()
        b_1 = self.get_next()
        b = self.retrieve(b_1)

        if self.debug:
            print("@{} JIT {} - ({}){} to ({}){}".format(self.pos, a != 0, a_1, a, b_1, b))
        if a != 0:
            self.pos = b
            # pos it automaticly incremented after each cycle, this stop the incrementation after a jump
            self.pos -= 1

    def jump_if_false(self, modes):
        # if false then set program pointer to val
        self.parameter_mode = modes.pop()
        a_1 = self.get_next()
        a = self.retrieve(a_1)
        self.parameter_mode = modes.pop()
        b_1 = self.get_next()
        b = self.retrieve(b_1)
        if self.debug:
            print("@{} JIF {} - ({}){} to ({}){}".format(self.pos, a == 0, a_1, a, b_1, b))
        if a == 0:
            self.pos = b
            # pos it automaticly incremented after each cycle, this stop the incrementation after a jump
            self.pos -= 1

    def less_than(self, modes):
        self.parameter_mode = modes.pop()
        a_1 = self.get_next()
        a = self.retrieve(a_1)
        self.parameter_mode = modes.pop()
        b_1 = self.get_next()
        b = self.retrieve(b_1)
        self.parameter_mode = modes.pop()
        # writes are always position mode
        c = self.get_next()
        if self.parameter_mode == 2:
            c += self.relative_base

        if self.debug:
            print("@{} #{} = ({}){} < ({}){}".format(self.pos, a < b, a_1, a, b_1, b))

        if a < b:
            self.write(c, 1)
        else:
            self.write(c, 0)

    def equals(self, modes):
        self.parameter_mode = modes.pop()
        a_1 = self.get_next()
        a = self.retrieve(a_1)
        self.parameter_mode = modes.pop()
        b_1 = self.get_next()
        b = self.retrieve(b_1)
        self.parameter_mode = modes.pop()
        # writes are always position mode
        c = self.get_next()
        if self.parameter_mode == 2:
            c += self.relative_base

        if self.debug:
            print("@{} #{} = ({}){} == ({}){}".format(self.pos, a == b, a_1, a, b_1, b))

        if a == b:
            self.write(c, 1)
        else:
            self.write(c, 0)

    def adjust_relative_base(self, modes):
        self.parameter_mode = modes.pop()
        a_1 = self.get_next()
        a = self.retrieve(a_1)
        old = self.relative_base
        self.relative_base += a
        if self.debug:
            print("@{} Relative base {} + ({}){} = {}".format(self.pos, old, a_1, a, self.relative_base))

    def decode(self, instr):
        s_instr = str(instr)

        # pad input to 5 length
        if len(s_instr) < 5:
            s_instr = '0' * (5 - len(s_instr)) + s_instr

        opcode = int(s_instr[-2:])
        s_instr = list(map(int, s_instr[:-2]))
        if opcode == 1:
            self.add(s_instr)
        elif opcode == 2:
            self.mul(s_instr)
        elif opcode == 3:
            self.get_input(s_instr)
        elif opcode == 4:
            self.output(s_instr)
        elif opcode == 5:
            self.jump_if_true(s_instr)
        elif opcode == 6:
            self.jump_if_false(s_instr)
        elif opcode == 7:
            self.less_than(s_instr)
        elif opcode == 8:
            self.equals(s_instr)
        elif opcode == 9:
            self.adjust_relative_base(s_instr)
        else:
            print("@{} Dont know opcode: {}".format(self.pos, opcode))

    def run(self):
        if self.debug:
            pprint.pprint(self.program)

        while self.program[self.pos] != 99:
            self.decode(self.program[self.pos])
            self.incr()

            # print(self.program)
        print("@{} Halt!".format(self.pos))
        return self.program


def print_map(in_map):
    for line in in_map:
        print("".join(line))


def remove_sublist_from_list(sublist, in_list):
    for i in range(len(in_list)-len(sublist)+1):
        remove = False
        for x in range(len(sublist)):
            if in_list[i+x] == sublist[x]:
                remove = True
            else:
                remove = False
                break
        if remove:
            in_list = in_list[:i] + in_list[i+len(sublist):]
            return in_list
    return in_list


def sliding_window_group(window_size, in_list):
    a = [[in_list[i] for i in range(x,x+window_size)] for x in range(len(in_list)-window_size+1)]
    return a


def calc_alignment_sum(coords_map):
    def check_coord(in_pos):
        if in_pos in coords_map.keys() and coords_map[in_pos] == "#":
            return True
        else:
            return False
    crosses = []
    for pos in coords_map:
        if coords_map[pos] == "#":
            if check_coord((pos[0], pos[1] - 1)) and check_coord((pos[0], pos[1] + 1)) and \
                    check_coord((pos[0] - 1, pos[1])) and check_coord((pos[0] + 1, pos[1])):
                crosses.append(pos)
    return sum([a[0]*a[1] for a in crosses])


class Pathing_ai:
    def __init__(self, coords_map):
        self.start = None
        self.end = None
        self.pos = None
        self.coords_map = coords_map
        self.init_scaffolding_pathing()
        self.facing = "up"
        self.moves = []

    def check_coord(self, in_pos):
        if in_pos in self.coords_map.keys() and self.coords_map[in_pos] == "#":
            return True
        else:
            return False

    def neighbours(self, pos):
        total = 0
        if self.check_coord((pos[0], pos[1] + 1)):
            total +=1

        if self.check_coord((pos[0], pos[1] - 1)):
            total += 1

        if self.check_coord((pos[0] + 1, pos[1])):
            total += 1

        if self.check_coord((pos[0] - 1, pos[1])):
            total += 1

        return total

    def near(self, pos_a, pos_b):

        if pos_a[0] == pos_b[0] and pos_a[1] == pos_b[1]:
            return True
        if pos_a[0] - 1 == pos_b[0] and pos_a[1] == pos_b[1]:
            return True
        if pos_a[0] + 1 == pos_b[0] and pos_a[1] == pos_b[1]:
            return True
        if pos_a[0] == pos_b[0] and pos_a[1] - 1 == pos_b[1]:
            return True
        if pos_a[0] == pos_b[0] and pos_a[1] + 1 == pos_b[1]:
            return True
        return False

    def draw_map(self):
        # find bottom right
        bot_right_x = 0
        bot_right_y = 0
        for y in range(39):
            for x in range(43):
                if (x,y) == self.pos:
                    if self.facing == "up":
                        print("^", end="")
                    if self.facing == "left":
                        print("<", end="")
                    if self.facing == "right":
                        print(">", end="")
                    if self.facing == "down":
                        print("v", end="")
                else:
                    print(self.coords_map[(x,y)], end="")
            print()

    def init_scaffolding_pathing(self):
        # find robot start
        ends = []
        # find possible starting and ending positions
        for pos in self.coords_map:
            if self.coords_map[pos] == "#" and self.neighbours(pos) == 1:
                ends.append(pos)
            if self.coords_map[pos] == "^":
                self.start = pos
                if len(ends) == 2 and not self.start:
                    break

        # decide which end is the start
        for end in ends:
            if self.near(self.start, end):
                ends.remove(end)
                break
        self.end = ends[0]
        self.coords_map[self.start] = "#"

        print(self.start, self.end)

    def in_front(self):
        if self.facing == "up":
            return self.check_coord((self.pos[0], self.pos[1] - 1))
        if self.facing == "down":
            return self.check_coord((self.pos[0], self.pos[1] + 1))
        if self.facing == "left":
            return self.check_coord((self.pos[0] - 1, self.pos[1]))
        if self.facing == "right":
            return self.check_coord((self.pos[0] + 1, self.pos[1]))

    def go_forward(self):
        if self.facing == "up":
            self.pos = (self.pos[0], self.pos[1]-1)
        if self.facing == "down":
            self.pos = (self.pos[0], self.pos[1]+1)
        if self.facing == "left":
            self.pos = (self.pos[0]-1, self.pos[1])
        if self.facing == "right":
            self.pos = (self.pos[0]+1, self.pos[1])

        self.moves[-1] = str(int(self.moves[-1])+1)

    def turn(self):
        if self.facing == "up":
            if self.check_coord((self.pos[0] - 1, self.pos[1])):
                self.facing = "left"
                self.moves += ["L", "0"]
                return

            if self.check_coord((self.pos[0] + 1, self.pos[1])):
                self.facing = "right"
                self.moves += ["R", "0"]
                return

        if self.facing == "down":
            if self.check_coord((self.pos[0] - 1, self.pos[1])):
                self.facing = "left"
                self.moves += ["R", "0"]
                return

            if self.check_coord((self.pos[0] + 1, self.pos[1])):
                self.facing = "right"
                self.moves += ["L", "0"]
                return

        if self.facing == "left":
            if self.check_coord((self.pos[0], self.pos[1]+1)):
                self.facing = "down"
                self.moves += ["L", "0"]
                return
            if self.check_coord((self.pos[0], self.pos[1]-1)):
                self.facing = "up"
                self.moves += ["R", "0"]
                return

        if self.facing == "right":
            if self.check_coord((self.pos[0], self.pos[1]+1)):
                self.facing = "down"
                self.moves += ["R", "0"]
                return
            if self.check_coord((self.pos[0], self.pos[1]-1)):
                self.facing = "up"
                self.moves += ["L", "0"]
                return

    def repeats(self, small_moves, move_list):
        # returns how many times this string appears in the main string
        window_in = sliding_window_group(len(small_moves), move_list)
        count = 0
        for i in window_in:
            if small_moves == i:
                count += 1
        return count

    def code_to_input(self, code):
        out = []
        for tuple in code:
            for i in tuple:
                for c in i:
                    out.append(c)
                out.append(",")
        return out[:-1] + [10]

    def minimise_instructions(self):
        # zip list to tuple
        grouped_moves = [(self.moves[i], self.moves[i+1]) for i in range(0,len(self.moves), 2)]
        A = [None, 0, 0]
        B = [None, 0, 0]
        C = [None, 0, 0]

        def find_remove_optimal_string(grouped_moves):
            out = [None, 0, 0]
            for i in range(1, len(grouped_moves)):
                s = grouped_moves[:i]
                a = (self.repeats(s, grouped_moves))
                if len(s) >= out[1] and a > 2 and len(s)*4 <= 20:
                    out = [s, len(s), a]
                if a == 1:
                    break
            try:
                while out[0] in sliding_window_group(len(out[0]), grouped_moves):
                    grouped_moves = remove_sublist_from_list(out[0], grouped_moves)
            except:
                pass
            return out, grouped_moves

        A, grouped_moves = find_remove_optimal_string(grouped_moves)
        B, grouped_moves = find_remove_optimal_string(grouped_moves)
        C, grouped_moves = find_remove_optimal_string(grouped_moves)
        print(A)
        print(B)
        print(C)
        print(grouped_moves)
        grouped_moves = [(self.moves[i], self.moves[i + 1]) for i in range(0, len(self.moves), 2)]
        out = []
        while grouped_moves:
            if grouped_moves and grouped_moves[0] == A[0][0]:
                grouped_moves = remove_sublist_from_list(A[0], grouped_moves)
                out.append("A")
            if grouped_moves and grouped_moves[0] == B[0][0]:
                grouped_moves = remove_sublist_from_list(B[0], grouped_moves)
                out.append("B")
            if grouped_moves and grouped_moves[0] == C[0][0]:
                grouped_moves = remove_sublist_from_list(C[0], grouped_moves)
                out.append("C")
        print("A: {}".format(A[0]))
        print("B: {}".format(B[0]))
        print("C: {}".format(C[0]))
        print(self.code_to_input(out))
        return self.code_to_input(A[0]), self.code_to_input(B[0]), self.code_to_input(C[0]), self.code_to_input(out)

    def run(self):
        self.pos = self.start
        while self.pos != self.end:
            if self.in_front():
                self.go_forward()
            else:
                self.turn()
        print(self.moves)
        return self.minimise_instructions()





def to_map_coords(in_map):
    out = {}
    for y in range(len(in_map)):
        for x in range(len(in_map[y])):
            out[(x, y)] = in_map[y][x]
    return out


def part1():
    # Part
    code = prog_to_dict(read_input())
    interpreter = Interpreter(code, False)
    a = interpreter.run()
    # a = interpreter.test_prog_7()
    print_map(interpreter.map)
    part1 = calc_alignment_sum(to_map_coords(interpreter.map))
    print("Part1 {}".format(part1))


def part2():
    code = prog_to_dict(read_input())
    interpreter = Interpreter(code, False)
    a = interpreter.run()
    coords_map = to_map_coords(interpreter.map)

    ai = Pathing_ai(coords_map)
    A,B,C,func = ai.run()


    code = prog_to_dict(read_input())
    code[0] = 2
    interpreter = Interpreter(code, False, func+A+B+C+["n", 10])
    a = interpreter.run()
    print(interpreter.output_buffer)

if __name__ == "__main__":
    # part1()
    part2()
    pass
