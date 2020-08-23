import sys
import time
from random import randint
from ICP2 import Graph
sys.setrecursionlimit(1000000000)
#print(sys.getrecursionlimit())
#exit(0)
g = Graph()
g.load('../orkut.txt', ' ', '#')
tt = time.time()
g.icp_index()

k, r = [], []
for i in range(100):
    k.append(randint(1, 100))
    r.append(randint(1, 3))
for i in range(100):
    g.find_communities(k[i], r[i]-1)
print("ICP AT: ", time.time() - tt)
print(g.no_nodes())
print(g.no_nodes2())
