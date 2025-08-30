from collections.abc import Sequence
from heapq import heappush, heappop

Road = tuple[str, str, int]

class Navigator:
    def __init__(self, roads: Sequence[Road]):
        self.graph: dict[str, list[tuple[str, int, Road]]] = {}
        for source, destination, time in roads:
            if source not in self.graph:
                self.graph[source] = []
            if destination not in self.graph:
                self.graph[destination] = []
            self.graph[source].append((destination, time, (source, destination, time)))
        super().__init__()

    def _dijkstra(self, start: str, target: str) -> list[Road] | None:
        shortest_time = {node: float("inf") for node in self.graph}
        previous: dict[str, tuple[str, Road] | None] = {node: None for node in self.graph}

        shortest_time[start] = 0
        priority_queue = [(0, start)]

        while priority_queue:
            current_time, current_location = heappop(priority_queue)
            if current_time > shortest_time[current_location]:
                continue
            if current_location == target:
                break
            for neighbor, travel_time, road in self.graph[current_location]:
                new_time = current_time + travel_time
                if new_time < shortest_time[neighbor]:
                    shortest_time[neighbor] = new_time
                    previous[neighbor] = (current_location, road)
                    heappush(priority_queue, (new_time, neighbor))

        if shortest_time[target] == float("inf"):
            return None

        route: list[Road] = []
        location = target
        while True:
            entry = previous[location]
            if entry is None:
                break
            prev_location, road_used = entry
            route.append(road_used)
            location = prev_location
        route.reverse()
        return route

    def get_shortest_route(self, start: str, lair: str) -> list[Road] | None:
        return self._dijkstra(start, lair)

    def get_shortest_route_with_stop(self, start: str, pit_stop: str, lair: str) -> list[Road] | None:
        first_leg = self._dijkstra(start, pit_stop)
        if first_leg is None:
            return None
        second_leg = self._dijkstra(pit_stop, lair)
        if second_leg is None:
            return None
        return first_leg + second_leg