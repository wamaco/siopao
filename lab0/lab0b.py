"""
function is_safe(coord, grid):
    (r, c) = coord
    return True if r and c are inside grid bounds
    else return False

# Possible directions to move: right, left, down, up
dirs = [(0,1), (0,-1), (1,0), (-1,0)]

function least_jumps(grid, d, u, s, e):
    if s == e:              # base case: start == end
        return 0
    
    visited = {s}           # keep track of visited cells
    queue = deque([(s, 0)]) # BFS queue stores (coordinate, distance_so_far)

    while queue not empty:
        (cr, cc), dist = queue.pop_left()   # take the next cell

        for each (dr, dc) in dirs:          # explore 4 neighbors
            nr, nc = cr+dr, cc+dc           # compute neighbor coordinates

            if is_safe((nr,nc), grid):      # if inside grid
                height_diff = grid[nr][nc] - grid[cr][cc]

                # check if the move is allowed
                if height_diff > u: continue   # too high to climb up
                if height_diff < -d: continue  # too steep to drop down

                # check if we've reached the end
                if (nr, nc) == e:
                    return dist + 1

                # if this neighbor hasn't been visited
                if (nr, nc) not in visited:
                    mark (nr,nc) visited
                    add ((nr,nc), dist+1) to queue

    return None   # no path from s to e found
"""

Coord = tuple[int, int]

# helper function to check if current coord is in bounds of the given grid
def is_safe(coord: Coord, grid: list[list[int]]) -> bool:
    r, c = coord
    if 0 <= r < len(grid) and 0 <= c < len(grid[0]):
        return True
    else:
        return False

dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)] # up, down, left, right

from collections import deque

def least_jumps(grid: list[list[int]], d: int, u: int, s: Coord, e: Coord) -> int | None:
    if s == e: # base case: starting point IS the end point
        return 0
    
    visited = set([s])
    queue = deque([(s, 0)])

    while len(queue) > 0: # while there's still something in the queue...
        (cr, cc), dist = queue.popleft() # get the current cell's info
        for r, c in dirs: # up, down, left, right
            nr, nc = cr+r, cc+c

            if is_safe((nr, nc), grid): # if current move is in bounds
                # 1st check: if it is safe to JUMP
                height_diff = grid[nr][nc] - grid[cr][cc]
                if height_diff > u: # too tall
                    continue
                if height_diff < -d: # too deep (pause)
                    continue
                
                # 2nd check: sensus ahh
                if (nr, nc) == e: # if current neighbor is the end point
                    return dist + 1
                if (nr, nc) not in visited: # just the usual neighbor
                    visited.add((nr, nc))
                    queue.append(((nr, nc), dist+1))

    return None # this means the BFS has finished and it didn't find a path s -> e