from dataclasses import dataclass
from collections.abc import Sequence

@dataclass
class Edge:
    i: int
    j: int
    cost: int = 1

def make_adjacency_list(n: int, edges: Sequence[Edge], directed=False):
    adj = [[] for _ in range(n)]
    for idx, e in enumerate(edges):
        adj[e.i].append((e.j, e.cost, idx, e))
        if not directed:
            adj[e.j].append((e.i, e.cost, idx, e))
    return adj

def bridges_articulation_points_and_bccs(n, edges):
    if any(e.i == e.j for e in edges):
        raise NotImplementedError("self-loops not supported")

    adj = make_adjacency_list(n, edges)
    vis, low = [-1]*n, [-1]*n
    time = 0
    bridges, artic_points, bccs = [], [], []
    edge_visited = [False]*len(edges)
    edge_stack = []

    def dfs(u, parent_edge=None):
        nonlocal time
        vis[u] = low[u] = time
        time += 1
        children = 0
        is_artic = False

        for v, _, idx, e in adj[u]:
            if edge_visited[idx]:
                continue
            edge_visited[idx] = True

            if vis[v] == -1:  # Tree edge
                edge_stack.append(e)
                dfs(v, e)
                low[u] = min(low[u], low[v])
                children += 1

                if low[v] > vis[u]:
                    bridges.append(e)
                if low[v] >= vis[u]:
                    is_artic = True
                    bcc = []
                    while edge_stack:
                        last = edge_stack.pop()
                        bcc.append(last)
                        if last == e:
                            break
                    bccs.append(bcc)
            elif e is not parent_edge:  # Back edge
                edge_stack.append(e)
                low[u] = min(low[u], vis[v])

        if (parent_edge and is_artic) or (parent_edge is None and children >= 2):
            artic_points.append(u)

    if n:
        dfs(0)

    return bridges, artic_points, bccs
