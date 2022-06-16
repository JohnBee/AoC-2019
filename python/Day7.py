import copy
import itertools


def read_input():
    with open("Day7-input.txt") as f:
        input = f.readline()
        prog = list(map(int, input.split(",")))
    return prog


class Interpreter:
    def __init__(self, program, phase, debug=False):
        self.program = copy.deepcopy(program)
        self.pos = 0
        self.debug = debug
        self.parameter_mode = 0
        self.last_output = None
        self.phase = phase

    def first_inputs(self, input):
        self.phase_setting_and_input_signal = [self.phase, input]

    def update_inputs(self, input):
        self.phase_setting_and_input_signal = [input]

    def incr(self):
        self.pos += 1
        return

    def retrieve(self, pos):
        # returns value dependant on parameter mode
        if self.parameter_mode == 0:
            return self.program[pos]
        if self.parameter_mode == 1:
            return pos

    def get_next(self):
        self.incr()
        out = self.program[self.pos]
        return out

    def write(self, pos, val):
        if self.debug:
            print("Write {} to {}".format(val, pos))
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

        if self.debug:
            print("#{} = ({}){} + ({}){}".format(c, a_1, a, b_1, b))
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

        if self.debug:
            print("#{} = ({}){} * ({}){}".format(c, a_1, a, b_1, b))
        self.write(c, a * b)

    def get_input(self, modes):
        dst = self.get_next()
        # get input should return a value from some input
        #get_input = int(input("Input: "))
        get_input = self.phase_setting_and_input_signal.pop(0)
        if self.debug:
            print("Input: {}".format(get_input))
        self.write(dst, get_input)

    def output(self, modes):
        self.parameter_mode = modes.pop()
        src = self.get_next()
        # output the value at src
        a = self.retrieve(src)
        print("\tOutput: ({}){}".format(src, a))
        self.last_output = a
        return self.last_output
        # if a != 0:
        #     print(self.program)
        #     pass

    def jump_if_true(self, modes):
        # if true then set program pointer to val
        self.parameter_mode = modes.pop()
        a_1 = self.get_next()
        a = self.retrieve(a_1)
        self.parameter_mode = modes.pop()
        b_1 = self.get_next()
        b = self.retrieve(b_1)

        if self.debug:
            print("JIT {} - ({}){} to ({}){}".format(a!=0, a_1, a, b_1, b))
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
            print("JIF {} - ({}){} to ({}){}".format(a==0, a_1, a, b_1, b))
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
        if self.debug:
            print("#{} = ({}){} < ({}){}".format(a < b, a_1, a, b_1, b))

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
        if self.debug:
            print("#{} = ({}){} == ({}){}".format(a == b, a_1, a, b_1, b))

        if a == b:
            self.write(c, 1)
        else:
            self.write(c, 0)

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
            return self.output(s_instr)
        elif opcode == 5:
            self.jump_if_true(s_instr)
        elif opcode == 6:
            self.jump_if_false(s_instr)
        elif opcode == 7:
            self.less_than(s_instr)
        elif opcode == 8:
            self.equals(s_instr)
        else:
            print("Dont know opcode: {} at {}".format(opcode, self.pos))

    def run(self):
        if self.debug:
            print(self.program)

        while self.program[self.pos] != 99:
            if self.decode(self.program[self.pos]) != None:
                self.incr()
                return self.last_output
            self.incr()
            # print(self.program)
        print("Halt!")
        return self.last_output

def load_test_prog1():
    return [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
def load_test_prog2():
    return [3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0]
def load_test_prog3():
    return [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
def load_test_prog4():
    return [3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]


if __name__ == "__main__":
    # Part 2
    code = read_input()
    #code = load_test_prog4()
    highest = 0
    base_phase_sequence = [9,8,7,6,5]
    perms = list(map(list, list(itertools.permutations(base_phase_sequence))))
    #perms = [base_phase_sequence]
    print(perms)
    for phase_sequence in perms:
        initial = 0
        #create interpreters
        a_i = Interpreter(code, phase_sequence.pop(0), True)
        b_i = Interpreter(code, phase_sequence.pop(0), True)
        c_i = Interpreter(code, phase_sequence.pop(0), True)
        d_i = Interpreter(code, phase_sequence.pop(0), True)
        e_i = Interpreter(code, phase_sequence.pop(0), True)

        # run feedback loop

        # first run
        # run 10 times
        def run_amp_loop(initial):
            a_i.update_inputs(initial)
            a = a_i.run()
            b_i.update_inputs(a)
            b = b_i.run()
            c_i.update_inputs(b)
            c = c_i.run()
            d_i.update_inputs(c)
            d = d_i.run()
            e_i.update_inputs(d)
            e = e_i.run()
            return e


        # first run to setup
        # when the amps are first run a setup routine is used to initialise the phase
        # so the first input setup it different to the other input updates as the phase isnt required
        a_i.first_inputs(initial)
        a = a_i.run()
        b_i.first_inputs(a)
        b = b_i.run()
        c_i.first_inputs(b)
        c = c_i.run()
        d_i.first_inputs(c)
        d = d_i.run()
        e_i.first_inputs(d)
        e = e_i.run()
        initial = e
        if initial > highest:
            highest = initial

        for i in range(0,10):
            initial = run_amp_loop(initial)
            if initial > highest:
                highest = initial
    print("highest: {}".format(highest))
    #print([a,b,c,d,e])

    # Part 2
    #part2()
    pass