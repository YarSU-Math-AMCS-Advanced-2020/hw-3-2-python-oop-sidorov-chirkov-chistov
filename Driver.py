from Client import Client


class Driver(Client):
    def __init__(self, login, password, car):
        super().__init__(login, password)
        self.car = car
