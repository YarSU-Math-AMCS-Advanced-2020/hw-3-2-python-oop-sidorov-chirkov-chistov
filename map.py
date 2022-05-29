from copy import copy
from datetime import time, timedelta
from manager import singleton
from os import path
from random import randint


class Location:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return int(str(hash(self.x)) + str(hash(self.y)))

    def __str__(self):
        return f"({self.x}, {self.y})"


@singleton
class Map:
    def __init__(self):  # map: 0 - can pass, -1 - can't pass
        self.city_map = []

        if not path.exists('map.txt'):
            raise OSError('Fatal error: map-file doesnt exists')
        with open('map.txt', 'r') as file:
            lst = file.readlines()

        self.city_map = [[int(cell) for cell in line.split()] for line in lst]
        self.update_traffic()

        # Limits of map
        self.min_x = 0
        self.max_x = len(self.city_map) - 1
        self.min_y = 0
        self.max_y = len(self.city_map[0]) - 1

    def __getitem__(self, item):
        return self.city_map[item]

    def update_traffic(self):
        for i in range(len(self.city_map)):
            for j in range(len(self.city_map[i])):
                if self.city_map[i][j] != -1:
                    self.city_map[i][j] = randint(0, 10)

    # Dijkstra implementation
    def find_way(self, a: Location, b: Location) -> list[Location]:
        inf = int(10 ** 10)
        distance = [[inf] * len(self.city_map[0]) for _ in
                    range(len(self.city_map))]
        distance[a.x][a.y] = 0
        parent = {a: Location(-1, -1)}
        s = {(distance[a.x][a.y], a)}

        # Utility func
        def update_vertex(xx, yy):
            if self.city_map[xx][yy] + dist < distance[xx][yy]:
                distance[xx][yy] = self.city_map[xx][yy] + dist
                s.add((distance[xx][yy], Location(xx, yy)))
                parent[Location(xx, yy)] = p

        while len(s) > 0:
            dist, p = s.pop()
            x, y = p.x, p.y

            if x >= 1 and self.city_map[x - 1][y] != -1:
                update_vertex(x - 1, y)
            if y >= 1 and self.city_map[x][y - 1] != -1:
                update_vertex(x, y - 1)
            if x < len(self.city_map) - 1 and self.city_map[x + 1][y] != -1:
                update_vertex(x + 1, y)
            if y < len(self.city_map[0]) - 1 and self.city_map[x][y + 1] != -1:
                update_vertex(x, y + 1)

        if distance[b.x][b.y] == 0:
            return []

        x = copy(b)
        result = [b]
        while parent[x] != Location(-1, -1):
            x = parent[x]
            result.append(x)
        result.reverse()
        return result

    def distance(self, a: Location, b: Location) -> int:
        return len(self.find_way(a, b))

    def trip_time(self, a: Location, b: Location) -> time:
        trip_time = time(second=0)
        way = self.find_way(a, b)
        for cell in way:
            trip_time += timedelta(seconds=33) * self.city_map[cell.x][cell.y]
        return trip_time
