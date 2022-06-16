from itertools import combinations
import copy
import math

def lcm(a, b):
    return abs(a * b) // math.gcd(a, b)

class Moon:
    def __init__(self,x,y,z):
        self.pos = [x,y,z]
        self.velocity = [0,0,0]

    def __repr__(self):
        return str("pos=< x={}, y={}, z={} >, vel=< x={}, y={}, z={} >".format(self.pos[0], self.pos[1], self.pos[2],
                                                                               self.velocity[0], self.velocity[1], self.velocity[2]))

    def get_potential_energy(self):
        return sum(map(abs, self.pos))

    def get_kinetic_energy(self):
        return sum(map(abs, self.velocity))

    def to_tuple(self):
        return (tuple(self.pos), tuple(self.velocity))


class Simulation:
    def __init__(self, moons, debug=False):
        self.moons = moons
        self.step_counter = 0
        self.debug = debug
        self.save_states = []

    def get_x_coords(self):
        return [a.pos[0] for a in self.moons]

    def get_y_coords(self):
        return [a.pos[1] for a in self.moons]

    def get_z_coords(self):
        return [a.pos[2] for a in self.moons]

    def update_velocities(self):
        moon_pairs = list(map(list, list(combinations(self.moons, 2))))
        for moon1, moon2 in moon_pairs:
            for i in range(3):
                if moon1.pos[i] < moon2.pos[i]:
                    moon1.velocity[i] += 1
                    moon2.velocity[i] -= 1
                elif moon1.pos[i] > moon2.pos[i]:
                    moon1.velocity[i] -= 1
                    moon2.velocity[i] += 1

    def update_positions(self):
        for moon in self.moons:
            for i in range(3):
                moon.pos[i] += moon.velocity[i]

    def step_moons(self):
        self.update_velocities()
        self.update_positions()

    def total_energy(self):
        return sum([moon.get_potential_energy() * moon.get_kinetic_energy() for moon in self.moons])

    def print_sim_state(self):
        print("After {} steps:".format(self.step_counter))
        for moon in self.moons:
            print(moon)
        print("#{} Sum of Total Energy: {}".format(self.step_counter, self.total_energy()))

    def step(self):
        self.step_moons()
        self.step_counter += 1

        if self.debug:
            self.print_sim_state()

    def sim_to_tuple(self):
        return tuple([moon.to_tuple() for moon in self.moons])

    def save_state(self):
        self.save_states.append(self.sim_to_tuple())

    def in_prev_sate(self):
        if self.sim_to_tuple() in self.save_states:
            return True
        else:
            return False



if __name__ == "__main__":
    # < x = -16, y = 15, z = -9 >
    # < x = -14, y = 5, z = 4 >
    # < x = 2, y = 0, z = 6 >
    # < x = -3, y = 18, z = 9 >

    a = Moon(-16, 15, -9)
    b = Moon(-14, 5, 4)
    c = Moon(2, 0, 6)
    d = Moon(-3, 18, 9)
    # a = Moon(-1, 0, 2)
    # b = Moon(2, -10, -7)
    # c = Moon(4, -8, 8)
    # d = Moon(3, 5, -1)
    moons = [a, b, c, d]
    sim = Simulation(moons, debug=False)
    orig_x = tuple([a[0][0] for a in sim.sim_to_tuple()])
    orig_y = tuple([a[0][1] for a in sim.sim_to_tuple()])
    orig_z = tuple([a[0][2] for a in sim.sim_to_tuple()])
    periods = [None,None,None]
    while True:
        sim.step()
        new_x = tuple(sim.get_x_coords())
        new_y = tuple(sim.get_y_coords())
        new_z = tuple(sim.get_z_coords())

        if orig_x == new_x and periods[0] == None:
            periods[0] = sim.step_counter + 1

        if orig_y == new_y and periods[1] == None:
            periods[1] = sim.step_counter + 1

        if orig_z == new_z and periods[2] == None:
            periods[2] = sim.step_counter + 1

        if periods[0] != None and periods[1] != None and periods[2] != None:
            break

    a = lcm(periods[0], periods[1])
    a = lcm(a, periods[2])
    print(periods)
    print(a)

