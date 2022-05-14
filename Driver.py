import enum

import Car
from Offer import Offer, OfferManager
from Client import Client
from Trip import TripManager, Trip


class Status(enum.Enum):
    OFFLINE = 0
    READY = 1
    ON_ROUTE = 2


class Driver(Client):
    def __init__(self, login: str, password: str, car: Car):
        super().__init__(login, password)
        self.car = car
        self.status: Status = Status.OFFLINE
        self.__enable_offers: list[Offer] = []
        OfferManager().add_observer(self)

    def update(self, offer_list: list[Offer]):
        self.__enable_offers = offer_list

    def handle_offer(self, offer_index: int) -> bool:
        offer = self.__enable_offers[offer_index]
        if OfferManager().find_offer_by_id(offer.id) is not None:
            self.status = Status.ON_ROUTE
            OfferManager().del_offer_by_id(offer.id)
            TripManager().add_trip(Trip(self, offer))
            return True
        return False

    def get_ready(self):
        if self.status != Status.ON_ROUTE:
            self.status = Status.READY

    def go_sleep(self):
        if self.status != Status.ON_ROUTE:
            self.status = Status.OFFLINE
