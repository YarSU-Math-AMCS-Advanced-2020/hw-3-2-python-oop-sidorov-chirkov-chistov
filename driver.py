import enum
from typing import List

from car import Car
from user import User
from offer import Offer, OfferManager
from trip import TripManager, Trip


class Status(enum.Enum):
    OFFLINE = 0
    READY = 1
    ON_ROUTE = 2


class Driver(User):
    def __init__(self, login: str, password: str, car: Car):
        super().__init__(login, password)
        self.car = car
        self.status: Status = Status.OFFLINE
        self.__enable_offers: List[Offer] = []
        OfferManager().add_observer(self)

    def update(self, offer_list: List[Offer]):
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
