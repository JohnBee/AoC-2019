import copy

def read_input_file():
    out = []
    with open("Day6-input.txt") as f:
        lines = f.readlines()
        print(lines)
        for line in lines:
            tokens = line.strip().split(")")
            key = tokens[0]
            value = tokens[1]
            out.append((key, value))

    return out


def list_to_tree(list):
    out = {}
    for k,v in list:
        if k in out.keys():
            out[k] += [v]
        else:
            out[k] = [v]
    return out

def use_file():
    o = read_input_file()
    return list_to_tree(o)


def load_test():
    lines = ["COM)B",
            "B)C",
            "C)D",
            "D)E",
            "E)F",
            "B)G",
            "G)H",
            "D)I",
            "E)J",
            "J)K",
            "K)L"]
    out = {}
    for line in lines:
        tokens = line.strip().split(")")
        key = tokens[0]
        value = tokens[1]
        if key in out.keys():
            out[key] += [value]
        else:
            out[key] = [value]

    return out

def load_test2():
    lines = [
        "COM)B",
        "B)C",
        "C)D",
        "D)E",
        "E)F",
        "B)G",
        "G)H",
        "D)I",
        "E)J",
        "J)K",
        "K)L",
        "K)YOU",
        "I)SAN"
    ]
    out = []
    for line in lines:
        tokens = line.strip().split(")")
        key = tokens[0]
        value = tokens[1]
        out.append((key,value))
    return out


def bfs(o, toVisit, visited, depth):
    if toVisit == []:
        return visited
    vis = copy.deepcopy(toVisit)

    d = depth + 1
    for v in toVisit:
        vis.remove(v)
        if v in o.keys():
            vis += o[v]
        visited += [(v, depth)]
    return bfs(o, vis, visited, d)


# def calc_jumps(orb_list, start, end):
#     for k, v in orb_list:
#         if k == start:
#             a = v
#         if k == end:
#             b = v
#     return a-b+2

def rebuild_tree(o, start):
    # find all that reference
    def neighbours(o, root):
        j = [(c[0], c[1]) for c in o if root==c[0] or root in c[1]]
        i = []
        for k,v in j:
            if k == root:
                i.append(v)
            else:
                i.append(k)
        return i

    new_tree = []

    def build(o, node, tree, visited, queue):
        visited.append(node)
        queue.append(node)

        while queue:
            v = queue.pop(0)
            for neigh in neighbours(o, v):
                if neigh not in visited:
                    tree.append((v, neigh))
                    visited.append(neigh)
                    queue.append(neigh)

        return tree
    print(build(o, start, new_tree, [], []))

    return new_tree


def search_map(o):
    start = "COM"
    e = bfs(o, [start], [], 0)
    print(sum([a[1] for a in e]))




if __name__ == "__main__":
    o = read_input_file()
    g = list_to_tree(o)
    # part 1 answer
    print("Part 1:")
    search_map(g)
    #o = load_test2()
    print(o)
    e = rebuild_tree(o, "YOU")
    f = list_to_tree(e)
    d = bfs(f,["YOU"],[],0)

    # part 2 answer
    print("Part 2")
    print(dict(d)["SAN"]-2)
