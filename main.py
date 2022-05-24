from map import Location, Map
m = Map()
a = Location(0, 0)
b = Location(1, 2)
lst = m.find_way(a, b)
for el in lst:
    print(el)
