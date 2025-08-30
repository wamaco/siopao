from collections.abc import Sequence

def to_kilimanjaro(M: Sequence[Sequence[int]]) -> int:
    rows, cols = len(M), len(M[0])

    best_cost = [float("inf")] * rows
    best_cost[0] = M[0][0]

    for r in range(1, rows):
        best_cost[r] = best_cost[r-1] + M[r][0]

    for col in range(1, cols):
        new_costs = [best_cost[r] + M[r][col] for r in range(rows)]

        for r in range(1, rows):
            new_costs[r] = min(new_costs[r], new_costs[r-1] + M[r][col])

        for r in range(rows-2, -1, -1):
            new_costs[r] = min(new_costs[r], new_costs[r+1] + M[r][col])

        best_cost = new_costs

    return int(best_cost[-1])
