from Client import Client


class Customer(Client):
    def __init__(self, login, password):
        super().__init__(login, password)
