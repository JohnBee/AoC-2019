import pprint
def prog_to_dict(program):
    return dict(zip(range(len(program)), program))


def read_input():
    with open("Day11-input.txt") as f:
        input = f.readline()
        prog = list(map(int, input.split(",")))
    return prog


class Turtle_map:
    def __init__(self, debug=False):
        self.pos = (0, 0)
        self.direction = 0
        self.paint_map = {(0, 0): 1}
        self.debug = debug

    def get_tile_colour(self):
        col = None
        if self.pos in self.paint_map.keys():
            col = self.paint_map[self.pos]
        else:
            col = 0
        if self.debug:
            print("Tile at {} is {}".format(self.pos, col))
        return col

    def move_forward(self):
        if self.direction == 0:
            self.pos = (self.pos[0], self.pos[1]-1)
        if self.direction == 1:
            self.pos = (self.pos[0]+1, self.pos[1])
        if self.direction == 2:
            self.pos = (self.pos[0], self.pos[1]+1)
        if self.direction == 3:
            self.pos = (self.pos[0]-1, self.pos[1])

    def move_turtle_direction(self, direction):
        assert (direction == 0 or direction == 1)
        if direction == 0:
            # turn left 90'
            self.direction = (self.direction - 1) % 4

        if direction == 1:
            # turn right 90'
            self.direction = (self.direction + 1) % 4
        self.move_forward()

        if self.debug:
            if direction == 0:
                print("Turning Left, new pos: {}, facing: {}".format(self.pos, self.direction))
            if direction == 1:
                print("Turning Right, new pos: {}, facing: {}".format(self.pos, self.direction))

    def paint_tile(self, colour):
        assert (colour == 0 or colour == 1)
        self.paint_map[self.pos] = colour
        if self.debug:
            print("Painting tile at {} colour {}".format(self.pos, colour))


class Interpreter:
    def __init__(self, program, debug=False):
        self.program = program
        self.pos = 0
        self.debug = debug
        self.parameter_mode = 0
        self.relative_base = 0
        self.turtle_bot = Turtle_map(debug=True)
        self.move_or_paint = 0

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
        #get_input = int(input("Input: "))
        get_input = self.turtle_bot.get_tile_colour()
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
        if self.move_or_paint == 0:
            self.turtle_bot.paint_tile(a)
        if self.move_or_paint == 1:
            self.turtle_bot.move_turtle_direction(a)

        # change mode for next output
        self.move_or_paint = (self.move_or_paint + 1) % 2

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


def part2_draw_paint_map(paint_map):
    # find top left
    top_left = [float('inf'), float('inf')]
    bot_right = [0, 0]
    for key in paint_map.keys():
        if key[0] <= top_left[0]:
            top_left[0] = key[0]
        if key[1] <= top_left[1]:
            top_left[1] = key[1]
        if key[0] >= bot_right[0]:
            bot_right[0] = key[0]
        if key[1] >= bot_right[1]:
            bot_right[1] = key[1]

    for y in range(top_left[1], bot_right[1]+1):
        for x in range(top_left[0], bot_right[0]+1):
            if (x, y) in paint_map.keys():
                if paint_map[(x, y)] == 0:
                    print(".", end='', sep='')
                else:
                    print('#', end='', sep='')
            else:
                print(".", end='',sep='')
        print()





if __name__ == "__main__":
    # Part
    code = prog_to_dict(read_input())
    #code = test_prog2()
    interpreter = Interpreter(code, False)
    a = interpreter.run()
    #a = interpreter.test_prog_7()
    print(len(interpreter.turtle_bot.paint_map.keys()))
    print(interpreter.turtle_bot.paint_map)
    part2_draw_paint_map(interpreter.turtle_bot.paint_map)
    pass