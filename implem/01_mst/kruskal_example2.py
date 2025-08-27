from collections.abc import Sequence

"""
Specs:
points of interest = vertices
minecart lines = edges
edges are made up of w minecart tracks = weight of each edge
undirected graph; no loops

Goal:
removed_track = track.pop() sum should be maximized
should return a connected graph with minimized number of lines/edges

Formally, the function will input a sequence of Lines and will output
a 2-tuple of the max weight that it removed and a list of the edges it removed,
where the list of removed edges are aliased as 1-indexed numbers
"""

class Edge:
    def __init__(self, x, y, cost, index):
        self.x = x
        self.y = y
        self.cost = cost
        self.index = index
    
    def __lt__(self, other):
        return self.cost < other.cost

class UnionFind:
    def __init__(self, n: int):
        self.parent = list(range(n + 1))
        self.rank = [0] * (n + 1)
    
    def find(self, elem: int):
        if self.parent[elem] == elem:
            return elem
        return self.find(self.parent[elem])
    
    def union(self, x: int, y: int) -> bool:
        rt1 = self.find(x)
        rt2 = self.find(y)

        if rt1 != rt2:
            if self.rank[rt1] > self.rank[rt2]:
                self.parent[rt2] = rt1
            elif self.rank[rt2] > self.rank[rt1]:
                self.parent[rt1] = rt2
            else:
                self.parent[rt2] = rt1
                self.rank[rt1] += 1
            return True
        return False

Line = tuple[tuple[int, int], int] # ((u_i, v_i), w_i)

def max_tracks(n: int, lines: Sequence[Line]) -> tuple[int, list[int]]:
    edge_list: list[Edge] = []
    total_weight: int = 0

    for index, elem in enumerate(lines, start=1):
        x, y = elem[0]
        weight = elem[1]
        edge_list.append(Edge(x, y, weight, index))
        total_weight += weight

    edge_list.sort()

    uf = UnionFind(n)
    mst_weight: int = 0
    mst_edges: set[int] = set()

    for edge in edge_list:
        if uf.union(edge.x, edge.y):
            mst_weight += edge.cost
            mst_edges.add(edge.index)

    removed_weight = total_weight - mst_weight
    removed_edges = [edge.index for edge in edge_list if edge.index not in mst_edges]

    return removed_weight, removed_edges
