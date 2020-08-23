class Vertex():
    def __init__(self, timestamp):
        self.minweight = 1000000
        self.minrank = self.minweight
        self.parent = None
        self.childs = []
        self.value = None
        self.timestamp = timestamp
        self.smallest_node = None
        self.root = self

    def addNode(self, u):
        if not self.value:
            self.value = set()
        self.value.add(u)
        if u.weight < self.minweight:
            self.minweight = u.weight
            self.smallest_node = u
            self.minrank = u.weight

    def __lt__(self, other):
        return self.minweight < other.minweight

    def __repr__(self):
        res = "{"
        for i in self.value:
            res += i.id + " "
        return res + "}"

    def __str__(self):
        res = "{"
        for i in self.value:
            res += i.id + " "
        return res + "}"