import threading
import sys
from lsfinal import Graph_l
sys.setrecursionlimit(100000000)
filename = sys.argv[1]
print(filename)
q = sys.argv[2]
print(q)
k = sys.argv[3]
print(k)
r = sys.argv[4]
print("r= ", r)
foo = Graph_l()
#foo.load(filename, "	", "#")
foo.load(filename, " ", "#")
foo.expreriments(int(q), int(k), int(r))


