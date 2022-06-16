import pprint
import copy
import itertools

def prog_to_dict(program):
    return dict(zip(range(len(program)), program))

def read_input():
    with open("Day21-input.txt") as f:
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
        # get_input = int(input("Input: "))
        assert self.input_buffer != []
        get_input = self.input_buffer.pop(0)
        if type(get_input) == str:
            get_input = ord(get_input)
        else:
            assert get_input == 10
        # print("Input: {}".format(chr(get_input)))
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
        # print("\t@{} Output: ({}){}".format(self.pos, src, a))
        if a > 255:
            print(a)
            exit()
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
        print("@{} Halt!".format(self.pos))
        return self.program


def display_output(output):
    for p in output:
        print(chr(p), end="")


def input_to_ascci(lines):
    output = []
    for line in lines:
        for char in line:
            output.append(char)
        output.append(10)
    return output

def generate_program():
    ops = ["AND", "OR", "NOT"]
    inps = ["A", "B", "C","D"]
    regs = ["T","J"]
    regs_combs = [(a,b) for a in inps+regs for b in regs]
    ops_regs_combs = [(a, b[0], b[1]) for a in ops for b in regs_combs]
    ops_regs_combs.remove(('OR','J','J'))
    ops_regs_combs.remove(('OR', 'T', 'T'))
    ops_regs_combs.remove(('AND', 'J', 'J'))
    ops_regs_combs.remove(('AND', 'T', 'T'))
    progs = []
    for ops in ops_regs_combs:
        progs.append(ops[0]+" "+ops[1]+" "+ops[2])
    return itertools.combinations_with_replacement(progs, 4)

def test_prog1():
    lines = [
        "NOT A J",
        "NOT B T",
        "AND T J",
        "NOT C T",
        "AND T J",
        "AND D J",
        "WALK"
    ]
    return input_to_ascci(lines)

def test_prog2():
    lines = [
        "NOT B J",
        "WALK"
    ]
    return input_to_ascci(lines)

def my_prog():
    lines = [
        "NOT A J", # jump immediately if theres no floor infront
        "NOT D T",
        "NOT T T",
        "OR T J",
        "WALK"

    ]
    return input_to_ascci(lines)

def part1():
    # (!A v !B v !C) ^ D
    lines = [
        "NOT A T",
        "NOT B J",
        "OR T J", # !A v !B
        "NOT C T",# !C
        "OR T J", # !A v !B v !c
        "AND D J",
        "WALK"

    ]
    return input_to_ascci(lines)

def part2():
    # jumpsd 5 spaces
    #(!A v !B v !C) ^ D
    lines = [
        "NOT A T",
        "NOT B J",
        "OR T J",  # !A v !B
        "NOT C T",  # !C
        "OR T J",  # !A v !B v !c
        "AND D J", # (!A v !B v !C) ^ D
        "NOT E T",
        "NOT T T", # E
        "OR H T", # T = E or H
        "AND T J", #(!A v !B v !c) ^ D ^ (E v H)
        "RUN"

    ]
    return input_to_ascci(lines)


if __name__ == "__main__":
    # Part
    code = prog_to_dict(read_input())

    prog = part2()
    interpreter = Interpreter(copy.deepcopy(code), False)
    interpreter.input_buffer = prog
    a = interpreter.run()
    display_output(interpreter.output_buffer)
    pass

# Droid jumps 4 tiles infront
# always check that tile 4 can be landed on
# jump if D i safe
#
