from abc import ABC, abstractmethod
from uuid import uuid4, UUID
from AbstractManager import Manager, singleton
import Driver
import Location
import decimal
import datetime
import Client


class Offer:
    # TODO: client wants to crate Offer just by destination point, new constructor is needed
    def __init__(self, client: Client, offer_time: datetime, departure_point: Location,
                 destination_point: Location, car_type, price: decimal):
        self.client_id = client.id
        self.offer_time = offer_time
        self.departure_point = departure_point
        self.destination_point = destination_point
        self.car_type = car_type
        self.price = price
        self.id = uuid4()


@singleton
class OfferManager:
    def __init__(self):
        self.offers: list[Offer] = []
        self.observers: list[Driver] = []

    def add_observer(self, d: Driver):
        if d not in self.observers:
            self.observers.append(d)

    def del_observer(self, d: Driver):
        if d in self.observers:
            self.observers.remove(d)

    def notify_observers(self, offer: Offer):
        max_dist = 100
        for o in self.observers:
            if Location.Traffic.distance(o.location, offer.departure_point) < max_dist \
                    and o.status == Driver.Status.ready:
                o.handle_offer(self, offer)

    def del_offer_by_id(self, id: UUID):
        return Manager.del_by_id(self.offers, id)

    def find_offer_by_id(self, id: UUID):
        return Manager.find_by_id(self.offers, id)

    def add_offer(self, offer: Offer):
        return Manager.add_element(self.offers, offer)


class OfferBuilder(ABC):
    pass
