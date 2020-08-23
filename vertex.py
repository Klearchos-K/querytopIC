class Vertex():
    def __init__(self):
        self.minweight = 99000000
        self.parent = None
        self.childs = []
        self.value = None
        self.smallest_node = None
        self.root = self

    def addNode(self, u):
        if not self.value:
            self.value = set()
        self.value.add(u)
        if u.weight < self.minweight:
            self.minweight = u.weight
            self.smallest_node = u

    def __lt__(self, other):
        return self.minweight < other.minweight

    def __repr__(self):
        if not self.value:
            return "{empty}"
        res = "{"
        for i in self.value:
            res += str(i.id) + " "
        return res + "}"

    def __str__(self):
        res = "{"
        for i in self.value:
            res += str(i.id) + " "
        return res + "}"
