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
foo.load(filename, "	", "#")
#foo.compute_cores(foo.Gr)

foo.expreriments(int(q), int(k), int(r))
exit(0)

def thr():
    print('me kalesan')
    foo = Graph_l()
    foo.load("youtube2.txt", " ", "#")
    foo.expreriments(100, 100, r)



for i in range(10):
    #thread = threading.Thread(target=thr())
    #thread.start()
    thr()

