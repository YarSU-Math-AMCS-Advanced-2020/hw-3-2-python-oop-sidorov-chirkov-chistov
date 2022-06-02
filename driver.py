from enum import Enum
from typing import List, Optional

import car
import offer
import trip
import user


class Status(Enum):
    OFFLINE = 0
    READY = 1
    ON_ROUTE = 2


class Driver(user.User):
    def __init__(self, login: str, password: str, __car: car.Car):
        super().__init__(login, password)
        self.car = __car
        self.status: Status = Status.OFFLINE
        self.__available_offers: List[offer.Offer] = []
        offer.OfferManager().add_observer(self)

    def update(self, offer_list: List[offer.Offer]):
        self.__available_offers = offer_list

    def handle_offer(self, offer_index: int) -> Optional[trip.Trip]:
        __offer = self.__available_offers[offer_index]
        if offer.OfferManager().find_offer_by_id(__offer.id) is not None:
            self.status = Status.ON_ROUTE
            offer.OfferManager().del_offer_by_id(__offer.id)
            __trip = trip.Trip(self, __offer)
            trip.TripManager().add_trip(__trip)
            return __trip
        return None

    def get_ready(self):
        if self.status != Status.ON_ROUTE:
            self.status = Status.READY

    def go_sleep(self):
        if self.status != Status.ON_ROUTE:
            self.status = Status.OFFLINE
