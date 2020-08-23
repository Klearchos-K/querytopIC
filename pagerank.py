import time

import networkx as nx
g = nx.Graph()
map = {}


def load(file='graph.txt', split_symbol=' ', comment_symbol='#'):
    start_time = time.time()
    # file = open('graph.txt', 'r')
    # file = open('amazon.txt', 'r')
    # file = open('DBLP.txt', 'r')
    f = open(file, 'r', encoding='utf-8')
    for line in f:
        if line[:len(comment_symbol)] == comment_symbol:
            print("akiri grammi")
            continue
        l = line.replace('\n', '')
        l = l.split(split_symbol)
        a = str(l[0])
        b = str(l[1])
        # print(a, b)
        g.add_edge(a, b)
        g.add_edge(b, a)

    f.close()
    print("DONE reading file/inserting: ", (time.time() - start_time) / 60)


print("endixi")
load('temp/com-friendster.ungraph.txt', '\t')
print("fiel done")
pr = nx.pagerank(g, alpha=0.9)
print("load done")
i = 1
x = sorted(pr.items(), key=lambda item: item[1], reverse=False)
for a in x:
   # print(a)
    map[a[0]] = i
    i += 1
print('DONE with pagerank')
f = open("friendster.txt", "w")
#print(map)
for u, v in g.edges:
    #print(u,v, "=>", map[u], map[v])
    f.write(str(map[u]) + " " + str(map[v]) + "\n")
f.close()

