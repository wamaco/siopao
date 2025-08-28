from collections.abc import Sequence
from dataclasses import dataclass
from itertools import combinations
from typing import Literal

@dataclass
class Edge:
    i: int
    j: int
    cost: int

class UF:
    def __init__(self, n):
        self.parent = [*range(n)]
        self.weight = [1]*n
        super().__init__()

    def __getitem__(self, i):
        if self.parent[i] == i:
            return i
        else:
            self.parent[i] = self[self.parent[i]]
            return self.parent[i]
        
    def unite(self, i, j):
        if (i := self[i]) == (j := self[j]):
            return False
        if self.weight[i] > self.weight[j]:
            i, j = j, i
        self.weight[j] += self.weight[i]
        self.parent[i] = j
        return True
    
def mst(n: int, edges: Sequence[Edge]) -> list[Edge]:
    tree = []
    comps = UF(n)
    for edge in sorted(edges, key=lambda edge: edge.cost)[::-1]:
        if comps.unite(edge.i, edge.j):
            tree.append(edge)

    return tree

def mst_cost(n, edges):
    return sum(edge.cost for edge in mst(n, edges))

Plan = Literal["Premium", "Premium_Pro", "Premium_Deluxe"]
P = "Premium"
PP = "Premium_Pro"
PD = "Premium_Deluxe"

def make_edgelist(plans: Sequence[Plan]) -> list[Edge]:
    s = len(plans)
    edgelist = []
    combos = combinations(range(s), 2)
    for combo in combos:
        i, j = combo
        if plans[i] == plans[j]:
            c = abs(i - j)
            edgelist.append(Edge(i, j, c))
        elif (plans[i] == P and plans[j] == PP) or (plans[j] == P and plans[i] == PP):
            c = abs(i - j) * 5
            edgelist.append(Edge(i, j, c))
        elif (plans[i] == PP and plans[j] == PD) or (plans[j] == PP and plans[i] == PD):
            c = abs(i - j) * 10
            edgelist.append(Edge(i, j, c))
        elif (plans[i] == P and plans[j] == PD) or (plans[j] == P and plans[i] == PD):
            c = abs(i - j) * 25
            edgelist.append(Edge(i, j, c))
    return edgelist


def get_max_profit(subscription_plan: Sequence[Plan]) -> int:
    s = len(subscription_plan)
    edges = make_edgelist(subscription_plan)
    return mst_cost(s, edges)
