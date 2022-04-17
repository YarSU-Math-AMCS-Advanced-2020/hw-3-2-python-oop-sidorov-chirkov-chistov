from uuid import uuid4
import AbstractManager
import Driver
import Location
import decimal
import datetime
import Client
from Trip import TripManager


class OfferInfo:
    # TODO: client wants to crate Offer just by destination point, new constructor is needed
    def __init__(self, client: Client, offer_time: datetime, departure_point: Location,
                 destination_point: Location, car_type, price: decimal):
        self.client_id = client.id
        self.offer_time = offer_time
        self.departure_point = departure_point
        self.destination_point = destination_point
        self.car_type = car_type
        self.price = price


class Offer:
    def __init__(self, offer_info: OfferInfo):
        self.offer_info = offer_info
        self.id = uuid4()


class OfferManager(AbstractManager.Manager):
    # TODO: offer manager knows about trip manager - that`s bad
    def __init__(self, trip_manager: TripManager):
        self.trip_manager = trip_manager
        self.offers: list[Offer] = []
        self.observers: list[Driver] = []

    def add_observer(self, d: Driver):
        self.observers.append(d)

    def del_observer(self, d: Driver):
        self.observers.remove(d)

    def notify_observers(self, offer: Offer):
        max_dist = 100
        for o in self.observers:
            if Location.Traffic.distance(o.location, offer.offer_info.departure_point) < max_dist \
                    and o.status == Driver.Status.ready:
                o.handle_offer(self, self.trip_manager, offer)

    def del_offer_by_id(self, id: int):
        return self.del_by_id(self.offers, id)

    def find_offer_by_id(self, id: int):
        return self.find_by_id(self.offers, id)

    def add_offer(self, offer: Offer):
        return self.add_element(self.offers, offer)
