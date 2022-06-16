def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

def read_input():
    with open("Day22-input.txt") as f:
        lines = f.readlines()
    return lines


def new_deck(size):
    return list(range(0, size))

def deal_new_stack(deck):
    deck.reverse()
    return deck

def cut_cards(deck, card_number):
    return deck[card_number:] + deck[:card_number]

def deal_with_increment(deck, increment):
    deck_size = len(deck)
    out = [None] * deck_size
    pos = 0
    for x in deck:
        out[(pos * increment) % deck_size] = x
        pos += 1
    return out

def run_sequence(deck, lines):
    for line in lines:
        # parse
        instr = line.strip().split(" ")[-2:]
        if instr[0] == 'new':
            deck = deal_new_stack(deck)
        if instr[0] == 'increment':
            deck = deal_with_increment(deck, int(instr[1]))
        if instr[0] == 'cut':
            deck = cut_cards(deck, int(instr[1]))
        print(instr)
    return deck


def reverse_deal(decksize, pos):
    return decksize-1-pos


def reverse_cut(decksize, pos, n):
    return (pos+n+decksize) % decksize

def reverse_increment(decksize, pos, n):
    # f(x) = x*n % s
    # f'(x) =  f(x) / n % s
    #increment = self.pos = (self.pos*n) % self.size
    return modinv(n,decksize) * pos % decksize


def reverse_shuffle(pos_, decksize): #  f(x)
    pos = pos_
    steps = read_input()
    steps.reverse()
    for line in steps:
        instr = line.strip().split(" ")[-2:]
        if instr[0] == 'new':
            pos = reverse_deal(decksize, pos)
        if instr[0] == 'increment':
            pos = reverse_increment(decksize, pos, int(instr[1]))
        if instr[0] == 'cut':
            pos = reverse_cut(decksize, pos, int(instr[1]))
    return pos


class Part2_shuffle:
    def __init__(self, size, pos):
        self.size = size
        self.pos = pos
        self.previous_pos = {self.pos: 0}
        self.prevs = []
        self.line_c = 1


    def increment_n(self, n):
        self.pos = (self.pos*n) % self.size

    def cut(self, n):
        self.pos = (self.pos-n) % self.size

    def deal_into(self):
        self.pos = self.size - self.pos - 1

    def run(self, lines):
        for line in lines:
            # parse
            instr = line.strip().split(" ")[-2:]
            if instr[0] == 'new':
                self.deal_into()
            if instr[0] == 'increment':
                self.increment_n(int(instr[1]))
            if instr[0] == 'cut':
                self.cut(int(instr[1]))
            # print(instr)
            if self.pos in self.previous_pos:
                self.prevs.append((self.previous_pos[self.pos], self.pos, self.line_c))
            self.previous_pos[self.pos] = self.line_c
            self.line_c += 1
        return self.pos





def test_prog3():
    lines = [
        "deal into new stack",
        "cut -2",
        "deal with increment 7",
        "cut 8",
        "cut -4",
        "deal with increment 7",
        "cut 3",
        "deal with increment 9",
        "deal with increment 3",
        "cut -1"
    ]
    deck = new_deck(10)
    deck = run_sequence(deck, lines)
    print(deck)

def part2_test_prog1():
    lines = [
        "deal with increment 7",
        "deal into new stack",
        "deal into new stack"
    ]
    s = Part2_shuffle(10, 7)
    pos = s.run(lines)
    print(pos)

def part2_test_prog2():
    lines = [
        "cut 6",
        "deal with increment 7",
        "deal into new stack"
    ]
    watch_value = 0
    s = Part2_shuffle(10, watch_value)
    test_deck = new_deck(10)

    s.cut(6)
    test_deck = cut_cards(test_deck, 6)
    assert s.pos == [x for x in range(len(test_deck)) if test_deck[x] == watch_value][0]

    s.increment_n(7)
    test_deck = deal_with_increment(test_deck, 7)
    assert s.pos == [x for x in range(len(test_deck)) if test_deck[x] == watch_value][0]

    s.deal_into()
    test_deck = deal_new_stack(test_deck)
    assert s.pos == [x for x in range(len(test_deck)) if test_deck[x] == watch_value][0]


    print(s.pos)
    s.deal_into()
    print(s.pos)
    # pos = s.run(lines)
    print(s.pos)

def part1():
    deck = new_deck(10007)
    inp = read_input()
    deck = run_sequence(deck, inp)
    for x in range(0,len(deck)):
        if deck[x] == 2019:
            print(x)
            break

def part2():
    prevs = []
    D = 119315717514047
    #   119315717514047
    to_find = 2020
    f = reverse_shuffle
    X = 2020
    Y = f(X, D)
    Z = f(Y, D)
    A = (Y - Z) * modinv(X - Y + D, D) % D
    B = (Y - A * X) % D

    n = 101741582076661
    #   101741582076661
    print((pow(A, n, D)*X + (pow(A, n, D)-1) * modinv(A-1, D) * B) % D)
    # 2980102096390
    # 91967327971097
if __name__== "__main__":
    # part1()
    part2()
    #print(reverse_shuffle(4485, 10007))