from collections.abc import Sequence
from heapq import heappop, heappush

def to_kilimanjaro(M: Sequence[Sequence[int]]) -> int:
    r, c = len(M), len(M[0])
    target = (r - 1, c - 1)
    min_f = [[float("inf")] * c for _ in range(r)]
    min_f[0][0] = M[0][0]
    pq = [(M[0][0], 0, 0)]
    while pq:
        cf, row, col = heappop(pq)
        if cf > min_f[row][col]:
            continue
        if (row, col) == target:
            return cf
        for dr, dc in ((1, 0), (-1, 0), (0, 1)):
            nr, nc = row + dr, col + dc
            if 0 <= nr < r and 0 <= nc < c:
                nf = cf + M[nr][nc]
                if nf < min_f[nr][nc]:
                    min_f[nr][nc] = nf
                    heappush(pq, (nf, nr, nc))
    return -1