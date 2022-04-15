import AbstractManager
import Location
import decimal
import datetime
import Client


class OfferInfo:
    def __init__(self, client: Client, offer_time: datetime, departure_point: Location,
                 destination_point: Location, car_type, price: decimal):
        # TODO: I want to get client and driver by id, please, realize this in Driver/ClientManager
        self.client_id = id(client)

        self.offer_time = offer_time
        self.departure_point = departure_point
        self.destination_point = destination_point
        self.car_type = car_type
        self.price = price


class Offer:
    def __init__(self, offer_info: OfferInfo):
        self.offer_info = offer_info
        self.id = id(offer_info)


class OfferManager(AbstractManager.Manager):
    def __init__(self):
        self.offers: list[Offer] = []

    def del_offer_by_id(self, id: int):
        return self.del_by_id(self.offers, id)

    def find_offer_by_id(self, id: int):
        return self.find_by_id(self.offers, id)

    def add_offer(self, offer: Offer):
        return self.add_element(self.offers, offer)
