import pprint
def prog_to_dict(program):
    return dict(zip(range(len(program)), program))

def read_input():
    with open("Day13-input.txt") as f:
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
        self.output_buffer = []
        self.screen = {}
        self.score = 0

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

    def auto_player(self):
        #get ball position
        ball_pos = None
        paddle_pos = None
        for k in self.screen.keys():
            if self.screen[k] == 'ball':
                ball_pos = k
            if self.screen[k] == 'paddle':
                paddle_pos = k
                break

        if paddle_pos[0] < ball_pos[0]:
            return 1
        if paddle_pos[0] == ball_pos[0]:
            return 0
        if paddle_pos[0] > ball_pos[0]:
            return -1


    def get_input(self, modes):
        self.parameter_mode = modes.pop()
        dst = self.get_next()
        if self.parameter_mode == 2:
            dst += self.relative_base

        # Draw the screen
        self.draw_screen()
        # get input should return a value from some input
        #get_input = int(input("Input: "))

        # set input to move left or right if in line with the ball or not

        get_input = self.auto_player()
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
        if self.debug:
            print("\t@{} Output: ({}){}".format(self.pos, src, a))
        self.output_buffer.append(a)
        if len(self.output_buffer) == 3:
            self.draw_object()

    def draw_screen(self):
        # find top left and bottom right
        top_left_x, top_left_y = (float('inf'), float('inf'))
        bottom_right_x, bottom_right_y = (0, 0)
        for x,y in self.screen.keys():
            if x < top_left_x:
                top_left_x = x
            if y < top_left_y:
                top_left_y = y
            if x > bottom_right_x:
                bottom_right_x = x
            if y > bottom_right_y:
                bottom_right_y = y
        print("Score: {}".format(self.score))
        for y in range(top_left_y, bottom_right_y+1):
            for x in range(top_left_x, bottom_right_x+1):
                if self.screen[(x,y)] == 'empty':
                    print('.',end='', sep='')
                if self.screen[(x,y)] == 'wall':
                    print('█',end='', sep='')
                if self.screen[(x,y)] == 'block':
                    print('▒',end='', sep='')
                if self.screen[(x,y)] == 'paddle':
                    print('-',end='', sep='')
                if self.screen[(x,y)] == 'ball':
                    print('o',end='', sep='')
            print()
        max_score = len([self.screen[k] for k in self.screen.keys() if self.screen[k] == 'block'])*33
        print("Max_score = {}".format(max_score))


    def draw_object(self):
        x = self.output_buffer.pop(0)
        y = self.output_buffer.pop(0)
        o = self.output_buffer.pop(0)

        if x == -1 and y == 0:
            self.score = o
            return

        if o == 0:
            o = 'empty'
        elif o == 1:
            o = 'wall'
        elif o == 2:
            o = 'block'
        elif o == 3:
            o = 'paddle'
        elif o == 4:
            o = 'ball'
        self.screen[(x, y)] = o

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
        print("Game Over - Score: {}".format(self.score))
        print("@{} Halt!".format(self.pos))
        return self.program



if __name__ == "__main__":
    # Part
    code = prog_to_dict(read_input())
    # insert quarters
    code[0] = 2

    interpreter = Interpreter(code, False)
    a = interpreter.run()
    #a = interpreter.test_prog_7()
    print(a)

    pass