from collections.abc import Sequence


def highest_compromised(values: Sequence[int], knows: Sequence[tuple[int, int]]) -> list[int]:
    n = len(values)
    if n == 0:
        return []
    adj = [[] for _ in range(n)]
    adj_trans = [[] for _ in range(n)]
    for i,j in knows:
        adj[i].append(j)
        adj_trans[j].append(i)
    finish = []
    vis = [False for _ in range(n)]
    max_arr= [values[i] for i in range(n)]
    sccs = []
    def dfs(node):
        stack = [(node,0)] #node,val,state (0 enter,1 exit)
        while stack:
            u,state = stack.pop()
            if state == 1:
                finish.append(u)
            if vis[u]:
                continue
            vis[u] = True
            stack.append((u,1))
            for i in adj[u]:
                stack.append((i,0))
            
    def dfs_trans(node):
        comps = []
        stack = [(node)] 
        while stack:
            u  = stack.pop()
            if vis[u]:
                continue
            vis[u] = True
            comps.append(u)
            for i in adj_trans[u]:
                stack.append(i)
        sccs.append(comps)

    for start in range(n):
        if not vis[start]:
            dfs(start)
    vis = [False for _ in range(n)]
    for start in finish[::-1]:
        if not vis[start]:
            dfs_trans(start)

    scc_dict = {i:0 for i in range(len(sccs))}
    scc_idx = {}
    for i in range(len(sccs)):
        scc_dict[i] = max(values[j] for j in sccs[i])
        for j in sccs[i]:
            scc_idx[j] = i
    for i in finish:
        idx = scc_idx[i]
        for j in adj[i]:
            idx_ = scc_idx[j]
            scc_dict[idx] = max(scc_dict[idx],scc_dict[idx_])
    
    max_arr = [scc_dict[scc_idx[i]] for i in range(n)]

    return max_arr

highest_compromised([40, 20, 30, 30, 10], [
        (0, 1),
        (0, 3),
        (1, 2),
        (2, 3),
        (3, 1),
        (2, 4),
    ])


highest_compromised([0, 1, 2, 3, 4, 5], [
        (5, 2),
        (2, 5),
        (2, 3),
        (3, 1),
        (1, 3),
        (4, 0),
    ])



highest_compromised([0, 1,2], [
    ])


highest_compromised([0, 1,2,3], [
    (0,1),
    (1,2),
    (1,3)
    ])
