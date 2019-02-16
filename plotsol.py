import matplotlib.pyplot as plt
from math import sqrt

def read_sol(filename):

    def decode_point(str_of_point):
        p = str_of_point.split(',')
        return int(p[0]), int(p[1])


    def decode_line(line):
        point, succs = line.split(':')
        return decode_point(point), list(map(decode_point, succs.split(';')))


    fd = open(filename, 'r')
    sol = {}
    for line in fd.readlines():
        point, succs = decode_line(line)
        sol[point] = succs
    return sol

sol = read_sol('sol.txt')
vxs, vys = zip(*sol.keys())

f = plt.figure()
ax = f.add_subplot(111)
ax.scatter(vxs, vys)

class Tree:

    def __init__(self, point):
        self.node = point
        self.children = []

    def add_children(self, point):
        stree = Tree(point)
        self.children.append(stree)
        return stree

    def print_childre(self):
        print(list(map(lambda t: t.node, self.children)))
    
    def is_leaf(self):
        return len(self.children) == 0


mark = set()
def build(tree):
    mark.add(tree.node)
    for succ in sol[tree.node]:
        if succ in mark:
            continue
        stree = tree.add_children(succ)
        build(stree)


vs = list(sol.keys())
root = Tree(vs[0])
build(root)

def euc(p1, p2):
    return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def score(tree):
    cost = 0
    for succ in tree.children:
        cost += euc(tree.node, succ.node) + score(succ)
    return cost


ax.text(min(vxs), max(vys), str(score(root)), color='green', fontsize=14)

def breadth(tree):
    for succ in tree.children:
        ax.plot(*zip(*(tree.node, succ.node)))
        breadth(succ)
        

breadth(root)
plt.show()
