def read_input():
    with open("Day5-input.txt") as f:
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
        get_input = int(input("Input: "))
        self.write(dst, get_input)

    def output(self, modes):
        self.parameter_mode = modes.pop()
        src = self.get_next()
        # output the value at src
        a = self.retrieve(src)
        print("\tOutput: {}".format(a))
        if a != 0:
            print(self.program)
            pass

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
            self.output(s_instr)
        elif opcode == 5:
            self.jump_if_true(s_instr)
        elif opcode == 6:
            self.jump_if_false(s_instr)
        elif opcode == 7:
            self.less_than(s_instr)
        elif opcode == 8:
            self.equals(s_instr)
        else:
            print("Dont know opcode: {}".format(opcode))

    def test_prog_1(self):
        # is input equal to 8
        self.program = [3,9,8,9,10,9,4,9,99,-1,8]
        a = self.run()
        # output should be equal to 1

    def test_prog_2(self):
        # is input less than 8
        self.program = [3,9,7,9,10,9,4,9,99,-1,8]
        a = self.run()

    def test_prog_3(self):
        # is input equal to 8
        self.program = [3,3,1108,-1,8,3,4,3,99]
        a = self.run()

    def test_prog_4(self):
        # is input less than 8
        self.program = [3,3,1107,-1,8,3,4,3,99]
        a = self.run()

    def test_prog_5(self):
        # jump test 0 if zero, 1 if non zero
        self.program = [3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9]
        a = self.run()

    def test_prog_6(self):
        # jump test 0 if zero, 1 if non zero
        self.program = [3,3,1105,-1,9,1101,0,0,12,4,12,99,1]
        a = self.run()

    def test_prog_7(self):
        # ouput 999 if below 8, output 1000 if equal to 8, output 1001 if greater than 8
        self.program = [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
                        1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
                        999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]
        a = self.run()


    def run(self):
        if self.debug:
            print(self.program)

        while self.program[self.pos] != 99:
            self.decode(self.program[self.pos])
            self.incr()

            # print(self.program)
        print("Halt!")
        return self.program




def part2():
    for i in range(99):
        for j in range(99):
            code = fix_input(read_input(), i, j)
            interpreter = Interpreter(code)
            a = interpreter.run()
            if interpreter.program[0] == 19690720:
                print("part2 = {}".format(100 * i + j))
                return
    print("None found")
    return


if __name__ == "__main__":
    # Part
    code = read_input()
    interpreter = Interpreter(code, True)
    a = interpreter.run()
    #a = interpreter.test_prog_7()
    print(a)

    # Part 2
    #part2()
    pass