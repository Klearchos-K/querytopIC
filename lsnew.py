import sys
import threading
import time
from copy import copy, deepcopy
from queue import Queue
from random import randint
import unionfind

from node import Node
from vertex import Vertex




class Graph_l():
    G = []
    Gr = {}
    IT = {}
    t = {}
    mw = {}
    __max_core_num = 0
    time_copy = 0
    name = ""

    def __insert_edge(self, a, b):
        if a not in self.Gr:
            self.Gr[a] = Node(str(a), int(a))
        if b not in self.Gr:
            self.Gr[b] = Node(str(b), int(b))
        self.Gr[a].add_neighbour(self.Gr[b])
        self.Gr[b].add_neighbour(self.Gr[a])

    def load(self, file='graph.txt', split_symbol=' ', comment_symbol='#'):
        self.name = file.split(".")[0]
        start_time = time.time()
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
            self.__insert_edge(a, b)

        f.close()
        print("DONE reading file/inserting: ", (time.time() - start_time) / 60)
        #self.compute_cores(self.Gr)
        self.G = sorted(self.Gr.values(), key=lambda kv: kv.weight, reverse=True)


    def load_part(self, file='graph.txt', split_symbol=' ', comment_symbol='#', part=50):
        start_time = time.time()
        f = open(file, 'r', encoding='utf-8')
        accept = set()
        pernao = 0
        kobo = 0
        c = 0
        for line in f:
            if line[:len(comment_symbol)] == comment_symbol:
                print("akiri grammi")
                continue
            if c == 0:
                for i in range(part):
                    new = randint(0,99)
                    while new in accept:
                        new = randint(0, 99)
                    accept.add(new)
            if c not in accept:
                kobo += 1
                c = (c + 1) % 100
                continue
            l = line.replace('\n', '')
            l = l.split(split_symbol)
            a = str(l[0])
            b = str(l[1])
            # print(a, b)
            self.__insert_edge(a, b)
            pernao += 1
            accept.remove(c)
            c = (c + 1) % 100
            #print(c)

        f.close()
        print("DONE reading file/inserting: ", (time.time() - start_time) / 60)
        print('perasa', pernao, 'kobo', kobo)
        #self.compute_cores(self.Gr)
        self.G = sorted(self.Gr.values(), key=lambda kv: kv.weight, reverse=True)


    def reduce_core(self, g, r):
        q = Queue()
        for u in deepcopy(g).values():
            if u.degree < r:
                q.put(u)
                while not q.empty():
                    v = q.get()
                    try:
                        g[v.id]
                    except:
                        continue
                    for v2 in v.getN():
                        #try:
                        #    g[v2]
                        #except:
                        #    continue
                        if g[v2].degree <= r:
                            q.put(g[v2])
                    for i in g[v.id].getN():
                        g[i].delete_neighbour(v)
                    del g[v.id]


    def compute_cores(self, g):
        self.__max_core_num = 0
        md = 0
        vert = [u for u_name, u in sorted(g.items(), key=lambda kv: (kv[1].degree), reverse=False)]
        for i in range(len(vert)):
            # vert[i].degree = len(vert[i].neighbours)
            # print(vert[i], vert[i].degree, vert[i].c, vert[i].c2, vert[i].support)
            vert[i].pos = i
            if vert[i].degree > md:
                md = vert[i].degree

        b = [None] * (md + 1)  # one for zero degree
        for i in range(len(vert)):
            b[vert[i].degree] = i
        #res = ""
        #for i in vert:
        #    res += "" + str(i.id) + ":" + str(i.pos) + " "
        # print(res)
        # print(b)
        for i in range(len(vert)):
            # if vert[i].degree - vert[i].c == 1:
            # print(type(vert[i].vertex_p))
            # vert[i].vertex_p.append(None)
            # vert[i].l.append(0)
            # print("METABOLH KATA 1", 'NEO CORE TOU', vert[i], vert[i].degree, len(vert[i].l))
            # if vert[i].c - vert[i].degree == 1:
            # print("METABOLH KATA --1")
            # del vert[i].vertex_p[-1]
            # del vert[i].l[-1]
            # print("METABOLH KATA 1", 'NEO CORE TOU', vert[i], vert[i].degree, len(vert[i].l))

            vert[i].c = vert[i].degree
            if vert[i].c > self.__max_core_num:
                self.__max_core_num = vert[i].c
            # print("TO EKNAAAAAAAAAAAAA ", type(vert[i].c)) EDO H ALLAGHHHHHHHHHHHHHHHHHHHH cu
            # vert[i].degree=0
            self.__del_node(vert[i], vert, b, g)
            # if i ==2:
            #   break

        #res = ""
        #for i in vert:
        #    res += str(i.id) + ":" + str(i.pos) + " "
        # print(res)
        # print(b)
        print("TO MAX CORE ", self.__max_core_num)
        #print("TO MAX D ", md)
        # for i in self.g.keys():
        #   self.g[i].degree = len(self.g[i].neighbours)

    def __del_node(self, u, vert, b, g):
        k = u.degree
        u.degree = 0
        for v_name in u.getN():
            v = g[v_name]
            if v.degree == 0:
                continue
            if v.degree <= k:
                # print("prosperasa ton ", v.id)
                # self.del_node(v, vert, b)
                continue

            v.degree += -1
            # b[v.degree] += 1
            p = v.degree
            while b[p] == None:  # find pointer of previous bin
                p += -1
            b[v.degree] = b[p] + 1

            if b[v.degree] == b[v.degree + 1]:
                b[v.degree + 1] = None

            temp = vert[v.pos]
            temppos = vert[v.pos].pos
            temppos2 = vert[b[v.degree]].pos
            vert[v.pos] = vert[b[v.degree]]
            vert[v.pos].pos = temppos  # vert[b[v.degree]].pos

            temppos = vert[b[v.degree]].pos
            vert[b[v.degree]] = temp
            vert[b[v.degree]].pos = temppos2
            # print("antimetathesa  ")
            # v.degree += -1
            # if v.degree <= k:
            #   self.del_node(v, vert, b)

    def countic(self, g, r):
        pos = len(self.G) - 1
        keys = []
        cvs = []

        self.compute_cores(g)
        #for i in g.values():
        #   print(i.c, i.id)
        to_del = []
        for u in g.values():
            u.degree = len(u.neighbours1) + len(u.neighbours2)
            # print(u.id, u.c)
            if u.c < r:
                to_del.append(u.id)
        for i in to_del:
            for a in g[i].getN():
                g[a].delete_neighbour(g[i])
            del g[i]
        # print(to_del)

        #self.reduce_core(g, r)

        while len(g) > 0:
            while not self.G[pos].id in g:
                pos += -1
            u = g[self.G[pos].id]
            pos += -1
            keys.append(u)
            self.remove(u, cvs, g, r)

        #print("--------------------------")
        # for i in cvs:
        #    print(i.id)

        return keys, cvs

    def remove(self, u, cvs, g, r):
        # print("KEYNODE ", u.id)
        q = Queue()
        q.put(u)
        while not q.empty():
            v = q.get()
            for v2 in v.getN():
                try:
                    g[v2]
                except:
                    continue
                if g[v2].degree == r:
                    q.put(g[v2])
            cvs.append(v)
            for i in g[v.id].getN():
                g[i].delete_neighbour(v)
            del g[v.id]

    def size_graph(self, g):
        #return g['size']
        tt = time.time()
        sum = 0
        for i in g.values():
            sum += len(i.neighbours1) + 1  # one for node
        #print("TOSO GIA TO SIZE ", time.time() - tt)
        return sum

    def local_search_only(self, k, r):
        tt = time.time()
        if k + r - 1 >= len(self.G):
            t = self.G[-1].weight
        else:
            t = self.G[k + r - 1].weight
        g = {}
        size = 0
        no = 0
        maxw = 0
        i = 0
        while self.G[i].weight >= t and i != len(self.G) - 1:
            g[self.G[i].id] = self.G[i]
            g[self.G[i].id].degree += - len(g[self.G[i].id].neighbours1)
            g[self.G[i].id].neighbours1.clear()
            size += 1# len(g[self.G[i].id].neighbours2)
            maxw = g[self.G[i].id].weight
            for u in g[self.G[i].id].neighbours2:
                if u in g:
                    g[u].add_neighbour(g[self.G[i].id])
                    size += 1
            i += 1
        #keys, cvs = self.countic(deepcopy(g), r)
        keys, cvs = self.countic(self.gcopy(g), r)
        no = len(keys)
        while no < k and i != len(self.G):
            ps = size  # self.size_graph(g)
            #while self.size_graph(g) < 2 * ps and i < len(self.G):
            while size < 2 * ps and i < len(self.G):
                g[self.G[i].id] = self.G[i]
                g[self.G[i].id].degree += - len(g[self.G[i].id].neighbours1)
                g[self.G[i].id].neighbours1.clear()
                size += 1 #len(g[self.G[i].id].neighbours2)
                maxw = g[self.G[i].id].weight
                for u in g[self.G[i].id].neighbours2:
                    if u in g:
                        g[u].add_neighbour(g[self.G[i].id])
                        size += 1
                i += 1
            #keys, cvs = self.countic(deepcopy(g), r)
            keys, cvs = self.countic(self.gcopy(g), r)
            no = len(keys)
            #print(no, 'edqwwqwqwqwqwq', ps)
        #print(no, 'edqwwqwqwqwqwq', ps)
        # keys, cvs = self.countic(deepcopy(g), r)
        #print("COUNT TIME ", time.time() - tt)
        return self.enumic(keys[-k:], cvs)




    def local_search(self, k, r):
        extend = False
        if r in self.t:
            t = self.t[r]
            if t == 'full':
                t = self.G[-1].weight
            extend = True
            #print("PEIRA ETOIMO t", t)
        elif k + r - 1 >= len(self.G):
            t = self.G[-1].weight
        else:
            t = self.G[k + r - 1].weight
        g = {}
        size = 0
        no = 0
        maxw = 0
        i = 0
        while self.G[i].weight >= t and i != len(self.G) - 1:
            g[self.G[i].id] = self.G[i]
            g[self.G[i].id].degree += - len(g[self.G[i].id].neighbours1)
            g[self.G[i].id].neighbours1.clear()
            size += 1
            maxw = g[self.G[i].id].weight
            for u in g[self.G[i].id].neighbours2:
                if u in g:
                    g[u].add_neighbour(g[self.G[i].id])
                    size += 1
            i += 1
        if not extend:
            #keys, cvs = self.countic(deepcopy(g), r)
            keys, cvs = self.countic(self.gcopy(g), r)
            #print(g)
            no = len(keys)
        while no < k and i != len(self.G):
            #ps = self.size_graph(g)
            ps = size
            #while self.size_graph(g) < 2 * ps and i < len(self.G):
            while size < 2 * ps and i < len(self.G):
                g[self.G[i].id] = self.G[i]
                g[self.G[i].id].degree += - len(g[self.G[i].id].neighbours1)
                g[self.G[i].id].neighbours1.clear()
                size += 1
                maxw = g[self.G[i].id].weight
                for u in g[self.G[i].id].neighbours2:
                    if u in g:
                        g[u].add_neighbour(g[self.G[i].id])
                        size += 1
                i += 1
            #keys, cvs = self.countic(deepcopy(g), r)
            temp = self.gcopy(g)
            keys, cvs = self.countic(temp, r)
            del temp
            #print(g)
            no = len(keys)
            #print(no, 'edqwwqwqwqwqwq', ps)
        #print(no, 'edqwwqwqwqwqwq')
        #keys, cvs = self.countic(deepcopy(g), r)
        num = self.create_vertices(keys, cvs, r)
        #self.construct_tree2222222(cvs[:num], r, g)
        self.con_tree2222222(cvs[:num], r, g)
        if i == len(self.G):
            print("MEGISTO DYNATO")
            self.t[r] = 'full'
        else:
            self.t[r] = maxw
        #for x in self.IT[r]:
        #    print(x, len(x.childs))
        #print('edooooo', cvs[:num])


    def enumic(self, keys, cvs):
        tt = time.time()
        #print("ENUM IC")
        #print(keys)
        #print(cvs)
        v2key = unionfind.unionfind(len(cvs))
        sumtime = 0
        ch = {}
        gp = {}
        map = {}
        mapk = {}
        IC = {}
        for i in range(len(cvs)):
            map[cvs[i].id] = i
        #print(map)
        p = len(cvs) - 1
        #print(v2key.groups())
        for u in reversed(keys):
            #print(u)
            ch[u.id] = set()
            gp[u.id] = set()
            while u.id != cvs[p].id:
                gp[u.id].add(cvs[p])
                #print("prosthesa ", cvs[p].id)
                v2key.unite(map[u.id], map[cvs[p].id])
                p += -1
            gp[u.id].add(cvs[p])
            #print("prosthesa ", cvs[p].id)
            p += -1
            #print("DESOLE")
            for v in gp[u.id]:
                for w in v.getN():
                    #print(w, "aniki se ", u.id, v2key.issame(map[u.id], map[w]))
                    if not v2key.issame(map[u.id], map[w]):
                        v2key.unite(map[u.id], map[w])
                        temp = v2key.find(map[w])
                        ch[u.id].add(mapk[temp])
                        #ch[u.id].add(ch[w])
                        #print("ENOSA TA", u.id, w)
                #print(ch[u.id], '********///**********')
                mapk[v2key.find(map[u.id])] = u.id
                #print(v2key.parent)
                #print(ch)
               # print("new map", mapk)
            tttt = time.time()
            IC[u.id] = gp[u.id]
            for a in ch[u.id]:
                for x in IC[a]:
                    IC[u.id].add(x)
            sumtime += time.time() - tttt
        #print("TIME TO ADD ", sumtime)

        #print(v2key.groups())
        #print(IC)
        #print("ENUM TIME ", time.time() - tt)
        re = [y for x,y in sorted(IC.items(), key=lambda kv: int(kv[0]), reverse=True)]
        return re
        return IC.values()


    def create_vertices(self, keys, cvs, r):
        #print('ftiaxno kobmous')
        if r not in self.IT:
            self.IT[r] = []
        i = 0
        j = 0
        #print(keys)
        #print(cvs)
        limit = len(keys) - len(self.IT[r])
        toadd = []
        keys.append(None)
        while i < len(keys)-1 and len(toadd)<limit:
            k = keys[i]
            u = cvs[j]
            u = self.Gr[u.id]
            vert = Vertex()
            vert.addNode(u)
            u.vertex_p[r] = vert
            while cvs[j + 1] != keys[i + 1]:
                j += 1
                u = cvs[j]
                u = self.Gr[u.id]
                vert.addNode(u)
                u.vertex_p[r] = vert
                if j + 1 >= len(cvs):
                    break
            i += 1
            j += 1
            #print("EFTIAXA", vert)
            toadd.append(vert)
        toadd.reverse()
        for x in toadd:
            self.IT[r].append(x)
        #print(self.IT[r])
        #print("prosthesa sto dendro ", toadd)
        return j


    def construct_tree(self, cvs, r):
        #print('build tree')
        total = 0
        maxc = 0
        start_time = time.time()
        seen = []
        for i in range(self.__max_core_num):
            seen.append(set())
        for u2 in sorted(cvs, key=lambda kv: kv.weight, reverse=True):
            u = self.Gr[u2.id]
            for v in u2.neighbours2:
                Su = u.vertex_p[r].root
                c = 0
                while Su.parent:
                    c += 1
                    if Su == Su.root:
                        Su = Su.parent
                    else:
                        Su = Su.root
                u.vertex_p[r].root = Su
                v = self.Gr[v]
                Sv = v.vertex_p[r].root
                c = 0
                while Sv.parent:
                    if Sv == Sv.root:
                        Sv = Sv.parent
                    else:
                        Sv = Sv.root
                    c += 1
                if c > maxc:
                    maxc = c
                v.vertex_p[r].root = Sv

                if Su != Sv:
                    #if True:
                    if Su.minweight < Sv.minweight:
                        # print("kitso des me1")
                        Su.childs.append(Sv)
                        Sv.parent = Su
                        #if len(Sv.childs) == 0:
                        #    self.__leafs[i].add(Sv)
                        #if Su in self.__leafs[i]:
                        #    self.__leafs[i].remove(Su)
                    else:
                        # print("kitso des me2")
                        Sv.childs.append(Su)
                        Su.parent = Sv
                        #if len(Su.childs) == 0:
                        #    self.__leafs[i].add(Su)
                        #if Sv in self.__leafs[i]:
                        #    self.__leafs[i].remove(Sv)


    def construct_tree2222222(self, cvs, r, g):
        #print('build tree')
        #print(self.IT[r])
        cvs.reverse()
        #print(cvs)
        #for kapa in (self.IT[r][10].value):
        #    print(kapa.getN())
        #print(sorted(self.IT[r][8].value), 'ogwegjwoengoewngioAPO TAPENTARKA')
        total = 0
        maxc = 0
        start_time = time.time()
        seen = []
        for i in range(self.__max_core_num):
            seen.append(set())
        for vertex in self.IT[r]:
            tempw = 9999999999
            for u2 in vertex.value:
                if tempw>u2.weight:
                    tempw=u2.weight
            for u2 in sorted(vertex.value):
                u = self.Gr[u2.id]
                for v in sorted(g[u2.id].neighbours2, reverse=True):
                    #print(g[v].vertex_p[r], '////////////////////////////////////////')
                    for k in g[v].vertex_p[r].value:
                        if k.weight < tempw:
                            #print("PROSPERASA", v, k)
                            continue
                    Su = u.vertex_p[r].root
                    c = 0
                    while Su.parent:
                        c += 1
                        if Su == Su.root:
                            Su = Su.parent
                        else:
                            Su = Su.root
                    u.vertex_p[r].root = Su
                    v = self.Gr[v]
                    #if v.weight<tempw:
                    #    continue
                    try:
                        Sv = v.vertex_p[r].root
                    except:
                        #Sv = v.vertex_p[r] = v
                        #print("EXCEPTION")
                        continue
                    c = 0
                    while Sv.parent:
                        if Sv == Sv.root:
                            Sv = Sv.parent
                        else:
                            Sv = Sv.root
                        c += 1
                    if c > maxc:
                        maxc = c
                    v.vertex_p[r].root = Sv

                    if Su != Sv:
                        if Su.minweight < Sv.minweight:
                            Su.childs.append(Sv)
                            Sv.parent = Su

                        else:
                            Sv.childs.append(Su)
                            Su.parent = Sv

    def con_tree(self,cvs, r):
        #print(self.Gr['4018'].getN())
        maxc = 0
        for vert in self.IT[r]:
            vv = set()
            self.__sub_tree(vert, vv)
            #print("===========", vert,"=============")
            nn = set()
            for u in vv:
                for k in u.neighbours2:
                    nn.add(int(k))
            #print(vert, sorted(nn, reverse=True))
            for v in sorted(nn, key=lambda kv: self.Gr[str(kv)].vertex_p[r].minweight, reverse=True):
                v = self.Gr[str(v)]
                #print(v, v.vertex_p[r].minweight)
                if v.weight < vert.minweight:
                    continue
                Su = vert.root
                c = 0
                while Su.parent:
                    c += 1
                    if Su == Su.root:
                        Su = Su.parent
                    else:
                        Su = Su.root
                #u.vertex_p[r].root = Su
                vert.root = Su

                Sv = v.vertex_p[r].root
                c = 0
                while Sv.parent:
                    if Sv == Sv.root:
                        Sv = Sv.parent
                    else:
                        Sv = Sv.root
                    c += 1
                if c > maxc:
                    maxc = c
                v.vertex_p[r].root = Sv

                if Su != Sv:
                    if Su.minweight < Sv.minweight:
                        Su.childs.append(Sv)
                        Sv.parent = Su
                        #print("ebala paidi", Sv, 'sto ', Su, ' apo ', vert)
                        break
                    else:
                        Sv.childs.append(Su)
                        Su.parent = Sv
                        #print("ebala paidi", Su, 'sto ', Sv, ' apo ', vert)
                        break

    def con_tree2222222(self, cvs, r, g):
        cvs.reverse()
        #self.reduce_core(g, r)
        #print(cvs)
        if r not in self.mw:
            self.mw[r] = self.Gr[cvs[0].id].vertex_p[r].minweight
        #print(self.mw[r])
        for u in cvs:
            u = self.Gr[u.id]
            for v in self.Gr[u.id].getN():
                v = self.Gr[v]
                try:
                    v.vertex_p[r]
                except:
                    continue
                if v.vertex_p[r].minweight < self.mw[r]:
                    continue
                Su = u.vertex_p[r].root
                while Su.parent:
                    if Su == Su.root:
                        Su = Su.parent
                    else:
                        Su = Su.root
                u.vertex_p[r].root = Su

                Sv = v.vertex_p[r].root
                while Sv.parent:
                    if Sv == Sv.root:
                        Sv = Sv.parent
                    else:
                        Sv = Sv.root
                v.vertex_p[r].root = Sv

                if Su != Sv:
                    if True:
                        Su.childs.append(Sv)
                        Sv.parent = Su

            self.mw[r] = u.vertex_p[r].minweight


    def find_communities(self, k, t):
        #if t not in self.IT:
        #    raise Exception("There is not " + str(t) + " tree")
        res = []
        for l in (self.IT[t][:k]):
            u = set()
            self.__sub_tree(l, u)
            res.append(u)
        return res

    def __sub_tree(self, vertex, U):
        U.update(vertex.value)
        for v in vertex.childs:
            self.__sub_tree(v, U)


    def query(self, k, r):
        if r not in self.IT:
            print("no icp tree found!")
            self.local_search(k, r)
        elif k > len(self.IT[r]):
            if r not in self.t:
                print("Tree too small!")
                self.local_search(k, r)
            elif self.t[r] != "full":
                print("Tree is not maximal!")
                self.local_search(k, r)
            elif self.t[r] == "full":
                print("KOPSTONA E")
        else:
            print("Great :)")
        return self.find_communities(k, r)



    def expreriments(self, num=100, max_k=100, max_r=10):
        k, r = [], []
        for i in range(num):
            k.append(randint(1, max_k))
            r.append(randint(1, max_r))

        self.time_copy = 0
        tt = time.time()
        for i in range(num):
            self.query(k[i], r[i])
        t2 = time.time() - tt - self.time_copy

        fo = self.time_copy
        self.time_copy = 0
        tt = time.time()
        for i in range(num):
            #print(k[i], r[i], "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            self.local_search_only(k[i], r[i])
        t1 = time.time() - tt - self.time_copy


        f = open(self.name + "-RESULTS.txt", "a")
        f.write("No " + str(num) + " k " + str(max_k) + " r " + str(max_r) + '\n')
        f.write("ONLINE TIME: " + str(t1) + "    " + str(self.time_copy) + '\n')
        f.write("MY TIME (OUR TIME): " + str(t2) + "    " + str(fo) + '\n')
        f.write("Ratio: " + str(t1/t2) + '\n \n')
        f.close()


    def gcopy(self, g):
        tt = time.time()
        new = {}
        for u in g.items():
            temp = Node(u[1].id, u[1].weight)
            temp.neighbours1 = copy(u[1].neighbours1)
            temp.neighbours2 = copy(u[1].neighbours2)
            temp.degree = copy(u[1].degree)
            temp.vertex_p = copy(u[1].vertex_p)

            new[u[0]] = temp
        #print(time.time() -tt, "TOOK TO KOPY g ////////////////////////////////////////////////////////////////")
        self.time_copy += time.time() - tt
        return new



