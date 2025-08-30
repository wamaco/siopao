from heapq import heappop, heappush

class BizarreBuilding:
    def __init__(self, n: int, x: int, c: int, y: int, d: int, e: int, f: int):
        self.n = n
        self.x = x
        self.c = c
        self.y = y
        self.d = d
        self.e = e
        self.f = f
        super().__init__()

    def shortest_escape_time(self, s: int, t: int) -> int:
        min_time = [float("inf")] * self.n
        min_time[s] = 0

        pq = [(0, s)]

        while pq:
            current_time, current_floor = heappop(pq)
            if current_time > min_time[current_floor]:
                continue
            if current_floor == t:
                return current_time

            # case 1: jump up
            next_floor = current_floor + self.x
            if next_floor < self.n:
                new_time = current_time + self.c
                if new_time < min_time[next_floor]:
                    min_time[next_floor] = new_time
                    heappush(pq, (new_time, next_floor))

            # case 2: jump down
            next_floor = current_floor - self.y
            if next_floor >= 0:
                new_time = current_time + self.d
                if new_time < min_time[next_floor]:
                    min_time[next_floor] = new_time
                    heappush(pq, (new_time, next_floor))

            # case 3: step up
            next_floor = current_floor + 1
            if next_floor < self.n:
                new_time = current_time + self.e
                if new_time < min_time[next_floor]:
                    min_time[next_floor] = new_time
                    heappush(pq, (new_time, next_floor))

            # case 4: step down
            next_floor = current_floor - 1
            if next_floor >= 0:
                new_time = current_time + self.f
                if new_time < min_time[next_floor]:
                    min_time[next_floor] = new_time
                    heappush(pq, (new_time, next_floor))

        return -1