from collections.abc import Sequence
from collections import defaultdict
def all_jammables(freqs_of_radios: Sequence[Sequence[int]]) -> list[tuple[int, int]]:
    n= len(freqs_of_radios)
    freqs_dict = defaultdict(list)
    for i,j in enumerate(freqs_of_radios):
        for k in j:
            freqs_dict[k].append(i)
    #bipartite graph freq->guard
    freqs = list(freqs_dict.keys())
    m = len(freqs)
    total_n = n + m
    adj = defaultdict(list)
    for i,j in freqs_dict.items():
        for k in j:
            adj[k].append(n+i)
            adj[i+n].append(k)
    nodes = list(adj.keys())
    disc = {i:-1 for i in nodes}
    low = {i:-1 for i in nodes}
    parent = {i:-1 for i in nodes}
    time = 0
    bridges = []
    artic_points = set()
    for start in nodes:
        if disc[start] != -1:
            continue
        # stack items: (node, child_idx, is_root, child_count, has_breakable_child)
        stack = [(start, 0, True, 0, False)]
        while stack:
            node, child_idx, is_root, child_count, has_breakable_child = stack.pop()
            if child_idx == 0:  
                disc[node] = low[node] = time
                time += 1
            finished = True
            while child_idx < len(adj[node]):
                j = adj[node][child_idx]
                child_idx += 1
                if disc[j] == -1:  # tree edge
                    parent[j] = node
                    child_count += 1
                    stack.append((node, child_idx, is_root, child_count, has_breakable_child))
                    stack.append((j, 0, False, 0, False))
                    finished = False
                    break
                elif j != parent[node]:  # back edge
                    low[node] = min(low[node], disc[j])
            if not finished:
                continue
            for j in adj[node]:
                if parent[j] == node:
                    low[node] = min(low[node], low[j])
                    if low[j] > disc[node]:
                        bridges.append((max(node, j)-n,min(node,j)))
                    if low[j] >= disc[node]:
                        has_breakable_child = True
            if (is_root and child_count >= 2) or (not is_root and has_breakable_child):
                artic_points.add(node)
    bridges = [(i,j) for i,j in bridges if len(adj[i+n]) > 1]
    return bridges


assert sorted(all_jammables([[10, 11], [10, 11], [10, 20, 21], [20, 21]])) ==sorted([(10, 2)])
assert sorted(all_jammables([[10, 11], [10, 11], [10, 20, 21], [20, 21],[10]])) == sorted([(10, 2),(10,4)])
assert all_jammables([[100, 101], [101, 102], [102, 103], [103, 100]]) == []
assert all_jammables([[50, 51, 52, 53, 54], [53, 54, 55, 56]]) == []
