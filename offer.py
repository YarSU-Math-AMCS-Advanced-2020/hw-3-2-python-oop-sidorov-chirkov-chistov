from abc import ABC, abstractmethod
from uuid import uuid4, UUID
from decimal import Decimal
from datetime import datetime

from manager import Manager, singleton
from driver import Driver
from map import Location, Map
from client import ClientManager
from customer import Customer
from car import Car, CarType
from dataclasses import dataclass


@dataclass
class Offer:
    def __init__(self, customer: Customer, offer_time: datetime, departure_point: Location,
                 destination_point: Location, car_type, price: Decimal):
        self.customer_id = customer.id
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

    def add_observer(self, driver: Driver):
        return Manager.add_element(self.observers, driver)

    def del_observer(self, driver: Driver):
        return Manager.del_by_id(self.observers, driver.id)

    def notify_observers(self):
        max_dist = 100
        for driver in self.observers:
            enable_offers: list[Offer] = []
            for offer in self.offer:
                if Map().distance(driver.location, offer.departure_point) < max_dist \
                        and driver.status == driver.status.READY:
                    enable_offers.append(offer)
            driver.update(enable_offers)

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

    def add_customer(self, customer: Customer):
        self.offer.customer_id = customer.id

    def add_offer_time(self):
        self.offer.offer_time = datetime.now()

    def add_departure_point(self):
        customer = ClientManager().find_client_by_id(self.offer.customer_id)
        # Если был задан невалидный клиент
        if customer is None:
            raise ValueError('Customer should be valid!')
        self.offer.departure_point = customer.location

    def add_destination_point(self, destination: Location):
        self.offer.departure_point = destination

    def add_car_type(self, car_info: Car | CarType = CarType.ECONOMY):
        if car_info is Car:
            self.offer.car_type = car_info.car_type
        elif car_info is CarType:
            self.offer.car_type = car_info
        else:
            raise TypeError('CarInfo should be of type Car or CarInfo!')

    @abstractmethod
    def add_price(self):
        pass

    def create_offer(self) -> Offer | None:
        # Если цена не None, то объект был полностью создан
        return self.offer if (self.offer.price is not None) else None


# Константная цена за проезд по клетке
class DefaultOfferBuilder(OfferBuilder, ABC):
    def __init__(self, const_price: Decimal = 1.0):
        super(OfferBuilder).__init__()
        self.const_price = const_price

    def add_price(self):
        self.offer.price = self.const_price * Map().distance(self.offer.departure_point, self.offer.destination_point)


# Цена с учетом трафика в текущий момент времени
class TrafficSensitiveOfferBuilder(OfferBuilder, ABC):
    def __init__(self, traffic_coefficient: Decimal = 1.0):
        super(OfferBuilder).__init__()
        self.traffic_coefficient = traffic_coefficient

    def add_price(self):
        price = Decimal(0)
        way = Map().find_way(self.offer.departure_point, self.offer.destination_point)
        for cell in way:
            price += Map[cell.y][cell.x] * self.traffic_coefficient
        self.offer.price = price


# Цена только с учетом времени поездки (может вычисляться нетривиально)
class TimeSensitiveOfferBuilder(OfferBuilder, ABC):
    def __init__(self, cost_per_minute: Decimal = 1.0):
        super(OfferBuilder).__init__()
        self.cost_per_minute = cost_per_minute

    def add_price(self):
        price = Map().trip_time(self.offer.departure_point,
                                self.offer.destination_point).minute * self.cost_per_minute
        self.offer.price = price


@singleton
class OfferDirector:
    @staticmethod
    def make_offer_with_car(customer: Customer, car: Car, destination: Location,
                            builder: OfferBuilder = DefaultOfferBuilder()) -> Offer | None:
        builder.add_customer(customer)
        builder.add_offer_time()
        builder.add_departure_point()
        builder.add_destination_point(destination)
        builder.add_car_type(car.car_type)
        builder.add_price()
        return builder.create_offer()

    @staticmethod
    def make_offer_without_car(customer: Customer, destination: Location,
                               builder: OfferBuilder = DefaultOfferBuilder()) -> Offer | None:
        builder.add_customer(customer)
        builder.add_offer_time()
        builder.add_departure_point()
        builder.add_destination_point(destination)
        builder.add_car_type()
        builder.add_price()
        return builder.create_offer()
