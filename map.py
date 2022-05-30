from copy import copy
from dataclasses import dataclass
from datetime import time, timedelta
from typing import List

from manager import singleton
from os import path
from random import randint


@dataclass
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
            raise OSError("Fatal error: map-file doesn't exist")
        with open('map.txt', 'r') as file:
            lst = file.readlines()

        self.city_map: List[List[int]] = \
            [[int(cell) for cell in line.split()] for line in lst]
        self.update_traffic()

        # Limits of map
        self.min_x = 0
        self.max_x = len(self.city_map) - 1
        self.min_y = 0
        self.max_y = len(self.city_map[0]) - 1

        self.min_traffic = 0
        self.max_traffic = 10

    def __getitem__(self, item: int):
        return self.city_map[item]

    def update_traffic(self):
        for i in range(len(self.city_map)):
            for j in range(len(self.city_map[i])):
                if self.city_map[i][j] != -1:
                    self.city_map[i][j] = randint(self.min_traffic, self.max_traffic)

    # Dijkstra implementation
    def find_way(self, start: Location, end: Location) -> list[Location]:
        inf = int(10 ** 10)
        bad_location = Location(-1, -1)

        distance = [[inf] * len(self.city_map[0]) for _ in
                    range(len(self.city_map))]
        distance[start.x][start.y] = 0
        parent = {start: bad_location}
        s = {(distance[start.x][start.y], start)}

        # Utility func
        def update_vertex(xx: int, yy: int) -> None:
            if self.city_map[xx][yy] + dist < distance[xx][yy]:
                distance[xx][yy] = self.city_map[xx][yy] + dist
                s.add((distance[xx][yy], Location(xx, yy)))
                parent[Location(xx, yy)] = point

        while len(s) > 0:
            dist, point = s.pop()
            x, y = point.x, point.y

            if x >= 1 and self.city_map[x - 1][y] != -1:
                update_vertex(x - 1, y)
            if y >= 1 and self.city_map[x][y - 1] != -1:
                update_vertex(x, y - 1)
            if x < len(self.city_map) - 1 and self.city_map[x + 1][y] != -1:
                update_vertex(x + 1, y)
            if y < len(self.city_map[0]) - 1 and self.city_map[x][y + 1] != -1:
                update_vertex(x, y + 1)

        if distance[end.x][end.y] == 0:
            return []

        current_point = copy(end)
        result = [current_point]
        while parent[current_point] != bad_location:
            current_point = parent[current_point]
            result.append(current_point)
        result.reverse()
        return result

    def distance(self, start: Location, end: Location) -> int:
        return len(self.find_way(start, end))

    def trip_time(self, start: Location,
                  end: Location,
                  seconds_per_traffic_unit: int = 33) -> time:
        trip_time = time(second=0)
        way = self.find_way(start, end)
        for cell in way:
            trip_time += timedelta(seconds=seconds_per_traffic_unit) * \
                         self.city_map[cell.x][cell.y]
        return trip_time
