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
