from dataclasses import dataclass
from math import isqrt

 
@dataclass
class Node:  # [i, j)
    i: int
    j: int
    val: int
    l: "Node | None" = None
    r: "Node | None" = None


    @classmethod
    def make(cls, seq, i, j):
        # make a tree on indices [i, j)
        if j - i == 1:
            return cls(i=i, j=j, val=seq[i])
        else:
            k = (i + j) // 2
            assert i < k < j
            l = cls.make(seq, i, k)
            r = cls.make(seq, k, j)
            return cls(i=i, j=j, val=min(l.val, r.val), l=l, r=r)


    @property
    def is_leaf(self):
        return self.j - self.i == 1


    def range_min(self, i, j):
        if i <= self.i and self.j <= j:
            # the interval of this node is completely contained
            # in the query interval
            return self.val
        elif j <= self.i or self.j <= i:
            # the intervals are completely disjoint
            return float('inf')
        else:
            # partially overlapping
            l_ans = self.l.range_min(i, j)
            r_ans = self.r.range_min(i, j)
            return min(l_ans, r_ans)


    def set(self, i, v):
        if not (self.i <= i < self.j):
            return

        if self.is_leaf:
            self.val = v
        else:
            self.l.set(i, v)
            self.r.set(i, v)
            self.val = min(self.l.val, self.r.val)


class RangeMin:
    def __init__(self, seq):
        self.seq = list(seq)
        self.n = len(seq)
        self.root = Node.make(seq, 0, self.n)
        super().__init__()


    def range_min(self, i, j):  # [i, j), include i, exclude j
        assert 0 <= i < j <= self.n
        return self.root.range_min(i, j)


    def __setitem__(self, i, v):
        assert 0 <= i < self.n
        self.root.set(i, v)


def main():
    r = RangeMin([3, 1, 4, 1, 5, 9, 2, 6])

    print(r.range_min(1, 5))  # 1
    print(r.range_min(4, 7))  # 2
    print(r.range_min(4, 6))  # 5


if __name__ == '__main__':
    main()
