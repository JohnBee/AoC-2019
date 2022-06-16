import pprint
import copy

def prog_to_dict(program):
    return dict(zip(range(len(program)), program))

def read_input():
    with open("Day19-input.txt") as f:
        input = f.readline()
        prog = list(map(int, input.split(",")))
    return prog


def fix_input(prog, noun, verb):
    prog[1] = noun
    prog[2] = verb
    return prog


class Interpreter:
    def __init__(self, program, debug=False):
        self.program = program
        self.pos = 0
        self.debug = debug
        self.parameter_mode = 0
        self.relative_base = 0
        self.input_buffer = []
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
        assert self.input_buffer != []
        get_input = self.input_buffer.pop(0)

        if self.debug:
            print("Input: {}".format(get_input))
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
        if self.debug:
            print("\t@{} Output: ({}){}".format(self.pos, src, a))
        self.output_buffer.append(a)

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
        if self.debug:
            print("@{} Halt!".format(self.pos))
        return self.program#


def print_tractor_beam(output):
    # find top_left
    top_left = min(output)
    bottom_right = max(output)
    for y in range(top_left[1], bottom_right[1]):
        for x in range(top_left[0], bottom_right[0]):
            if output[(x,y)] == 1:
                print("#", end="")
            else:
                print(".", end="")
        print((x, y),sum([output[(x_i, y)] for x_i in range(top_left[0], bottom_right[0])]))


def get_sequence(output):
    sequence = []
    top_left = min(output)
    bottom_right = max(output)
    for y in range(top_left[1], bottom_right[1]):
        seq = sum([output[(x_i, y)] for x_i in range(top_left[0], bottom_right[0])])
        sequence.append(seq)
    return sequence


def check_coords(x, y, code_):
    if x < 0 or y < 0:
        return 0
    code = copy.deepcopy(code_)
    interpreter = Interpreter(code, False)
    p_input = [x, y]
    interpreter.input_buffer = [p_input[0], p_input[1]]
    a = interpreter.run()
    o = interpreter.output_buffer.pop(0)
    return o

def print_range(top_left, bot_right, code):
    for y in range(top_left[1], bot_right[1]):
        for x in range(top_left[0], bot_right[0]):
            o = check_coords(x,y, code)
            if o:
                print("#", end="")
            else:
                print(".", end="")
        print()

def part1():
    prog_input = []
    for y in range(0, 50):
        for x in range(0, 50):
            prog_input.append((x, y))
    print(prog_input)
    output = {}
    # Part
    while prog_input:
        code = prog_to_dict(read_input())
        # code = test_prog2()
        interpreter = Interpreter(code, False)
        p_input = prog_input.pop(0)
        interpreter.input_buffer = [p_input[0], p_input[1]]
        a = interpreter.run()
        # a = interpreter.test_prog_7()
        output[p_input] = interpreter.output_buffer.pop(0)
    print(output)
    print(sum(list(output.values())))
    print_tractor_beam(output)

def part2():
    code = prog_to_dict(read_input())
    # print_range((0,0),(50,50), code)
    bot_left = [2, 4]
    # walk down bottom left corner
    while check_coords(bot_left[0], bot_left[1], code) != 1 or check_coords(bot_left[0]+99, bot_left[1]-99, code) != 1:
        # step down
        # print("Checking {}".format(bot_left))
        c = check_coords(bot_left[0], bot_left[1], code)
        if not c:
            bot_left[0] += 1
        else:
            bot_left[1] += 1

    assert check_coords(bot_left[0], bot_left[1], code)  # check bot left)
    assert check_coords(bot_left[0], bot_left[1]-99, code)  # check top left
    assert check_coords(bot_left[0]+99, bot_left[1]-99, code)  # check top right
    assert check_coords(bot_left[0]+99, bot_left[1], code)  # check bot right
    print(bot_left)
    print("Top_left {} {}".format(bot_left[0], bot_left[1] - 99))
    print("Part2: {}".format(bot_left[0]*10000 + (bot_left[1] - 99)))

if __name__ == "__main__":
    # part1()
    part2()
    pass