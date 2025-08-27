from collections.abc import Sequence

class Edge:
    def __init__(self, x: int, y: int, cost: int):
        self.x = x
        self.y = y
        self.cost = cost

    def __lt__(self, other):
        return self.cost < other.cost
    
class UnionFind:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, node):
        if self.parent[node] == node:
            return node
        return self.find(self.parent[node])
    
    def union(self, i: int, j: int):
        root_1 = self.find(i)
        root_2 = self.find(j)

        if root_1 != root_2:
            if self.rank[root_1] > self.rank[root_2]:
                self.parent[root_2] = root_1
            elif self.rank[root_2] > self.rank[root_1]:
                self.parent[root_1] = root_2
            else:
                self.parent[root_2] = root_1
                self.rank[root_1] += 1

def min_ladders(mountain: Sequence[Sequence[int]]) -> int:
    row, col = len(mountain), len(mountain[0])
    edge_list: list[Edge] = []

    # convert each (i, j) into a index for easier usage
    def index(i, j):
        return i * col + j
    
    # edge generation
    for i in range(row):
        for j in range(col):
            if (j + 1) < col:
                edge_list.append(Edge(index(i, j), index(i, j+1), abs(mountain[i][j] - mountain[i][j + 1])))
            if (i + 1) < row:
                edge_list.append(Edge(index(i, j), index(i+1, j), abs(mountain[i][j] - mountain[i + 1][j])))
    
    # sort the edges by increasing cost
    edge_list.sort()

    # implem of union find for Kruskal's MST
    uf  = UnionFind(row * col)
    needed_ladders: int = 0
    edge_count: int = 0

    for edge in edge_list:
        if uf.find(edge.x) != uf.find(edge.y):
            uf.union(edge.x, edge.y)
            needed_ladders += edge.cost
            edge_count += 1

            if edge_count == (row * col + 1):
                break

    return needed_ladders

"""
Problem Statement:

Steve is climbing a mountain.

The mountain can be represented as an r×c grid of numbers.
We number the rows 0 to r−1 from top to bottom, and the columns 0 to c−1 from left to right.
Each cell of this grid represents a 1×1 portion of the mountain when viewed from the top.
The cell at row i and column j contains an integer denoting the elevation of the cell.
All units are in meters.

From a cell (i,j), Steve can only move to one of the cells directly north, south, east, or west of that cell, if it exists.
No other movements are allowed.
In addition, if there is an elevation difference of Δh between the two cells,
    Steve will need to use Δh ladders to safely move between these two cells.
That is, you can only go to a cell if either it has the same height, or you've placed Δh ladders between them.

He wants to find out what the view is like from every cell on the mountain.
Of course, the simple solution is to just place ladders between every pair of adjacent cells with differing heights.
But Steve doesn't have enough ladders, so Steve would like to minimize the number of ladders needed.

Can you help him out?
"""
