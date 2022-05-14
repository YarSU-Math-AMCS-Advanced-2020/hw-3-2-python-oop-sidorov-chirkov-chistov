from abc import ABC, abstractmethod
from uuid import uuid4, UUID
from AbstractManager import Manager, singleton
import Driver
from Map import Location, Map
from decimal import Decimal
from datetime import datetime
import Client
from Client import ClientManager
from Car import Car, CarType


class Offer:
    # TODO: client wants to crate Offer just by destination point, new constructor is needed
    def __init__(self, client: Client, offer_time: datetime, departure_point: Location,
                 destination_point: Location, car_type, price: Decimal):
        self.client_id = client.id
        self.offer_time = offer_time
        self.departure_point = departure_point
        self.destination_point = destination_point
        self.car_type = car_type
        self.price = price
        self.id = uuid4()

    def __init__(self):
        pass


@singleton
class OfferManager:
    def __init__(self):
        self.offers: list[Offer] = []
        self.observers: list[Driver] = []

    def add_observer(self, d: Driver):
        return Manager.add_element(self.observers, d)

    def del_observer(self, d: Driver):
        return Manager.del_by_id(self.observers, d.id)

    def notify_observers(self):
        max_dist = 100
        for dr in self.observers:
            enable_offers: list[Offer] = []
            for offer in self.offer:
                if Map.distance(dr.location, offer.departure_point) < max_dist \
                        and dr.status == Driver.Status.ready:
                    enable_offers.append(offer)
            dr.update(self, enable_offers)

    def del_offer_by_id(self, id: UUID) -> bool:
        return Manager.del_by_id(self.offers, id)

    def find_offer_by_id(self, id: UUID) -> Offer:
        return Manager.find_by_id(self.offers, id)

    def add_offer(self, offer: Offer) -> bool:
        return Manager.add_element(self.offers, offer)


class OfferBuilder(ABC):
    def __init__(self):
        self.offer = Offer()

    def reset(self):
        self.offer = Offer()

    def add_client(self, client: Client):
        self.offer.client_id = client.id

    def add_offer_time(self):
        self.offer.offer_time = datetime.now()

    def add_departure_point(self):
        client = ClientManager().find_client_by_id(self.offer.client_id)
        # Если был задан невалидный клиент
        if client is None:
            self.reset()
        self.offer.departure_point = client.location

    def add_destination_point(self, destination: Location):
        self.offer.departure_point = destination

    def add_car_type(self, car_info=CarType.economy):
        if car_info is Car:
            self.offer.car_type = car_info.car_type
        elif car_info is CarType:
            self.offer.car_type = car_info
        else:
            self.reset()

    @abstractmethod
    def add_price(self):
        pass

    def return_offer(self) -> Offer | None:
        # Если цена не None, то объект был полностью создан
        return self.offer if (self.offer.price is not None) else None


# Константная цена за проезд по клетке
class DefaultOfferBuilder(OfferBuilder, ABC):
    def __init__(self, const_price: Decimal = 1.0):
        super(OfferBuilder).__init__()
        self.const_price = const_price

    def add_price(self):
        self.offer.price = self.const_price * Map.distance(self.offer.departure_point, self.offer.destination_point)


# Цена с учетом трафика в текущий момент времени
class TrafficSensitiveOfferBuilder(OfferBuilder, ABC):
    def __init__(self, traffic_coefficient: Decimal = 1.0):
        super(OfferBuilder).__init__()
        self.traffic_coefficient = traffic_coefficient

    def add_price(self):
        price = Decimal(0)
        way = Map.find_way(self.offer.departure_point, self.offer.destination_point)
        for cell in way:
            # TODO: Я бы хотел, чтобы Traffic был singleton, и не получал аргументов на вход - хочется хранить карту тоже отдельно
            price += Map[cell.y][cell.x] * self.traffic_coefficient
        self.offer.price = price


# Цена только с учетом времени поездки (может вычисляться нетривиально)
class TimeSensitiveOfferBuilder(OfferBuilder, ABC):
    def __init__(self, cost_per_minute: Decimal = 1.0):
        super(OfferBuilder).__init__()
        self.cost_per_minute = cost_per_minute

    def add_price(self):
        price = Map.trip_time(self.offer.departure_point,
                                self.offer.destination_point).minute * self.cost_per_minute
        self.offer.price = price


@singleton
class OfferDirector:
    @staticmethod
    def make_offer_with_car(self, client: Client, car: Car, destination: Location,
                            builder: OfferBuilder = DefaultOfferBuilder()) -> Offer | None:
        builder.add_client(client)
        builder.add_offer_time()
        builder.add_departure_point()
        builder.add_destination_point(destination)
        builder.add_car_type(car.car_type)
        builder.add_price()
        return builder.offer

    @staticmethod
    def make_offer_without_car(self, client: Client, destination: Location,
                               builder: OfferBuilder = DefaultOfferBuilder()) -> Offer | None:
        builder.add_client(client)
        builder.add_offer_time()
        builder.add_departure_point()
        builder.add_destination_point(destination)
        builder.add_car_type()
        builder.add_price()
        return builder.offer
