from collections.abc import Sequence
def defusing_batteries(n: int, wires: Sequence[tuple[int, int]]) -> list[int]:
    if n < 3:
        return []
    adj = [set() for _ in range(n)]
    for i,j in wires:
        if i != j:
            adj[i].add(j)
            adj[j].add(i)
    adj = [list(i) for i in adj]
    disc = [-1]*n  
    low = [-1]*n   
    parent = [-1]*n
    time = 0
    bridges = []
    artic_points = set()
    for start in range(n):
        if disc[start] != -1:
            continue
        stack = [(start, 0, True, 0, 0)]
        while stack:
            node, child_idx, is_root, child_count, has_breakable_child = stack.pop()
            if child_idx == 0:  
                disc[node] = low[node] = time
                time += 1
            finished = True
            while child_idx < len(adj[node]):
                j = adj[node][child_idx]
                child_idx += 1
                if disc[j] == -1: 
                    parent[j] = node
                    child_count += 1
                    stack.append((node, child_idx, is_root, child_count, has_breakable_child))
                    stack.append((j, 0, False, 0, 0))
                    finished = False
                    break
                elif j != parent[node]:  
                    low[node] = min(low[node], disc[j])
            if not finished:
                continue
            for j in adj[node]:
                if parent[j] == node:
                    low[node] = min(low[node], low[j])
                    if low[j] > disc[node]:
                        bridges.append((node, j))
                    if low[j] >= disc[node]:
                        has_breakable_child += 1
            if (is_root and child_count >= 3) or (not is_root and has_breakable_child >= 2):
                artic_points.add(node)
    return sorted(artic_points)