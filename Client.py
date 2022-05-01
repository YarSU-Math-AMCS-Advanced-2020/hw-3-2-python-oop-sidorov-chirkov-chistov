from random import randint
from uuid import uuid4
import AbstractManager
from Location import Location


class Client:
    # TODO: add rating system, rating changes due to trip ends or conflicts
    def __init__(self, login: str, password: str):
        if type(login) != str:
            raise TypeError("Login should be string, got " + str(type(login)))
        if not login[0].isalpha() or not login.isalnum():
            raise ValueError("Login should consist of letters and digits, first symbol is letter")
        self.login = login
        self.password = password
        # TODO: set random location depending on map (depends on map size and dont set a car on impassable place)
        self.location = Location(randint(0, 200), randint(0, 200))
        self.rating: float = 0.0  # from 0.0 to 5.0
        self.id = uuid4()


class ClientManager(AbstractManager.Manager):
    def __init__(self):
        self.clients: list[Client] = []

    def del_client_by_id(self, id: int):
        return self.del_by_id(self.clients, id)

    def find_client_by_id(self, id: int):
        return self.find_by_id(self.clients, id)

    def add_client(self, client: Client):
        for cl in self.clients:
            if cl.login == client.login:
                raise ValueError("Login is already used by another user")
        return self.add_element(self.clients, client)
