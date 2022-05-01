import datetime
import random


class Location:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class Traffic:
    def __init__(self, city_map: list[list[int]]):  # map: 0 - passable, -1 - impassable
        self.city_map = city_map
        for i in range(0, len(city_map)):
            for j in range(0, len(city_map)):
                city_map[i][j] = random.randint(0, 10)

    @staticmethod
    def find_way(a: Location, b: Location):
        # TODO: return an array of cells you need to visit in right order
        # (using bfs or better Dijkstra (consider traffic in each cell))
        return list[Location]

    @staticmethod
    def distance(a: Location, b: Location):
        return len(Traffic.find_way(a, b))

    @staticmethod
    def trip_time(a: Location, b: Location):
        # TODO: find the time just by calculating some kind of formula including traffic in each cell
        return datetime.time(hour=1)
