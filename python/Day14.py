import math
class Recipe:
    def __init__(self, ingredients, output):
        # ingredients = (Identifier, amount)
        self.ingredients = ingredients
        self.output = output

    def __repr__(self):
        ingr = [(self.ingredients[a], a) for a in self.ingredients.keys()]
        output = ""
        for i in ingr:
            output += str(i[0]) + " " + i[1] + ", "
        output = output[:-2]
        output += " => " + str(self.output[1]) + " " + self.output[0]
        return output


def read_input():
    with open("Day14-input.txt") as f:
        lines = f.readlines()
        recipes = extract_recipes(lines)
    return recipes



def extract_recipes(lines):
    recipes = []
    for line in lines:
        a = line.strip()
        a = a.split(',')
        a = a[:-1] + a[-1].split("=>")
        for i in range(len(a)):
            if a[i][0] == " ":
                a[i] = a[i][1:]

            if a[i][-1] == " ":
                a[i] = a[i][:-1]
            a[i] = a[i].split(" ")
        ingr = [(b[1], int(b[0])) for b in a]

        output = ingr[-1]
        ingr = dict(ingr[:-1])
        recipes.append(Recipe(ingr, output))
    return recipes

ore_store = 1000000000000
ore_count = 0
fuel_created = 0

def produce(ingredient, amount, stores, recipes):
    global ore_count
    global ore_store
    global fuel_created

    # produces an ingredient and adds it to the stores
    # if the ingredient requires something not in the stores, it produces it
    if ingredient == "FUEL":
        fuel_created += amount

    if ingredient == "ORE":
        if ore_store >= amount:
            ore_store -= amount
        else:
            print("Fuel_created: {}".format(fuel_created))
            exit()

        ore_count += amount
        if "ORE" in stores.keys():
            stores["ORE"] += amount
        else:
            stores["ORE"] = amount
        return

    r = find_recipe(ingredient, recipes)
    amount_needed = math.ceil(amount / r.output[1])

    for ingr in r.ingredients:
        to_make = amount_needed * r.ingredients[ingr]
        if ingr in stores.keys() and stores[ingr] >= to_make:
            stores[ingr] -= to_make
        else:
            if ingr in stores.keys():
                produce(ingr, to_make-stores[ingr], stores, recipes)
            else:
                produce(ingr, to_make, stores, recipes)
            stores[ingr] -= to_make

    if ingredient in stores.keys():
        stores[ingredient] += r.output[1]*amount_needed
    else:
        stores[ingredient] = r.output[1]*amount_needed


def find_recipe(need, recipes):
    r = [r for r in recipes if r.output[0] == need]
    if r == []:
        print("Can't find {}".format(need))
        exit()
    return r[0]


def part1(recipes):
    global ore_count
    global fuel_created
    global ore_store
    # find the fuel recipe
    fuel_recipe = find_recipe("FUEL", recipes)
    available = []
    stores = {}
    produce("FUEL", 1184209, stores, recipes)
    print(fuel_created, ore_store)
    print(ore_count)


def test_1():
    test = ["157 ORE => 5 NZVS",
            "165 ORE => 6 DCFZ",
            "44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL",
            "12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ",
            "179 ORE => 7 PSHF",
            "177 ORE => 5 HKGWZ",
            "7 DCFZ, 7 PSHF => 2 XJWVT",
            "165 ORE => 2 GPVTF",
            "3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT"]

    return extract_recipes(test)

def test_2():
    test = ["2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG",
            "17 NVRVD, 3 JNWZP => 8 VPVL",
            "53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL",
            "22 VJHF, 37 MNCFX => 5 FWMGM",
            "139 ORE => 4 NVRVD",
            "144 ORE => 7 JNWZP",
            "5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC",
            "5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV",
            "145 ORE => 6 MNCFX",
            "1 NVRVD => 8 CXFTF",
            "1 VJHF, 6 MNCFX => 4 RFSQX",
            "176 ORE => 6 VJHF"]
    return extract_recipes(test)

def test_3():
    test = ["171 ORE => 8 CNZTR",
            "7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL",
            "114 ORE => 4 BHXH",
            "14 VRPVC => 6 BMBT",
            "6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL",
            "6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT",
            "15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW",
            "13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW",
            "5 BMBT => 4 WPTQ",
            "189 ORE => 9 KTJDG",
            "1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP",
            "12 VRPVC, 27 CNZTR => 2 XDBXC",
            "15 KTJDG, 12 BHXH => 5 XCVML",
            "3 BHXH, 2 VRPVC => 7 MZWV",
            "121 ORE => 7 VRPVC",
            "7 XCVML => 6 RJRHP",
            "5 BHXH, 4 VRPVC => 5 LTCX"]
    return extract_recipes(test)

if __name__ == "__main__":
    r = read_input()
    #r = test_3()
    part1(r)