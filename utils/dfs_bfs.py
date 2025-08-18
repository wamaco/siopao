adjlist = {
    1: [2, 3],
    2: [4, 5],
    3: [6],
    4: [],
    5: [],
    6: []
}

"""
DFS(node):
    if node is already visited:
        return

    mark node as visited

    for each neighbor of node:
        DFS(neighbor)

"""
def dfs(node: int, adj_list: dict[int, list[int]], visited: set, answer: list[int]):
    if node in visited:
        return
    
    visited.add(node)
    answer.append(node)

    for neighbor in adj_list[node]:
        dfs(neighbor, adj_list, visited, answer)

    return answer

"""
BFS(start):
    create an empty queue
    enqueue(start)
    mark start as visited

    while queue is not empty:
        node = dequeue from front
        for each neighbor of node:
            if neighbor is not visited:
                enqueue(neighbor)
                mark neighbor as visited

"""
from collections import deque

def bfs(node: int, adj_list: dict[int, list[int]], visited: set, answer: list[int]) -> list[int]:
    visited = set([node])
    answer = []
    queue = deque([node])

    while len(queue) > 0:
        curr_node = queue.popleft()
        answer.append(curr_node)

        for neighbor in adj_list[curr_node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return answer

print(dfs(1, adjlist, set(), []))
print(bfs(1, adjlist, set(), []))
