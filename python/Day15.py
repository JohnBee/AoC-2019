import pprint
import copy

part1 = None
part2 = None


def prog_to_dict(program):
    return dict(zip(range(len(program)), program))

def read_input():
    with open("Day15-input.txt") as f:
        input = f.readline()
        prog = list(map(int, input.split(",")))
    return prog


def fix_input(prog, noun, verb):
    prog[1] = noun
    prog[2] = verb
    return prog

def draw_map(map):
    size = 42
    half_size = size // 2
    # draw 11x11 around the droid
    for y in range(-half_size, half_size+1):
        for x in range(-half_size, half_size+1):

            if (x, y) in map.keys():
                print(map[(x, y)], end="",sep="")
            else:
                print(" ", end="", sep="")
        print()


def part2_oxygen_steps(map):
    steps = 0
    while "." in map.values():
        draw_map(map)
        new_map = copy.deepcopy(map)
        for pos in map:
            if map[pos] == "O":
                if map[(pos[0],pos[1]+1)] == ".":
                    new_map[(pos[0],pos[1]+1)] = "O"

                if map[(pos[0],pos[1]-1)] == ".":
                    new_map[(pos[0],pos[1]-1)] = "O"

                if map[(pos[0]+1,pos[1])] == ".":
                    new_map[(pos[0]+1,pos[1])] = "O"

                if map[(pos[0]-1,pos[1])] == ".":
                    new_map[(pos[0]-1,pos[1])] = "O"
        map = copy.deepcopy(new_map)
        steps +=1
    return steps


class Droid_control:
    def __init__(self):
        self.moves = []
        self.map = {(0,0):"."}
        self.pos = {"x":0, "y":0}
        self.next_move = None
        self.north = 1
        self.south = 2
        self.east = 4
        self.west = 3

    def draw_map(self, map_size=20):
        size = map_size
        half_size = size // 2
        # draw 11x11 around the droid
        for y in range(self.pos["y"]-half_size, self.pos["y"]+half_size+1):
            for x in range(self.pos["x"]-half_size, self.pos["x"]+half_size+1):

                if x == self.pos["x"] and y == self.pos["y"]:
                    print("D", end="", sep="")
                    continue

                if (x, y) in self.map.keys():
                    print(self.map[(x, y)], end="",sep="")
                else:
                    print(" ", end="", sep="")
            print()

    def undo(self):
        global part2
        global part1

        try:
            prev_move = self.moves.pop()
        except:
            # back at the start, calculate the oxygen flow
            self.draw_map(map_size=42)
            part2 = part2_oxygen_steps(self.map)
            print("part1 - {}".format(part1))
            print("part2 - {}".format(part2))
            exit()


        if prev_move == self.north:
            self.next_move = self.south

        elif prev_move == self.south:
            self.next_move = self.north

        elif prev_move == self.west:
            self.next_move = self.east

        elif prev_move == self.east:
            self.next_move = self.west

    def droid_ai(self):
        global part1
        up = (self.pos["x"], self.pos["y"]-1)
        down = (self.pos["x"], self.pos["y"]+1)
        left = (self.pos["x"]-1, self.pos["y"])
        right = (self.pos["x"]+1, self.pos["y"])
        current = (self.pos["x"], self.pos["y"])

        #check if we've found the oxygen system
        if current in self.map.keys() and self.map[(self.pos["x"], self.pos["y"])] == 'O':
            print("Oxygen at {}".format(self.pos))
            print(self.moves)
            part1 = len(self.moves)

        print(self.moves)

        # try an available side
        if up not in self.map.keys():
            self.next_move = self.north
            self.moves.append(self.next_move)
        elif down not in self.map.keys():
            self.next_move = self.south
            self.moves.append(self.next_move)
        elif left not in self.map.keys():
            self.next_move = self.west
            self.moves.append(self.next_move)
        elif right not in self.map.keys():
            self.next_move = self.east
            self.moves.append(self.next_move)
        else:
            self.undo()

    def log_status_code(self, status, last_move):
        status = int(status)
        if status == 0: # hit a wall
            print("Hit wall")
            if last_move == self.north: # North
                self.map[(self.pos["x"], self.pos["y"]-1)] = '#'
            if last_move == self.east: # East
                self.map[(self.pos["x"]+1, self.pos["y"])] = '#'
            if last_move == self.south: # South
                self.map[(self.pos["x"], self.pos["y"]+1)] = '#'
            if last_move == self.west: # West
                self.map[(self.pos["x"]-1, self.pos["y"])] = '#'
            self.moves.pop()

        elif status == 1: # moved one step in direction
            if last_move == self.north: # North
                self.pos["y"] -= 1
            if last_move == self.east: # East
                self.pos["x"] += 1
            if last_move == self.south: # South
                self.pos["y"] += 1
            if last_move == self.west: # West
                self.pos["x"] -= 1
            self.map[(self.pos["x"], self.pos["y"])] = '.'

        elif status == 2: # move, location is the oxygen system
            if last_move == self.north: # North
                self.pos["y"] -= 1
            if last_move == self.east: # East
                self.pos["x"] += 1
            if last_move == self.south: # South
                self.pos["y"] += 1
            if last_move == self.west: # West
                self.pos["x"] -= 1
            self.map[(self.pos["x"], self.pos["y"])] = 'O'

        else:
            print("Don't know status {}".format(status))


class Interpreter:
    def __init__(self, program, debug=False):
        self.program = program
        self.pos = 0
        self.debug = debug
        self.parameter_mode = 0
        self.relative_base = 0
        self.last_move = None
        self.droid_control = Droid_control()

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
            return self.program[self.relative_base+pos]

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
        self.droid_control.draw_map()
        print("1 = North, 4 = East, 2 = South, 3 = West")
        #get_input = int(input("Input: "))
        self.droid_control.droid_ai()
        get_input = self.droid_control.next_move
        assert get_input in range(1, 5)
        self.last_move = get_input

        if self.debug:
            if self.parameter_mode != 2:
                print("@{} Input {} to ({}){}".format(self.pos, get_input,dst, dst))
            else:
                print("@{} Input {} to ({}){}".format(self.pos, get_input, dst+self.relative_base, dst))
        self.write(dst, get_input)

    def output(self, modes):
        self.parameter_mode = modes.pop()
        src = self.get_next()
        # output the value at src
        a = self.retrieve(src)
        print("\t@{} Output: ({}){}".format(self.pos, src, a))
        self.droid_control.log_status_code(a, self.last_move)

    def jump_if_true(self, modes):
        # if true then set program pointer to val
        self.parameter_mode = modes.pop()
        a_1 = self.get_next()
        a = self.retrieve(a_1)
        self.parameter_mode = modes.pop()
        b_1 = self.get_next()
        b = self.retrieve(b_1)

        if self.debug:
            print("@{} JIT {} - ({}){} to ({}){}".format(self.pos, a!=0, a_1, a, b_1, b))
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
            print("@{} JIF {} - ({}){} to ({}){}".format(self.pos, a==0, a_1, a, b_1, b))
        if a == 0:
            self.pos = b
            # pos it automaticly incremented after each cycle, this stop the incrementation after a jump
            self.pos -=1

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
            s_instr = '0'*(5-len(s_instr)) + s_instr

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



if __name__ == "__main__":
    # Part
    code = prog_to_dict(read_input())
    #code = test_prog2()
    interpreter = Interpreter(code, False)
    a = interpreter.run()
    #a = interpreter.test_prog_7()
    print(a)
    pass