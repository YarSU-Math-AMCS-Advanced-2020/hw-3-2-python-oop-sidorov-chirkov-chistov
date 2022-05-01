from Client import Client


class Customer(Client):
    def __init__(self, login: str, password: str):
        super().__init__(login, password)
