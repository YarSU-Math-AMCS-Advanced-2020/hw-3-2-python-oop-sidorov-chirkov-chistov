import enum
from typing import List, Optional

from car import Car
from offer import Offer, OfferManager
from trip import TripManager, Trip
from user import User


class Status(enum.Enum):
    OFFLINE = 0
    READY = 1
    ON_ROUTE = 2


class Driver(User):
    def __init__(self, login: str, password: str, car: Car):
        super().__init__(login, password)
        self.car = car
        self.status: Status = Status.OFFLINE
        self.__available_offers: List[Offer] = []
        OfferManager().add_observer(self)

    def update(self, offer_list: List[Offer]):
        self.__available_offers = offer_list

    def handle_offer(self, offer_index: int) -> Optional[Trip]:
        offer = self.__available_offers[offer_index]
        if OfferManager().find_offer_by_id(offer.id) is not None:
            self.status = Status.ON_ROUTE
            OfferManager().del_offer_by_id(offer.id)
            trip = Trip(self, offer)
            TripManager().add_trip(trip)
            return trip
        return None

    def get_ready(self):
        if self.status != Status.ON_ROUTE:
            self.status = Status.READY

    def go_sleep(self):
        if self.status != Status.ON_ROUTE:
            self.status = Status.OFFLINE
