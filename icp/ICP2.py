import copy
import sys
import threading
import time

import unionfind as unionfind

from node import Node
from vertex import Vertex
import networkx as nx
from networkx.algorithms.core import k_core, core_number
#import matplotlib.pyplot as plt

class Graph():
    def __init__(self, g={}, r_max=548458):
        self.uf = []
        self.__g = g
        self.__IT = []
        self.__r_max = []
        self.__leafs = []
        self.__top_com = []
        self.__rm = r_max
        self.__max_core_num = 0
        self.name = ""

    def __insert_edge(self, a, b):
        if a not in self.__g:
            self.__g[a] = Node(str(a), int(a), [])
        if b not in self.__g:
            self.__g[b] = Node(str(b), int(b), [])
        self.__g[a].add_neighbour(str(b))
        self.__g[b].add_neighbour(str(a))

    def __compute_cores(self):
        self.__max_core_num = 0
        md = 0
        vert = [u for u_name, u in sorted(self.__g.items(), key=lambda kv: len(kv[1].neighbours), reverse=False)]
        for i in range(len(vert)):
            vert[i].degree = len(vert[i].neighbours)
            #print(vert[i], vert[i].degree, vert[i].c, vert[i].c2, vert[i].support)
            vert[i].pos = i
            if vert[i].degree > md:
                md = vert[i].degree

        b = [None] * (md + 1)  # one for zero degree
        for i in range(len(vert)):
            b[vert[i].degree] = i
        res = ""
        for i in vert:
            res += "" + str(i.id) + ":" + str(i.pos) + " "
        #print(res)
        #print(b)
        for i in range(len(vert)):
            if vert[i].degree - vert[i].c == 1:
                #print(type(vert[i].vertex_p))
                vert[i].vertex_p.append(None)
                vert[i].l.append(0)
                #print("METABOLH KATA 1", 'NEO CORE TOU', vert[i], vert[i].degree, len(vert[i].l))
            if vert[i].c - vert[i].degree == 1:
                #print("METABOLH KATA --1")
                del vert[i].vertex_p[-1]
                del vert[i].l[-1]
                #print("METABOLH KATA 1", 'NEO CORE TOU', vert[i], vert[i].degree, len(vert[i].l))


            vert[i].c = vert[i].degree
            if vert[i].c > self.__max_core_num:
                self.__max_core_num = vert[i].c
            #print("TO EKNAAAAAAAAAAAAA ", type(vert[i].c)) EDO H ALLAGHHHHHHHHHHHHHHHHHHHH cu
            # vert[i].degree=0
            self.__del_node(vert[i], vert, b)
            # if i ==2:
            #   break

        res = ""
        for i in vert:
            res += str(i.id) + ":" + str(i.pos) + " "
       # print(res)
        #print(b)
        #print("TO MAX CORE ", self.__max_core_num)
        #print("TO MAX D ", md)
        #for i in self.g.keys():
         #   self.g[i].degree = len(self.g[i].neighbours)

    def __del_node(self, u, vert, b):
        k = u.degree
        u.degree = 0
        for v_name in u.neighbours:
            v = self.__g[v_name]
            if v.degree == 0:
                continue
            if v.degree <= k:
                #print("prosperasa ton ", v.id)
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
            #print("antimetathesa  ")
            # v.degree += -1
            # if v.degree <= k:
            #   self.del_node(v, vert, b)

    def find_cores(self):
        mind = 1000000000000
        maxd = 0
        minnode = ""
        for i in self.__g.keys():
            if self.__g[i].degree < mind:
                mind = self.__g[i].degree
                minnode = i
            if self.__g[i].degree > maxd:
                maxd = self.__g[i].degree
        #print(minnode, mind)
        for i in self.__g.keys():
            if self.__g[i].degree == mind:
                self.__delete_dfs(i, mind)
        while mind <= maxd:
            if mind < maxd:
                pass
                #print("step ", mind)
            mind += 1
            com = False
            for i in self.__g.keys():
                if self.__g[i].degree == mind:
                    self.__delete_dfs(i, mind)
                    con = True

    def __delete_dfs(self, u, k):
        # print("molis esbisa ton ", u)
        self.__g[u].degree = 0
        self.__g[u].c = k
        for v in self.__g[u].neighbours:
            if self.__g[v].degree == 0:
                continue
            # g[v].delete_neighbour(u)
            self.__g[v].degree += -1
            if self.__g[v].degree < k:
                self.__delete_dfs(v, k)

    def __construct_tree(self):
        map = []
        mapr = []
        for i in self.__IT:
            self.uf.append(unionfind.unionfind(len(i)))
            map.append({})
            mapr.append({})
        #print(self.uf)
        for i in range(len(self.__IT)):
            for j in range(len(self.__IT[i])):
                #print(j.minweight)
                map[i][self.__IT[i][j].minweight] = j
        #print(map)

        total = 0
        maxc = 0
        start_time = time.time()
        seen = []
        for i in range(self.__max_core_num):
            seen.append(set())
        for u_name, u in sorted(self.__g.items(), key=lambda kv: kv[1].weight, reverse=True):
            if int(u.id) % 1000 == 0:
                #print("Step ", u.id, u.degree, u.c)
                #print(total)
                total = 0
            for i in range(u.c):
                Su = u.vertex_p[i]
                if Su not in seen[i]:
                    self.__top_com[i].append(Su)
                    seen[i].add(Su)
            for v_name in u.neighbours:
                if self.__g[v_name].weight <= u.weight:
                    continue
                v = self.__g[v_name]
                for i in range(min(self.__g[v_name].c, u.c)):
                    #startt = time.time()
                    Su = u.vertex_p[i]
                    Su2 = map[i][Su.minweight]
                    #u.vertex_p[i].root = Su
                    Sv = v.vertex_p[i]
                    Sv2 = map[i][Sv.minweight]
                    #v.vertex_p[i].root = Sv
                    #total+= time.time() - startt
                    #print("==", i)
                    #print(Su, u)
                    #print(Sv, v)
                    #print(self.uf[i].issame(Su2, Sv2))
                    if not self.uf[i].issame(Su2, Sv2):
                        try:
                            f = self.uf[i].find(Su2)
                            Su = mapr[i][f]
                        except:
                            pass
                        try:
                            f = self.uf[i].find(Sv2)
                            Sv = mapr[i][f]
                        except:
                            pass
                        self.uf[i].unite(Su2, Sv2)
                        if Su.minweight < Sv.minweight:
                            #print("kitso des me1")
                            Su.childs.append(Sv)
                            Sv.parent = Su
                            f = self.uf[i].find(Sv2)
                            mapr[i][f] = Su
                            #print("ebala paidi", Sv, 'sto ', Su)
                            if len(Sv.childs) == 0:
                                self.__leafs[i].add(Sv)
                            if Su in self.__leafs[i]:
                                self.__leafs[i].remove(Su)
                        else:
                            #print("kitso des me2")
                            Sv.childs.append(Su)
                            Su.parent = Sv
                            f = self.uf[i].find(Su2)
                            mapr[i][f] = Sv
                            #print("ebala paidi", Su, 'sto ', Sv)
                            if len(Su.childs) == 0:
                                self.__leafs[i].add(Su)
                            if Sv in self.__leafs[i]:
                                self.__leafs[i].remove(Sv)
        for i in range(len(self.__leafs)):
            self.__leafs[i] = sorted(self.__leafs[i], reverse=True)
        print("DONE constructing tree for icp index: ", (time.time() - start_time))
        print("MAX bottom up path ", maxc)
        #exit()

    def __update_core(self, u_name, u, k, S, U):
        #print("paidia me kalesane ", u_name)
        if u.c2 != -1:
            S[u.c2].addNode(u)
            # u.vertex_p.append(S[u.c2]) #==============================================================
            u.vertex_p[u.c2] = S[u.c2]
        U.add(u_name)
        for v in u.neighbours:
            if self.__g[v].c2 == -1 or self.__g[v].c < u.c2 or v in U:
                continue
            if (u.c2 == -1 and self.__g[v].c2 <= k) or (u.c2 != -1 and self.__g[v].c2 == u.c2 + 1):
                self.__g[v].support += -1
                if self.__g[v].support < self.__g[v].c2:
                    self.__g[v].c2 += -1
                    self.__update_core(v, self.__g[v], k, S, U)

    def __update_support(self, U):
        for u_name in U:
            u = self.__g[u_name]
            u.support = 0
            if u.c2 == -1:
                continue
            for v_name in u.neighbours:
                if self.__g[v_name].c < u.c2:
                    continue
                if self.__g[v_name].c2 >= u.c2:
                    u.support += 1

    def icp_index(self):
        start_time = time.time()
        self.__compute_cores()
        print("TO MEGISTO CORE", self.__max_core_num)
        for u_name, u in self.__g.items():
            u.degree = len(u.neighbours)
            u.vertex_p = [None] * u.c  # ===========================================================
            u.l = [0] * u.c
            u.c2 = u.c
            for v in u.neighbours:
                if self.__g[v].c >= u.c:
                    u.support += 1
        for i in range(self.__max_core_num):
            self.__IT.append([])
            self.__leafs.append(set())
            self.__top_com.append([])
            self.__r_max.append(0)  # infinity
        for u_name, u in sorted(self.__g.items(), key=lambda kv: kv[1].weight):
            # print("EINAI H SEIRA SOU: ", u_name)
            S = []
            for i in range(u.c2):
                new_vert = Vertex(timestamp=0+len(self.__IT[i]))
                S.append(new_vert)
                S[i].addNode(u)
                # u.vertex_p.append(S[i]) #==============================================================
                u.vertex_p[i] = S[i]
            k = u.c2
            u.c2 = -1
            U = set()
            self.__update_core(u_name, u, k, S, U)
            self.__update_support(U)
            for i in range(k):
                self.__IT[i].append(S[i])
        #print("====AFTOOOOOOOO========")
        i = 0
        for tree in self.__IT:
            if len(tree) - self.__rm >= 0:
                self.__r_max[i] = tree[len(tree) - self.__rm] #######################################################
                self.__r_max[i] = self.__r_max[i].minrank
            i += 1
        print("DONE with icp nodes: ", (time.time() - start_time))
        self.__construct_tree()
        f = open("INDEX-" + self.name.split("/")[1], "a")
        print("DONE with icp indexing total ", (time.time() - start_time))
        f.write("DONE with icp indexing total " + str(time.time() - start_time) + '\n \n')
        f.close()


    def __sub_tree(self, vertex, U):
        U.update(vertex.value)
        for v in vertex.childs:
            self.__sub_tree(v, U)

    def print_tree(self, root):
        for x in root.value:
            print(x.id)
        print("====")

        #print(self.find_communities(15, 2))
        # for c in root.childs:
        #   self.print_tree(c)
        print("====================================")

        # print("===")
        #print(self.IT[1])

    def find_non_contained_communities(self, k, t):
        if t >= len(self.__IT):
            raise Exception("There is not " + str(t) + " tree")
        return self.__leafs[t][:k]

    def find_communities2(self, k, t):
        if t >= len(self.__IT):
            raise Exception("There is not " + str(t) + " tree")
        result = []
        limit = len(self.__leafs[t])
        for i in range(limit - 1):
            # result.append(self.leafs[t][i])
            temp = self.__leafs[t][i]
            while temp > self.__leafs[t][i + 1] and len(result) < k:
                result.append(temp)
                temp = temp.parent
                if temp is None:
                    break
        if len(result) == k:
            return result
        # last leaf
        result.append(self.__leafs[t][-1])
        temp = self.__leafs[t][-1].parent
        while len(result) < k and temp:
            result.append(temp)
            temp = temp.parent

        return result


    def find_communities(self, k, t):
        if t >= len(self.__IT):
            raise Exception("There is not " + str(t) + " tree")
        res = []
        for l in (self.__top_com[t][:k]):
            u = set()
            self.__sub_tree(l, u)
            res.append(u)
        return res

    def __single_icp(self, k):
        self.__IT[k].clear()
        kcore = {}
        for u in self.__g.values():
            u.degree = len(u.neighbours)
            if u.c > k:
                temp = copy.copy(u)
                for v in temp.neighbours.copy():
                    if self.__g[v].c <= k:
                        temp.neighbours.remove(v)
                        temp.degree += -1
                kcore[temp.id] = temp
        print(len(kcore))

        for u_name, u in sorted(kcore.items(), key=lambda kv: kv[1].weight):
            new_vert = Vertex(timestamp=0 + len(self.__IT[k]))
            S = new_vert
            if u.degree == -1:
                continue
            self.__del_dfs(u, S, kcore, k)
            self.__IT[k].append(S)
            #self.g[u_name].vertex_p[k] = S  #  Original node not the copy one
            #print("o ", u_name, ' exei keno!')
            #print('Ebala to ', S, k)
            #break
        #print(len(kcore))
        #print(self.__IT[k])
       # if k == 2:
       #     print("EDO EISAI2", k)
       #     print(kcore)
        #for u in kcore.keys():
         #   print(self.g[u].vertex_p[k].parent)
        self.__recompute_tree_vertices(k, kcore)

    def __del_dfs(self, u, S, kcore, k):
        #print("hrthe o ", u, 'me d ', u.degree, type(u.neighbours[0]))
        u.degree = -1
        S.addNode(self.__g[u.id])  # add the original node not the copy
        self.__g[u.id].vertex_p[k] = S
        #print("prosthesa ton ", u)
        for v_name in u.neighbours:
            v = kcore[v_name]
            if v.degree == -1 or v_name in S.value:
                continue
            v.degree += -1
            if v.degree <= k:
                #print("stelno me d", v.degree, v)
                self.__del_dfs(v, S, kcore, k)


    def __recompute_tree_vertices(self, k, kcore):
        print("me kalesane na anaftakso ", k)
        self.__leafs[k].clear()
        self.__leafs[k] = set()
        self.__top_com[k].clear()
        seen = set()
        for u_name, foo in sorted(kcore.items(), key=lambda kv: kv[1].weight, reverse=True):
            #print("IRTHSAAA ", u_name)
            u = self.__g[u_name]
            Su = u.vertex_p[k]
            if Su not in seen:
                self.__top_com[k].append(Su)
                seen.add(Su)
            for v_name in u.neighbours:
                if self.__g[v_name].weight <= u.weight or v_name not in kcore:
                    continue
                v = self.__g[v_name]
                i = k
                Su = u.vertex_p[i]
                while Su.parent:
                    Su = Su.parent
                Sv = v.vertex_p[i]
                while Sv.parent:
                    Sv = Sv.parent
                if Su != Sv:
                    if Su.minweight < Sv.minweight:
                        Su.childs.append(Sv)
                        Sv.parent = Su
                        if len(Sv.childs) == 0:
                            self.__leafs[i].add(Sv)
                        if Su in self.__leafs[i]:
                            self.__leafs[i].remove(Su)
                    else:
                        Sv.childs.append(Su)
                        Su.parent = Sv
                        if len(Su.childs) == 0:
                            self.__leafs[i].add(Su)
                        if Sv in self.__leafs[i]:
                            self.__leafs[i].remove(Sv)

        self.__leafs[k] = sorted(self.__leafs[k], reverse=True)


    def __make_tree(self):
        self.__IT.append([])
        self.__r_max.append(0)
        self.__leafs.append([])
        self.__top_com.append([])
        self.__single_icp(len(self.__IT) - 1)
        #print(self.__IT[-1], 'xrima sto xrima')

    def edge_insertion(self, u_name, v_name):
        u = self.__g[u_name]
        v = self.__g[v_name]
        old_u = u.c
        old_v = v.c
        old_md = self.__max_core_num
        if v_name in u.neighbours and u_name in v.neighbours:
            print("Edge already exists!")
            return
        #self.insert_edge(u_name, v_name)

        print("Prin leo ", u.c, v.c)
        #self.compute_cores()
        self.__insert_fast(u_name, v_name)
        print("Tora leo ", u.c, v.c)
        if self.__max_core_num > old_md:
            print("THELOUME NEO DENDRO")
            self.__make_tree()

        cmin = min(u.c, v.c)
        print("to c min", cmin)
        for i in range(cmin):
            if u.rank < self.__r_max[i] or v.rank < self.__r_max[i]:
                continue
            if self.__is_recompute(u, v, i):
                print("PLz recompute all tree vertices of tree ", i)
                self.__single_icp(i)
        if old_u != u.c or old_v != v.c:
            print("cores updated!", cmin)
            if cmin < len(self.__r_max):
                if u.rank >= self.__r_max[cmin] and v.rank >= self.__r_max[cmin]:  #  ?????????????????????????????
                    print("PLLLLZZZZZzzz recompute all tree vertices of tree ", cmin)
                    self.__single_icp(i)

    def __is_recompute(self, u, v, k):
        if not u.vertex_p[k] and not v.vertex_p[k]:
            print("eeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
            return True
        elif not u.vertex_p[k]:
            R_min = v.vertex_p[k].timestamp
            w2 = v
            print("PERITPOSI XEXE 1")
        elif not v.vertex_p[k]:
            R_min = u.vertex_p[k].timestamp
            w2 = u
            print("PERITPOSI XEXE 2")
        else:
            R_min = min(u.vertex_p[k].timestamp, v.vertex_p[k].timestamp)
            if u.vertex_p[k].timestamp < v.vertex_p[k].timestamp:
                w2 = u
            else:
                w2 = v
        print(R_min, k, w2)
        for w in self.__IT[k][R_min].value:
            for x in w.neighbours:
                #w.l[k] = 0
                if self.__g[x].c <= k:
                   # print("alfffkos", x)
                    continue
                if not self.__g[x].vertex_p[k] or len(self.__g[x].vertex_p) >= k:  ######################################
                    #print("alfffkos_2", x)
                    continue
                if self.__g[x].vertex_p[k].timestamp >= w.vertex_p[k].timestamp:
                    w.l[k] += 1
            #print(w, w.l[k], k)
        u2 = self.__IT[k][R_min].smallest_node
        print('proto kalesma', u2, u2.c, u2.l, k)
        self.__insertion_dfs(u2, k, self.__IT[k][R_min])
        print(w2, w2.c, k, len(w2.l))
        return w2.l[k] != -1


    def __insertion_dfs(self, u, k, u2):
        u.l[k] = -1
        for v_name in u.neighbours:
            v = self.__g[v_name]
            if v not in u2.value or len(v.l) <= k: # v.l[k] == -1: ##############################################
                continue
            elif v.l[k] == -1:
                continue
            v.l[k] += -1
            if v.l[k] < k:
                self.__insertion_dfs(v, k, u2)

    def edge_deletion(self, u_name, v_name):
        u = self.__g[u_name]
        v = self.__g[v_name]
        if v_name not in u.neighbours or u_name not in v.neighbours:
            return
        old_u = u.c
        old_v = v.c
        old_md = self.__max_core_num
        # u.neighbours.remove(v_name)
        # u.degree += -1
        # v.neighbours.remove(u_name)
        # v.degree += -1
        # self.compute_cores()

        self.__delete_fast(u_name, v_name)
        cmin = min(u.c, v.c)
        for i in range(cmin):
            if u.rank < self.__r_max[i] or v.rank < self.__r_max[i]:
                continue

            u.l[i] = 0
            for x in u.neighbours:
                print(x, len(self.__g[x].vertex_p), i)
                if self.__g[x].c <= i:
                    continue
                elif not u.vertex_p[i] or not self.__g[x].vertex_p[i]:
                    continue
                print(self.__g[x].vertex_p[i], u.vertex_p[i])
                if self.__g[x].vertex_p[i].timestamp >= u.vertex_p[i].timestamp:
                    u.l[i] += 1

            v.l[i] = 0
            for x in v.neighbours:
                print(x, len(self.__g[x].vertex_p), i)
                if self.__g[x].c <= i:
                    continue
                elif not v.vertex_p[i] or not self.__g[x].vertex_p[i]:
                    continue
                print(self.__g[x].vertex_p[i], v.vertex_p[i])
                if self.__g[x].vertex_p[i].timestamp >= v.vertex_p[i].timestamp:
                    v.l[i] += 1
            print(u.l[i], v.l[i], ' EEEEELLLL')
            if u.l[i] <= i or v.l[i] <= i:
                print("Plz recompute tree ", i, 'apo ', u, v)
                self.__single_icp(i)
        if old_u != u.c or old_v != v.c:
            if u.rank >= self.__r_max[cmin] and v.rank >= self.__r_max[cmin]:
                print("Plz recompute tree ", cmin, 'apo CMIN', u, v)
            self.__single_icp(cmin)
        if self.__max_core_num < old_md:
            self.__IT[len(self.__IT) - 1].clear()
            del self.__IT[len(self.__IT) - 1]
            print(self.__max_core_num - old_md, 'mpouldozaaaaaaaaaaaaa')



    def print(self):
        #for i in self.g.keys():
            #print(i, g[i].c, g[i].c2, g[i].support)
            #g[i].print_p()
            #print("====")

        root = None

        xx = self.find_communities(6, 2)
        print(xx, '*************************--')
       # for u in self.IT[2]:
        #    print(u, u.timestamp)

        for i in self.__r_max:
            print(i)
        print(self.__r_max, ' kejf')
        #self.is_recompute(self.g['v14'], self.g['v1'], 1)
        self.edge_insertion('v6', 'v1')  # 2 6



        tw = "NONE"
        for i in self.__IT[1]:
            if self.__g['v12'] in i.value:
                tw = i
            if not i.parent:
                root = i
                # break
        #for x in root.value:
            #print(x.id)

        self.print_tree(root.childs[2].childs[0])
        print(tw.parent.value)
        xx = self.find_communities(6, 2)
        print(xx, '!!!!!!!!!!!!!!!!!!!!!')
        #print(self.IT[2])
        w = self.__g['v8']
        '''k=2
        for x in w.neighbours:
            # w.l[k] = 0
            if self.g[x].vertex_p[k].timestamp >= w.vertex_p[k].timestamp:
                w.l[k] += 1'''
        print("DOAGRSFP ")
        #self.edge_deletion('v8', 'v10')
        #xx = self.find_communities(6, 0)
        #print(xx, '!!!!!!!!!!!!!!!!!!!!')
        #for u_name, u in self.g.items():
            #print(u_name, u.c, len(u.vertex_p))

        '''for l in (self.top_com[1]):
            u = set()
            self.sub_tree(l, u)
            print(u, type(l))
            #break
            print(len(u), "+++++++++++++++++++++")'''

    def tester(self):
        print(self.__top_com[2])
        for i in (self.__IT[2]):
            #print(i, i.parent)
            pass
        return
        for i in self.__g.values():
            print(i, i.neighbours)
        return
        ol = 0
        tmes = []
        samples = []
        for i in range(1, self.__max_core_num):
            tttt = time.time()
            a = self.find_communities(400, i)
            if ol == len(a):
                pass
                #break
            ol = len(a)
            tt = (time.time()-tttt)
            print( tt, i, len(a))
            tmes.append(tt)
            samples.append(i)
        plt.plot(samples, tmes)
        #plt.title('TutorialKart')
        plt.xlabel('r')
        plt.ylabel('Time')
        plt.show()
        exit(2)
        #self.icp_index()
        foo = time.time() - tttt
        print("EKANA GHGPRA ", foo) #139
        tttt = time.time()

        self.__compute_cores()
        for i_n, i in self.__g.items():
            i.vertex_p = [None] * i.c

        for i in reversed(range(self.__max_core_num)):
            self.__IT.append([])
            self.__leafs.append(set())
            self.__top_com.append([])

            print("ekana gia ", i)
        for i in (range(self.__max_core_num)):
            self.__single_icp(i)
        print("EKANA arga ", time.time() - tttt)
        #print("EKANA grg ", foo)
        for i in self.__top_com:
            print(len(i))

        return



    def load(self, file='fb.txt', split_symbol=' ', comment_symbol='#'):
        start_time = time.time()
        #f = open('graph.txt', 'r')
        #f = open('amazon.txt', 'r')
        #f = open('DBLP.txt', 'r')
        self.name = file
        f = open(file, 'r', encoding='utf-8')
        for line in f:
            if line[:len(comment_symbol)] == comment_symbol:
                print("akiri grammi")
                continue
            l = line.replace('\n', '')
            l = l.split(split_symbol)
            a = str(l[0])
            b = str(l[1])
            #print(a, b)
            self.__insert_edge(a, b)


        f.close()
        print("DONE reading file/inserting: ", (time.time() - start_time) / 60)


    def __subgraph(self, u):
        k = u.c
        kcore = {}
        seen = set()
        nodes = {u}
        while len(nodes) > 0:
            temp = nodes.pop()
            temp.cd = 0
            seen.add(temp)
            kcore[temp.id] = temp
            #print(len(temp.neighbours))
            for v_name in temp.neighbours:
                v = self.__g[v_name]
                #print(v)
                if v.c < k:
                    continue
                temp.cd += 1
                if v in seen:
                    continue
                if v.c == k:
                    #print("ebala to ", v)
                    nodes.add(v)
           # print("==")
        return kcore

    def __insert_fast(self, u_name, v_name):
        u = self.__g[u_name]
        v = self.__g[v_name]
        if u.c < v.c:
            r = u
        else:
            r = v
        self.__insert_edge(u_name, v_name)
        sub = self.__subgraph(r)
        #print("trxon k", r.c)
       #for i in sub.values():
         #   print(i.id, i.degree, i.cd)
        k = r.c
        mcd = 0
        vert = [u for u_name, u in sorted(sub.items(), key=lambda kv: kv[1].cd, reverse=False)]
        for i in range(len(vert)):
            vert[i].degree = len(vert[i].neighbours)
            #print(vert[i], vert[i].degree, vert[i].c, vert[i].c2, vert[i].support)
            vert[i].pos = i
            if vert[i].cd > mcd:
                mcd = vert[i].cd

        b = [None] * (mcd + 1)  # one for zero cd
        for i in range(len(vert)):
            b[vert[i].cd] = i
        if vert[-1].c > self.__max_core_num:
            self.__max_core_num = vert[i].c
            print("kati egine")

        res =""
        for i in vert:
            res += "" + str(i.id) + ":" + str(i.pos) + " "
        print(res)
        print(b)

        for i in range(len(vert)):
            if vert[i].cd <= k:
                for v_name in vert[i].neighbours:
                    v = self.__g[v_name]
                    if v.c != k:
                        continue
                    if v.cd > vert[i].cd:
                        v.cd += -1
                        # Reorder
                        p = v.cd
                        while b[p] == None:  # find pointer of previous bin
                            p += -1
                        b[v.cd] = b[p] + 1

                        if b[v.cd] == b[v.cd + 1]:
                            b[v.cd + 1] = None
                        print(v.pos, vert[-1].pos)
                        temp = vert[v.pos]
                        temppos = vert[v.pos].pos
                        temppos2 = vert[b[v.cd]].pos
                        vert[v.pos] = vert[b[v.cd]]
                        vert[v.pos].pos = temppos  # vert[b[v.degree]].pos

                        temppos = vert[b[v.cd]].pos
                        vert[b[v.cd]] = temp
                        vert[b[v.cd]].pos = temppos2
            else: # vert[i].cd > k
                #print("NEO KORSE")
                vert[i].c += 1
                vert[i].vertex_p.append(None)
                vert[i].l.append(0)
        if vert[-1].c > self.__max_core_num:
            self.__max_core_num = vert[i].c
            print("kati egine")
        res =""
        for i in vert:
            res += "" + str(i.id) + ":" + str(i.pos) + " "
        print(res)
        print(b)


    def __delete_fast(self, u_name, v_name):
        u = self.__g[u_name]
        v = self.__g[v_name]
        if u.c < v.c:
            r = u
        else:
            r = v
        u.neighbours.remove(v_name)
        u.degree += -1
        v.neighbours.remove(u_name)
        v.degree += -1
        if u.c != v.c:
            sub = self.__subgraph(r)
            print("exo idio")
        else:
            sub = self.__subgraph(u)
            sub2 = self.__subgraph(v)
            sub.update(sub2)
            print("exo diaforetiko")
        print(type(sub))
        k = r.c

        mcd = 0
        vert = [u for u_name, u in sorted(sub.items(), key=lambda kv: kv[1].cd, reverse=False)]
        for i in range(len(vert)):
            vert[i].degree = len(vert[i].neighbours)
            # print(vert[i], vert[i].degree, vert[i].c, vert[i].c2, vert[i].support)
            vert[i].pos = i
            if vert[i].cd > mcd:
                mcd = vert[i].cd

        b = [None] * (mcd + 1)  # one for zero cd
        for i in range(len(vert)):
            b[vert[i].cd] = i

        # res = ""
        # for i in vert:
        #     res += "" + str(i.id) + ":" + str(i.pos) + " "
        # print(res)
        # print(b)

        for i in range(len(vert)):
            if vert[i].cd < k:
                print("meiosa===============================================================", vert[i], vert[i].c, vert[i].degree, vert[i].cd, len(vert[i].neighbours))
                vert[i].c += -1
                del vert[i].vertex_p[-1]
                del vert[i].l[-1]
                for v_name in vert[i].neighbours:
                    v = self.__g[v_name]
                    if v.c != k:
                        continue
                    if v.cd > vert[i].cd:
                        v.cd += -1
                        # Reorder
                        p = v.cd
                        while b[p] == None:  # find pointer of previous bin
                            p += -1
                        b[v.cd] = b[p] + 1

                        if b[v.cd] == b[v.cd + 1]:
                            b[v.cd + 1] = None
                        #print(v.pos, vert[-1].pos)
                        temp = vert[v.pos]
                        temppos = vert[v.pos].pos
                        temppos2 = vert[b[v.cd]].pos
                        vert[v.pos] = vert[b[v.cd]]
                        vert[v.pos].pos = temppos  # vert[b[v.degree]].pos

                        temppos = vert[b[v.cd]].pos
                        vert[b[v.cd]] = temp
                        vert[b[v.cd]].pos = temppos2
            else:  # vert[i].cd > k
                break
        if vert[-1].c > self.__max_core_num:
            self.__max_core_num = vert[i].c
            print("kati egine")
        # res = ""
        # for i in vert:
        #     res += "" + str(i.id) + ":" + str(i.pos) + " "
        # print(res)
        # print(b)

    def no_nodes(self):
        n = 0
        for i in self.__IT:
            n += len(i)

        return "MPAMPI"

    def no_nodes2(self):
        n = 0
        for i in self.__IT:
            for j in i:
                n += len(j.value)

        return n


g = {"v1": Node("v1", 1, ['v2', 'v3', 'v8', 'v13', 'v15']),
     "v2": Node("v2", 2, ['v1', 'v8']),
     "v3": Node("v3", 3, ['v1', 'v4', 'v5']),
     "v4": Node("v4", 4, ['v3', 'v5']),
     "v5": Node("v5", 5, ['v3', 'v4']),
     "v6": Node("v6", 6, ['v7', 'v9', 'v10', 'v11']),
     "v7": Node("v7", 7, ['v6', 'v10', 'v11']),
     "v8": Node("v8", 8, ['v1', 'v2', 'v9', 'v11']),
     "v9": Node("v9", 9, ['v6', 'v8', 'v10', 'v11']),
     "v10": Node("v10", 10, ['v6', 'v7', 'v9']),
     "v11": Node("v11", 11, ['v6', 'v7', 'v8', 'v9']),
     "v12": Node("v12", 12, ['v13', 'v14', 'v15']),
     "v13": Node("v13", 13, ['v1', 'v12', 'v14', 'v15']),
     "v14": Node("v14", 14, ['v12', 'v13', 'v15']),
     "v15": Node("v15", 15, ['v1', 'v12', 'v13', 'v14'])

     }

def start2():
    print("kalesa start")
    tt = Graph()
    tt.load()
    #tt.find_cores()
    tt.icp_index()
    #tt.compute_cores()
    sta = time.time()
    tt.tester()
    print("icp build in ", time.time() - sta)

#sys.setrecursionlimit(10000)
#sys.setrecursionlimit(1000)
#threading.stack_size(250000000)
#thread = threading.Thread(target=start2())
#thread.start()

#tt.print()

