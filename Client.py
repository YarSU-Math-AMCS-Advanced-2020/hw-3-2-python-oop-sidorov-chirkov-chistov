from decimal import Decimal
from random import randint
from uuid import uuid4, UUID
from AbstractManager import Manager, singleton
from Map import Location


class Client:
    def __init__(self, login: str, password: str):
        if type(login) != str:
            raise TypeError("Login should be string, got " + str(type(login)))
        if not login[0].isalpha() or not login.isalnum():
            raise ValueError("Login should consist of letters and digits, first symbol is letter")
        self.login = login
        self.password = password
        # TODO: set random location depending on map (depends on map size and dont set a car on impassable place)
        self.location = Location(randint(0, 200), randint(0, 200))
        self.__rating: float = 8.5  # from 0.0 to 10.0
        self.id = uuid4()
        self.google_pay_balance: Decimal = Decimal(0.0)
        self.apple_pay_balance: Decimal = Decimal(0.0)
        self.bank_card_balance: Decimal = Decimal(0.0)

    @property
    def rating(self):
        return self.__rating

    @rating.setter
    def rating(self, value: float):
        self.__rating = value
        if self.__rating > 10.0:
            self.__rating = 10.0
        if self.__rating < 0.0:
            self.__rating = 0.0

    def __str__(self):
        return f"{self.login}"


@singleton
class ClientManager:
    def __init__(self):
        self.clients: list[Client] = []

    def del_client_by_id(self, id: UUID) -> bool:
        return Manager.del_by_id(self.clients, id)

    def find_client_by_id(self, id: UUID) -> Client | None:
        return Manager.find_by_id(self.clients, id)

    def add_client(self, client: Client) -> bool:
        for cl in self.clients:
            if cl.login == client.login:
                raise ValueError("Login is already used by another user")
        return Manager.add_element(self.clients, client)
