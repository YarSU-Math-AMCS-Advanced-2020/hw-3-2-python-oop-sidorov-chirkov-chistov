import datetime
import os
import random
from AbstractManager import singleton


class Location:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


@singleton
class Map:
    def __init__(self):  # map: 0 - passable, -1 - impassable
        self.city_map = []
        if not os.path.exists('map.txt'):
            raise OSError("Fatal error: map-file doesnt exists")
        with open('map.txt', 'r') as file:
            lst = file.readlines()
        self.city_map = [[int(n) for n in x.split()] for x in lst]
        self.update_traffic()

    def __getitem__(self, item):
        return self.city_map[item]

    def update_traffic(self):
        for i in range(len(self.city_map)):
            for j in range(len(self.city_map[i])):
                if self.city_map[i][j] != -1:
                    self.city_map[i][j] = random.randint(0, 10)

    def find_way(self, a: Location, b: Location) -> list[Location]:
        pass
        # Dijkstra algorithm implementation

    def distance(self, a: Location, b: Location) -> int:
        return len(self.find_way(a, b))

    def trip_time(self, a: Location, b: Location) -> datetime.time:
        time = datetime.time(minute=0)
        way = self.find_way(a, b)
        for cell in way:
            time += datetime.timedelta(seconds=33) * int(self.city_map[cell.x][cell.y])
        return time
