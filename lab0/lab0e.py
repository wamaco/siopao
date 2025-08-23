from collections import deque

Coord = tuple[int, int]
Query = tuple[Coord, Coord]

def lowest_highest_tower(grid: list[list[int]], qs: list[Query]) -> list[int]:
    rows, cols = len(grid), len(grid[0])
    total_cells = rows * cols

    # flatten grid heights para madali index by 1D
    heights = [grid[r][c] for r in range(rows) for c in range(cols)]
    
    def cell_id(r, c):
        return r * cols + c

    # gawa ng graph edges between neighbors
    # weight = max height of the 2 cells
    edges = []
    for r in range(rows):
        for c in range(cols):
            u = cell_id(r, c)
            if r + 1 < rows:
                v = cell_id(r + 1, c)
                edges.append((max(heights[u], heights[v]), u, v))
            if c + 1 < cols:
                v = cell_id(r, c + 1)
                edges.append((max(heights[u], heights[v]), u, v))
    edges.sort(key = lambda x: x[0])

    # kruskal via dsu
    parent = list(range(total_cells))
    rank = [0] * total_cells

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]] # path comp
            x = parent[x]
        return x
    
    def unite(a, b):
        a, b = find(a), find(b)
        if a == b:
            return False
        
        if rank[a] < rank[b]:
            a, b = b, a

        parent[b] = a

        if rank[a] == rank[b]:
            rank[a] += 1

        return True

    # mst adjlist
    mst_adj = [[] for _ in range(total_cells)]
    edges_used = 0
    for w, a, b in edges:
        if unite(a, b):
            mst_adj[a].append((b, w))
            mst_adj[b].append((a, w))
            edges_used += 1
            if edges_used == total_cells - 1:
                break

    # NOTE: I tried using Lec Notes 6 implems para maka-full AC <3

    # prepro ng LCA
    log = (total_cells - 1).bit_length() # buti na lang may ganto omg
    up = [[-1] * total_cells for _ in range(log)]
    mx = [[0] * total_cells for _ in range(log)]
    depth = [-1] * total_cells

    # root tree at node 0
    dq = deque([0])
    depth[0] = 0
    while dq:
        node = dq.popleft()
        for nxt, weight in mst_adj[node]:
            if depth[nxt] == -1:
                depth[nxt] = depth[node] + 1
                up[0][nxt] = node
                mx[0][nxt] = weight
                dq.append(nxt)

    # bin lifting table
    for k in range(1, log):
        for v in range(total_cells):
            mid = up[k - 1][v]
            if mid != -1:
                up[k][v] = up[k - 1][mid]
                mx[k][v] = max(mx[k - 1][v], mx[k - 1][mid])

    # lca w/ max tracking
    def max_on_path(a, b):
        if a == b:
            return heights[a]
        res = 0
        if depth[a] < depth[b]:
            a, b = b, a
        diff = depth[a] - depth[b]
        bit = 0
        while diff:
            if diff & 1:
                res = max(res, mx[bit][a])
                a = up[bit][a]
            diff >>= 1
            bit += 1
        if a == b: return res

        # climb up powers of 2 bago mag LCA
        for k in range(log - 1, -1, -1):
            if up[k][a] != -1 and up[k][a] != up[k][b]:
                res = max(res, mx[k][a], mx[k][b])
                a, b = up[k][a], up[k][b]

        res = max(res, mx[0][a], mx[0][b])
        return res

    answers = []

    for (sr, sc), (er, ec) in qs:
        answers.append(max_on_path(cell_id(sr, sc), cell_id(er, ec)))
    return answers