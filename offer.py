from abc import ABC, abstractmethod
from datetime import datetime
from decimal import Decimal
from typing import List
from uuid import uuid4, UUID

from car import Car, CarType
from payment import PaymentHandler, PaymentHandlerType, create_handler, CashPayHandler
from user import UserManager
from passenger import Passenger
from dataclasses import dataclass
from driver import Driver
from manager import Manager, singleton
from map import Location, Map


@dataclass
class Offer:
    car_type: CarType = CarType.ECONOMY
    departure_point: Location = Location(0, 0)
    destination_point: Location = Location(0, 0)
    offer_time: datetime = datetime(year=0, month=0, day=0)
    passenger: Passenger = Passenger('admin', 'password')
    payment_handler: PaymentHandler = CashPayHandler(passenger)
    price: Decimal = Decimal(0.0)

    def __post_init__(self):
        self.id = uuid4()
        self.passenger_id = self.passenger.id


@singleton
class OfferManager:
    def __init__(self):
        self.offers: List[Offer] = []
        self.observers: List[Driver] = []

    def add_observer(self, driver: Driver):
        return Manager.add_element(self.observers, driver)

    def del_observer(self, driver: Driver):
        return Manager.del_by_id(self.observers, driver.id)

    def notify_observers(self, max_dist: float = 100):
        for driver in self.observers:
            enable_offers: List[Offer] = []
            for offer in self.offers:
                if Map().distance(driver.location, offer.departure_point) < max_dist and \
                        driver.status == driver.status.READY:
                    enable_offers.append(offer)
            driver.update(enable_offers)

    def del_offer_by_id(self, _id: UUID) -> bool:
        return Manager.del_by_id(self.offers, _id)

    def find_offer_by_id(self, _id: UUID) -> Offer | None:
        return Manager.find_by_id(self.offers, _id)

    def add_offer(self, offer: Offer) -> bool:
        return Manager.add_element(self.offers, offer)


class OfferBuilder(ABC):
    def __init__(self):
        self.offer = Offer()

    def add_car_type(self, car_info: Car | CarType = CarType.ECONOMY):
        if isinstance(car_info, Car):
            self.offer.car_type = car_info.car_type
        elif isinstance(car_info, CarType):
            self.offer.car_type = car_info
        else:
            raise TypeError('CarInfo should be of type Car or CarInfo!')

    def add_departure_point(self):
        passenger = UserManager().find_passenger_by_id(self.offer.passenger_id)
        # If passenger is not valid
        if passenger is None:
            raise ValueError('passenger should be valid!')
        self.offer.departure_point = passenger.location

    def add_destination_point(self, destination: Location):
        self.offer.departure_point = destination

    def add_offer_time(self):
        self.offer.offer_time = datetime.now()

    def add_passenger(self, passenger: Passenger):
        self.offer.passenger_id = passenger.id

    def add_payment_process(self,
                            payment_handler_type: PaymentHandlerType =
                            PaymentHandlerType.CashPayHandler):
        passenger = UserManager().find_passenger_by_id(self.offer.passenger_id)
        if passenger is None:
            raise ValueError('Passenger should be valid')
        self.offer.payment_handler = create_handler(passenger, payment_handler_type)

    @abstractmethod
    def add_price(self):
        pass

    def create_offer(self) -> Offer | None:
        # If price is not None, then object was completely created
        return self.offer if (self.offer.price is not None) else None

    def reset(self):
        self.offer = Offer()


# Const price per cell
class DefaultOfferBuilder(OfferBuilder):
    def __init__(self, const_price: Decimal = Decimal(1.0)):
        super().__init__()
        self.const_price = const_price

    def add_price(self):
        dist = Map().distance(self.offer.departure_point, self.offer.destination_point)
        self.offer.price = self.const_price * dist


# Price according to traffic at the current time
class TrafficSensitiveOfferBuilder(OfferBuilder):
    def __init__(self, traffic_coefficient: Decimal = Decimal(1.0)):
        super().__init__()
        self.traffic_coefficient = traffic_coefficient

    def add_price(self):
        price = Decimal(0)
        way = Map().find_way(self.offer.departure_point,
                             self.offer.destination_point)
        for cell in way:
            price += Map[cell.y][cell.x] * self.traffic_coefficient
        self.offer.price = price


# Price according to time of the trip (can be calculated non-trivially)
class TimeSensitiveOfferBuilder(OfferBuilder):
    def __init__(self, cost_per_minute: Decimal = Decimal(1.0)):
        super().__init__()
        self.cost_per_minute = cost_per_minute

    def add_price(self):
        time = Map().trip_time(self.offer.departure_point, self.offer.destination_point)
        self.offer.price = time.minute * self.cost_per_minute


@singleton
class OfferDirector:
    @staticmethod
    def make_offer_with_car(passenger: Passenger,
                            car: Car,
                            destination: Location,
                            builder: OfferBuilder =
                            DefaultOfferBuilder()) -> Offer | None:
        builder.add_car_type(car.car_type)
        builder.add_departure_point()
        builder.add_destination_point(destination)
        builder.add_offer_time()
        builder.add_passenger(passenger)
        builder.add_payment_process()
        builder.add_price()
        return builder.create_offer()

    @staticmethod
    def make_offer_without_car(passenger: Passenger,
                               destination: Location,
                               builder: OfferBuilder =
                               DefaultOfferBuilder()) -> Offer | None:
        builder.add_car_type()
        builder.add_departure_point()
        builder.add_destination_point(destination)
        builder.add_offer_time()
        builder.add_passenger(passenger)
        builder.add_payment_process()
        builder.add_price()
        return builder.create_offer()

    @staticmethod
    def make_offer_with_car_with_applepay(passenger: Passenger, car: Car,
                                          destination: Location,
                                          builder: OfferBuilder =
                                          DefaultOfferBuilder()) -> Offer | None:
        builder.add_car_type(car.car_type)
        builder.add_departure_point()
        builder.add_destination_point(destination)
        builder.add_offer_time()
        builder.add_passenger(passenger)
        builder.add_payment_process(PaymentHandlerType.ApplePayHandler)
        builder.add_price()
        return builder.create_offer()

    @staticmethod
    def make_offer_without_car_with_applepay(passenger: Passenger,
                                             destination: Location,
                                             builder: OfferBuilder =
                                             DefaultOfferBuilder()) -> Offer | None:
        builder.add_car_type()
        builder.add_departure_point()
        builder.add_destination_point(destination)
        builder.add_offer_time()
        builder.add_passenger(passenger)
        builder.add_payment_process(PaymentHandlerType.ApplePayHandler)
        builder.add_price()
        return builder.create_offer()
