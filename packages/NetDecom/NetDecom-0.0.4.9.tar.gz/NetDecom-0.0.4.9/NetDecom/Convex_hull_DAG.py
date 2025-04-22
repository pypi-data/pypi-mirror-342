#This is a convex hull algorithm that absorbs minimal separations, inputs the directed graph and sets of concerns, and obtains the convex hull.
import networkx as nx
from collections import deque
from itertools import chain

class Convex_hull_DAG:
    def __init__(self, graph):
        self.graph = graph

    def Reachable(self, G, x, a, z):
        def _pass(e, v, f, n):
            is_element_of_A = n in a
            # almost_definite_status = True  # always true for DAGs; not so for RCGs
            collider_if_in_Z = v not in z or (e and not f)
            return is_element_of_A and collider_if_in_Z  # and almost_definite_status

        queue = deque([])
        for node in x:
            if bool(G.pred[node]):
                queue.append((True, node))
            if bool(G.succ[node]):
                queue.append((False, node))
        processed = queue.copy()

        while any(queue):
            e, v = queue.popleft()
            preds = ((False, n) for n in G.pred[v])
            succs = ((True, n) for n in G.succ[v])
            f_n_pairs = chain(preds, succs)
            for f, n in f_n_pairs:
                if (f, n) not in processed and _pass(e, v, f, n):
                    queue.append((f, n))
                    processed.append((f, n))

        return {w for (_, w) in processed}


    def FCMS(self,g,u,v):
        nodeset = {u} | {v} 
        ancestors_u_v_included = nodeset.union(*[nx.ancestors(g, node) for node in nodeset])
        An = nx.subgraph(g, ancestors_u_v_included)
        mb_u = set([parent for child in An.successors(u) for parent in An.predecessors(child)]) | set(An.successors(u)) | set(An.predecessors(u))
        mb_u.discard(u)
        reach_v = self.Reachable(g, {v}, ancestors_u_v_included, mb_u)
        return mb_u & reach_v

    def CMDSA(self,r):
        g = self.graph
        ang = nx.subgraph(g, r.union(*[nx.ancestors(g, node) for node in r]))
        h = r
        s = 1
        mark = set()
        while s:
            s = 0
            Q = set()
            m = set(g.nodes)-h
            mb = nx.node_boundary(g, m, h)
            h_ch_in_m = nx.node_boundary(g, h, m)
            for v in mb:
                pa = set(g.predecessors(v))
                Q |= (pa & h)
            for v in h_ch_in_m:
                Q |= (h & set(g.predecessors(v)))
            Q |= mb
            if len(Q)>1:
                for a in Q.copy():
                    Q.remove(a)
                    for b in Q:                    
                        if (a,b) not in mark and g.has_edge(a, b)==False: 
                            mark.add((a,b))
                            mark.add((b,a))
                            if g.has_edge(b,a)==False: 
                                S_a = self.FCMS(ang,a,b)                           
                                if not S_a:
                                    continue
                                S_b = self.FCMS(ang,b,a)
                                if ( S_a | S_b) - (( S_a | S_b) & h):
                                    s = 1
                                    h |= ( S_a | S_b)  
                                    break               
                    else:
                        continue
                    break
        return h
    
#from Convex_hull_DAG import *
#hull = Convex_hull_DAG(G)
#hull.CMDSA(R)