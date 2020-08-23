class Node:
    def __init__(self, id, w):
        self.id = id
        self.neighbours1 = set()
        self.neighbours2 = set()
        self.degree = len(self.neighbours1) + len(self.neighbours2)
        self.weight = w
        #self.cd = 0
        self.pos = 0
        self.c = 0
        self.vertex_p = {}

    def add_neighbour(self, u):
        if u.id in self.neighbours1 or u.id in self.neighbours2:
            return
        if u.weight < self.weight:
            self.neighbours1.add(u.id)
        else:
            self.neighbours2.add(u.id)
        self.degree += 1

    def delete_neighbour(self, x):
        if x.id in self.neighbours1:
            self.neighbours1.remove(x.id)
        elif x.id  in self.neighbours2:
            self.neighbours2.remove(x.id)
        else: return
        self.degree += -1

    def getN(self):
        return self.neighbours1.union(self.neighbours2)

    def __repr__(self):
        return "_" + self.id

    def __lt__(self, other):
        return self.weight > other.weight

