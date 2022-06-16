
def read_input():
    with open("Day2-input.txt") as f:
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

    def incr(self):
        self.pos += 1
        return

    def get_next(self):
        self.incr()
        out = self.program[self.pos]
        return out

    def write(self, pos, val):
        if self.debug:
            print("Write {} to {}".format(val, pos))
        self.program[pos] = val

    def add(self):
        a = self.get_next()
        b = self.get_next()
        if self.debug:
            print("{} + {}".format(self.program[a], self.program[b]))
        self.write(self.get_next(), self.program[a]+self.program[b])

    def mul(self):
        a = self.get_next()
        b = self.get_next()
        if self.debug:
            print("{} * {}".format(self.program[a], self.program[b]))
        self.write(self.get_next(), self.program[a]*self.program[b])

    def run(self):
        while self.program[self.pos] != 99:
            if self.program[self.pos] == 1:
                self.add()
            elif self.program[self.pos] == 2:
                self.mul()
            else:
                self.incr()

            #print(self.program)
        return self.program

def part2():
    for i in range(99):
        for j in range(99):
            code = fix_input(read_input(), i, j)
            interpreter = Interpreter(code)
            a = interpreter.run()
            if interpreter.program[0] == 19690720:
                print("part2 = {}".format(100*i+j))
                return
    print("None found")
    return

if __name__ == "__main__":
    # Part 1
    code = fix_input(read_input(), 12, 2)
    print(code)
    interpreter = Interpreter(code, True)
    a = interpreter.run()
    print(a)

    # Part 2
    part2()
    pass