from collections.abc import Sequence
def routes_to_add(routes: Sequence[tuple[str, str]]) -> int:
    nodes = set()
    for i,j in routes:
        nodes.add(i)
        nodes.add(j)
    nodes = {j:i for i,j in enumerate(nodes)}
    n = len(nodes.keys())
    if n == 0:
        return 0
    edges = set()
    for i,j in routes:
        if nodes[i] != nodes[j]:
            edges.add((nodes[i],nodes[j]))
    adj =  [[] for _ in range(n)]
    adj_trans = [[] for _ in range(n)]
    for i,j in edges:
        adj[i].append(j)
        adj_trans[j].append(i)
    visited =[False]*n
    finish = []
    for start in range(n):
        if visited[start]:
            continue
        stack = [(start, 0)]  # (node, state): state 0 = enter, 1 = exit
        while stack:
            node, state = stack.pop()
            if state == 1:
                finish.append(node)
                continue
            if visited[node]:
                continue
            visited[node] = True
            stack.append((node, 1))          
            for j in adj[node]:
                stack.append((j, 0))
    visited = [False] * n
    sccs = []
    for node in reversed(finish):
        if visited[node]:
            continue
        comp = []
        stack = [node]
        while stack:
            u = stack.pop()
            if visited[u]:
                continue
            comp.append(u)
            visited[u] = True
            for v in adj_trans[u]:
                stack.append(v)
        sccs.append(comp)
    if len(sccs) == 1:
        return n*(n-1)
    scc_dict = {i:-1 for i in range(n)}
    m = len(sccs)
    sizes = [0 for _ in range(m)]
    for i in range(m):
        sizes[i] = len(sccs[i])
        for j in sccs[i]:
            scc_dict[j] = i
    condensed_adj =  [set() for _ in range(m)]
    for i in range(n):
        for j in adj[i]:
            if scc_dict[i] != scc_dict[j]:
                condensed_adj[scc_dict[i]].add(scc_dict[j])
    condensed_adj = [list(i) for i in condensed_adj]
    indeg = [0]*m
    outdeg = [0]*m
    for su in range(m):
        for sv in condensed_adj[su]:
            outdeg[su]+=1;indeg[sv]+=1
    start = [i for i in range(m) if indeg[i] == 0]
    end   = [i for i in range(m) if outdeg[i] == 0]
    return sizes[start[0]] * sizes[end[0]] if len(start) == 1 and len(end) == 1 else 0