# hint: smallest spread
# runtime: O(n log n)
# technique used: modified sliding window problem with array indexing

def best_rolls(softness_vals: list[int], k: int) -> list[int]:
    n: list[tuple[int, int]] = sorted((val, i) for i, val in enumerate(softness_vals))
    curr_min: int | None = None
    best_start = 0
    for i in range(len(n) - k + 1):
        spread = n[i+k-1][0] - n[i][0] # O(1) access
        if curr_min is None or curr_min > spread: # needs update
            curr_min = spread
            best_start = i
    best_window = n[best_start:best_start+k]
    a = [i[1] for i in best_window]
    return sorted(a)
