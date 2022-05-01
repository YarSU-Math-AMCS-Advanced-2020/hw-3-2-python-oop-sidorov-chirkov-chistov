from random import randint
from uuid import uuid4
from Location import Location


class Client:
    # TODO: ClientManager to check for the same logins
    # TODO: add rating system, rating changes due to trip ends or conflicts
    def __init__(self, login: str, password: str):
        self.login = login
        self.password = password
        # TODO: set random location depending on map (depends on map size and dont set a car on impassable place)
        self.location = Location(randint(0, 200), randint(0, 200))
        self.rating = 0.0
        self.id = uuid4()
