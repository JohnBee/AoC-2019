import math


def extract_asteroids(lines):
    asteroids = []
    y = 0
    for line in lines:
        x = 0
        for a in line.strip():
            if a == '#':
                asteroids.append((x, y))
            x += 1
        y += 1
    return asteroids


def read_input():
    with open("Day10-input.txt")as f:
        lines = f.readlines()
        lines = list(map(lambda x: x.strip(), lines))
    return extract_asteroids(lines)


def calc_dist(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)


def on_line(p1, p2, p3):
    # test if p3 sits between p1 and p2
    if math.isclose(calc_dist(p1, p3) + calc_dist(p2, p3), calc_dist(p1, p2)):
        #print("{} == {}".format(calc_dist(p1, p3) + calc_dist(p2, p3), calc_dist(p1, p2)))
        return True
    return False


def vision_obscured(p1, p2, asteroid_map):
    # test if vision is obscured on the map between p1 and p2
    for asteroid in asteroid_map:
        if asteroid != p1 and asteroid != p2 and on_line(p1, p2, asteroid):

            return True # vision is obscured
    return False


def calc_visible_asteroids(p1, asteroid_map):
    total = 0
    for asteroid in asteroid_map:
        if not vision_obscured(p1, asteroid, asteroid_map) and p1 != asteroid:
            total += 1
    return total


def list_visible_asteroids(p1, asteroid_map):
    out = []
    for asteroid in asteroid_map:
        if not vision_obscured(p1, asteroid, asteroid_map) and p1 != asteroid:
            out.append(asteroid)
    return out


def sort_asteroid_by_angle(p1, asteroids):
    angs = {}
    # order asteroids by angle
    # calc the angle of each point
    for asteroid in asteroids:
        dy = asteroid[1] - p1[1]
        dx = asteroid[0] - p1[0]
        theta = math.atan2(dy, dx)
        theta *= 180 / math.pi
        theta += 90
        if theta < 0:
            theta += 360
        angs[asteroid] = theta
    asteroids.sort(key=lambda x: angs[x])
    return asteroids


def part1(asteroid_map):
    highest = 0
    loc = None
    for asteroid in asteroid_map:
        total = calc_visible_asteroids(asteroid, asteroid_map)
        if total > highest:
            highest = total
            loc = asteroid
    return highest, loc


def part2(asteroid_map):
    # get visible asteroids
    p1 = (17, 22)
    #p1 = (3,4)
    counter = 0
    last_asteroid = None
    while counter < 200 and len(asteroid_map) > 1:
        visisble_asteroids = list_visible_asteroids(p1, asteroid_map)
        visisble_asteroids = sort_asteroid_by_angle(p1, visisble_asteroids)
        for asteroid in visisble_asteroids:
            counter += 1
            last_asteroid = asteroid
            print("{}th removed: {}".format(counter, last_asteroid))
            asteroid_map.remove(asteroid)
            if counter == 200:
                break
    print(last_asteroid[0]*100 + last_asteroid[1])



def load_test1():
    # (3,4) 8
    map = [ ".#..#",
            ".....",
            "#####",
            "....#",
            "...##"]
    return extract_asteroids(map)

def load_test2():
    # (5,8) 33
    map = [ "......#.#.",
            "#..#.#....",
            "..#######.",
            ".#.#.###..",
            ".#..#.....",
            "..#....#.#",
            "#..#....#.",
            ".##.#..###",
            "##...#..#.",
            ".#....####"]
    return extract_asteroids(map)


def load_test3():
    # (1, 2) 35
    map = [ "#.#...#.#.",
            ".###....#.",
            ".#....#...",
            "##.#.#.#.#",
            "....#.#.#.",
            ".##..###.#",
            "..#...##..",
            "..##....##",
            "......#...",
            ".####.###."]
    return extract_asteroids(map)


def load_test4():
    # (6, 3) 41
    map = [ ".#..#..###",
            "####.###.#",
            "....###.#.",
            "..###.##.#",
            "##.##.#.#.",
            "....###..#",
            "..#.#..#.#",
            "#..#.#.###",
            ".##...##.#",
            ".....#.#.."]
    return extract_asteroids(map)


def load_test5():
    # (11, 13) 210
    map = [ ".#..##.###...#######",
            "##.############..##.",
            ".#.######.########.#",
            ".###.#######.####.#.",
            "#####.##.#.##.###.##",
            "..#####..#.#########",
            "####################",
            "#.####....###.#.#.##",
            "##.#################",
            "#####.##.###..####..",
            "..######..##.#######",
            "####.##.####...##..#",
            ".#####..#.######.###",
            "##...#.##########...",
            "#.##########.#######",
            ".####.#.###.###.#.##",
            "....##.##.###..#####",
            ".#.#.###########.###",
            "#.#.#.#####.####.###",
            "###.##.####.##.#..##"]
    return extract_asteroids(map)


if __name__ == "__main__":
    asteroid_map = read_input()
    #asteroid_map = load_test1()
    #asteroid_map = load_test3()
    #asteroid_map = load_test5()
    #print(calc_visible_asteroids((3, 4), asteroid_map))
    print(part2(asteroid_map))