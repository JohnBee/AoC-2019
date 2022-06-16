import pprint
import copy
import logging
import threading
import time

def prog_to_dict(program):
    return dict(zip(range(len(program)), program))

def read_input():
    with open("Day23-input.txt") as f:
        input = f.readline()
        prog = list(map(int, input.split(",")))
    return prog

class NATHandler:
    def __init__(self, network_list,  message_db=None):
        self.last_message = None
        self.message_db = message_db
        self.network_list = network_list
        self.sent_messages = []
        self._lock = threading.Lock

    def network_is_idle(self):
        idle = True
        logging.info("Checking for Idle")
        for i in range(len(self.network_list)):
            logging.info("Read_Counter %s %s", self.network_list[i].read_counter, self.message_db.check_any_messages(i))
            if self.network_list[i].read_counter > 10 and not self.message_db.check_any_messages(i):
                idle = True
            else:
                idle = False
                break
        return idle

    def locked_write(self, message):
        self.last_message = message

    def run(self):
        while True:
            if self.network_is_idle() and self.last_message != None:
                logging.info("Unblocking")
                self.message_db.locked_write(0, self.last_message)
                # test part 2
                logging.info("Nat sent to 0: %s", self.last_message)
                if self.sent_messages and len(self.sent_messages) >=2 and self.last_message[1] == self.sent_messages[-1][1]:
                    print(self.sent_messages)
                    print(f'Part2: {self.last_message[1]}')
                    exit()
                logging.info("Last unblocked messages")
                self.sent_messages.append(self.last_message)
            time.sleep(2)

class NetworkMessageDatabase:
    def __init__(self, nat_handler=None):
        self.messages = {}
        self._lock = threading.Lock()
        self._lock2 = threading.Lock()
        self.nat_last_message = None
        self.nat_handler = nat_handler

    def locked_write(self, recipient, message):
        with self._lock:
            assert type(message) == list
            #logging.info(message)
            if recipient in self.messages:
                self.messages[recipient] += message
            elif recipient != 255:
                self.messages[recipient] = message

            if recipient != 255:
                logging.info("writing to %s %s", recipient, len(self.messages[recipient]))

            if recipient == 255:
                logging.info(f'Part1: {message[1]}')
                self.nat_handler.locked_write(message)
                logging.info("Done nat write")

    def read(self, network_id):
        if network_id not in self.messages or not self.messages[network_id]:
            # no messages to be received
            return [-1]
        else:
            if network_id == 0:
                logging.info("Reading from 0 %s", self.messages[network_id])
            x = self.messages[network_id].pop(0)
            y = self.messages[network_id].pop(0)
            if network_id == 0:
                logging.info("Reading from 0 %s", len(self.messages[network_id]))
            return [x, y]


    def check_any_messages(self, network_id):
        if network_id in self.messages and self.messages[network_id] != []:
            return len(self.messages[network_id])
        else:
            return False


class Interpreter:
    def __init__(self, program, message_db, network_id, debug=False, ):
        self.program = program
        self.pos = 0
        self.debug = debug
        self.parameter_mode = 0
        self.relative_base = 0
        self.packet_to_send = []
        self.message_db = message_db
        self.output_buffer = []
        self.network_id = network_id
        self.setup_phase = True
        self.read_counter = 0
        self.input_buffer = []

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
        if self.setup_phase:
            get_input = self.network_id
            self.setup_phase = False
        else:
            if not self.input_buffer:
                self.input_buffer = self.message_db.read(self.network_id)

            get_input = self.input_buffer.pop(0)

            self.read_counter += 1
        if self.debug:
            print(f"Input: {get_input}")
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
        self.output_buffer.append(a)
        self.read_counter = 0
        if len(self.output_buffer) == 3:
            self.message_db.locked_write(self.output_buffer[0], self.output_buffer[1:])
            self.output_buffer = []

        if self.debug:
            print("\t@{} Output: ({}){}".format(self.pos, src, a))

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


def start_interpreter(interpreter_network_id, interpreter):
    logging.info("Thread starting, interpreter %s", interpreter_network_id)
    interpreter.run()
    logging.info("Thread finished, interpreter %s", interpreter_network_id)


def start_nat(i, nat):
    logging.info("Thread starting %s, NAT", i)
    nat.run()
    logging.info("Thread finished %s, NAT", i)


def test_part1():
    prog = prog_to_dict(read_input())
    message_db = NetworkMessageDatabase()
    a = Interpreter(copy.deepcopy(prog), message_db=message_db, network_id=1, debug=True)
    a.run()

def part1():
    # initialise the network
    # test_part1()
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                       datefmt="%H:%M:%S")

    prog = prog_to_dict(read_input())
    threads = []
    interpreters = []
    message_db = NetworkMessageDatabase()

    for i in range(0, 50):
        a = Interpreter(copy.deepcopy(prog), message_db=message_db, network_id=i, debug=False)
        interpreters.append(a)

    nat_handler = NATHandler(interpreters, message_db)
    message_db.nat_handler = nat_handler

    for i in range(0, 50):
        x = threading.Thread(target=start_interpreter, args=(i, interpreters[i]), daemon=True)
        threads.append(x)
        x.start()

    logging.info("Starting NAT")
    # nat = threading.Thread(target=start_nat, args=(i+1, nat_handler), daemon=False)
    # nat.start()
    nat_handler.run()

if __name__ == "__main__":
    # Part
    part1()
    pass