def tester(n):

    foo = Graph_l()
    foo.load('amazon.txt', '\t')
    g1 = foo.Gr
    foo.reduce_core(g1, n)
    #print(foo.Gr)
    s2 = set()
    for i in g1.keys():
        s2.add(i)

    foo2 = Graph_l()
    foo2.load('amazon.txt', '\t')
    r = n
    g = foo2.Gr
    foo2.compute_cores(g)
    # for i in g.values():
    #   print(i.c, i.id)
    to_del = []
    for u in g.values():
        u.degree = len(u.neighbours1) + len(u.neighbours2)
        # print(u.id, u.c)
        if u.c < r:
            to_del.append(u.id)
    for i in to_del:
        for a in g[i].getN():
            g[a].delete_neighbour(g[i])
        del g[i]
    #print(g)
    s1 = set()
    for i in g.keys():
        s1.add(i)

    #print((s2) == (s1))
    return s2==s1

#def fooo():
#    foo.expreriments(100)
#    return



#sys.setrecursionlimit(18000000)
#threading.stack_size(268000000)
#foo = Graph_l()
#foo.load_part('fb2.txt', ' ', part=50)
#foo.load('fb2.txt', ' ')



def check_correctness(a, b):
    correct = True
    for j in range(len(a)):
        s1 = set()
        s2 = set()
        for i in a[j]:
            s1.add(i.id)
        for i in b[j]:
            s2.add(i.id)
        if not s1 == s2:
            #print("EISAI LATHOS", j)
            correct = False
            break
    return correct



#thread = threading.Thread(target=fooo())
#thread.start()

