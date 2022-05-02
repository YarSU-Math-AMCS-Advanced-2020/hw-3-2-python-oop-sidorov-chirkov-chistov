import enum
from random import random
import Car
from Offer import Offer, OfferManager
from Client import Client
from Trip import TripManager, Trip


class Status(enum.Enum):
    offline = 0
    ready = 1
    on_route = 2


class Driver(Client):
    def __init__(self, login: str, password: str, car: Car):
        super().__init__(login, password)
        self.car = car
        self.status: Status = Status.offline

    def handle_offer(self, offer: Offer):
        if random() > 0.8:
            self.status = Status.on_route
            OfferManager().del_offer_by_id(offer.id)
            TripManager().add_trip(Trip(self, offer))

    def get_ready(self):
        if self.status != Status.on_route:
            self.status = Status.ready

    def go_sleep(self):
        if self.status != Status.on_route:
            self.status = Status.offline
