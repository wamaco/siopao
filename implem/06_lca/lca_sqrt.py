from collections.abc import Sequence
from dataclasses import dataclass, field
from math import sqrt


@dataclass
class Node:
    label: int
    parent: "Node | None" = None
    children: "list[Node]" = field(default_factory=list)
    depth: int = 0
    jump: "Node | None" = None
    # node.jump is the ancestor of this node k steps up

    def compute_stuff(self, k, ancestors):
        self.jump = ancestors[-k] if len(ancestors) >= k else ancestors[0]

        ancestors.append(self)
        for child in self.children:
            child.depth = self.depth + 1
            child.compute_stuff(k, ancestors)
        ancestors.pop()

    def ascend(self, d):
        curr = self

        # big jumps
        while curr.depth > curr.jump.depth >= d:
            curr = curr.jump

        # small jumps
        while curr.depth > d:
            curr = curr.parent

        assert curr.depth <= d
        return curr

    def __eq__(self, other):
        return self.label == other.label

    def __ne__(self, other):
        return self.label != other.label


class RootedTree:
    def __init__(self, parent: Sequence[int], root: int):
        self.n = n = len(parent)
        # nodes are labelled 0 to n-1
        # node parent[i] is the root of node i
        # node 'root' is the root
        self.nodes = [Node(label=i) for i in range(n)]

        # set up root, parent and children pointers
        self.root = self.nodes[root]
        self.root.parent = self.root
        for i in range(n):
            if i != root:
                self.nodes[i].parent = self.nodes[parent[i]]
                self.nodes[parent[i]].children.append(self.nodes[i])

        # DFS to compute stuff
        k = int(sqrt(n))
        self.root.compute_stuff(k, [self.root])

        super().__init__()

    def lca(self, i, j):
        # get node objects
        i = self.nodes[i]
        j = self.nodes[j]

        # make them the same depth
        i = i.ascend(j.depth)
        j = j.ascend(i.depth)
        assert i.depth == j.depth

        # big jumps
        while i.jump != j.jump:
            i = i.jump
            j = j.jump

        # small jumps
        while i != j:
            i = i.parent
            j = j.parent

        return i.label


def main():
    tree = RootedTree([None, 0, 0, 1, 1], 0)

    assert tree.lca(1, 0) == 0
    assert tree.lca(2, 3) == 0
    assert tree.lca(1, 3) == 1
    assert tree.lca(3, 4) == 1


if __name__ == '__main__':
    main()
