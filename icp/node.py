class Node:
    def __init__(self, id, w, neighbours):
        self.id = id
        self.neighbours = neighbours
        self.c = 0
        self.c2 = 0
        self.support = 0
        self.degree = len(neighbours)
        self.weight = w
        self.vertex_p = []
        self.pos = None
        self.rank = self.weight
        self.l = []  # number of neighbours with no smaller timestamp for each k tree
        self.cd = 0

    def add_neighbour(self, u):
        if u in self.neighbours:
            return
        self.neighbours.append(u)
        self.degree += 1

    def delete_neighbour(self, x):
        self.neighbours.remove(x)
        self.degree += -1

    def print_p(self):
        for i in self.vertex_p:
            res = []
            for k in i.value:
                res.append(k.id)
            print(res)
            #break

    def __repr__(self):
        return self.id

    def __lt__(self, other):
        return self.weight < other.weight