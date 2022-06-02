from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import List, Optional, Union
from uuid import uuid4, UUID

import car
import driver
import manager
import map
import passenger
import payment
import user


@dataclass
class Offer:
    __car_type: car.CarType = car.CarType.ECONOMY
    departure_point: map.Location = map.Location(0, 0)
    destination_point: map.Location = map.Location(0, 0)
    offer_time: datetime = datetime(year=1, month=1, day=1)
    __passenger: passenger.Passenger = passenger.Passenger('admin', 'password')
    payment_handler: payment.PaymentHandler = payment.CashPayHandler(__passenger)
    price: Decimal = Decimal(0.0)

    def __post_init__(self):
        self.id = uuid4()
        self.passenger_id = self.__passenger.id


@manager.singleton
class OfferManager:
    def __init__(self):
        self.offers: List[Offer] = []
        self.observers: List[driver.Driver] = []

    def add_observer(self, __driver: driver.Driver):
        return manager.Manager.add_element(self.observers, __driver)

    def del_observer(self, __driver: driver.Driver):
        return manager.Manager.del_by_id(self.observers, __driver.id)

    def notify_observers(self, max_dist: float = 100):
        for __driver in self.observers:
            available_offers: List[Offer] = []
            for offer in self.offers:
                if map.Map().distance(__driver.location, offer.departure_point) < max_dist and \
                        __driver.status == __driver.status.READY:
                    available_offers.append(offer)
            __driver.update(available_offers)

    def del_offer_by_id(self, _id: UUID) -> bool:
        return manager.Manager.del_by_id(self.offers, _id)

    def find_offer_by_id(self, _id: UUID) -> Optional[Offer]:
        return manager.Manager.find_by_id(self.offers, _id)

    def add_offer(self, offer: Offer) -> bool:
        return manager.Manager.add_element(self.offers, offer)


class OfferBuilder(ABC):
    def __init__(self):
        self.offer = Offer()

    def add_car_type(self, car_info: Union[car.Car, car.CarType] = car.CarType.ECONOMY):
        if isinstance(car_info, car.Car):
            self.offer.car_type = car_info.car_type
        elif isinstance(car_info, car.CarType):
            self.offer.car_type = car_info
        else:
            raise TypeError('CarInfo should be of type Car or CarInfo!')

    def add_departure_point(self):
        __passenger = user.UserManager().find_passenger_by_id(self.offer.passenger_id)
        # If passenger is not valid
        if __passenger is None:
            raise ValueError('passenger should be valid!')
        self.offer.departure_point = __passenger.location

    def add_destination_point(self, destination: map.Location):
        self.offer.departure_point = destination

    def add_offer_time(self):
        self.offer.offer_time = datetime.now()

    def add_passenger(self, __passenger: passenger.Passenger):
        self.offer.passenger_id = __passenger.id

    def add_payment_process(self,
                            payment_handler_type: payment.PaymentHandlerType =
                            payment.PaymentHandlerType.CashPayHandler):
        __passenger = user.UserManager().find_passenger_by_id(self.offer.passenger_id)
        if __passenger is None:
            raise ValueError('Passenger should be valid')
        self.offer.payment_handler = payment.create_handler(__passenger, payment_handler_type)

    @abstractmethod
    def add_price(self):
        pass

    def create_offer(self) -> Optional[Offer]:
        # If price is not None, then object was completely created
        return self.offer if (self.offer.price != Decimal(0.0)) else None

    def reset(self):
        self.offer = Offer()


# Const price per cell
class DefaultOfferBuilder(OfferBuilder):
    def __init__(self, const_price: Decimal = Decimal(1.0)):
        super().__init__()
        self.const_price = const_price

    def add_price(self):
        dist = map.Map().distance(self.offer.departure_point, self.offer.destination_point)
        self.offer.price = self.const_price * dist


# Price according to traffic at the current time
class TrafficSensitiveOfferBuilder(OfferBuilder):
    def __init__(self, traffic_coefficient: Decimal = Decimal(1.0)):
        super().__init__()
        self.traffic_coefficient = traffic_coefficient

    def add_price(self):
        price = Decimal(0)
        way = map.Map().find_way(self.offer.departure_point,
                                 self.offer.destination_point)
        for cell in way:
            price += map.Map[cell.y][cell.x] * self.traffic_coefficient
        self.offer.price = price


# Price according to time of the trip (can be calculated non-trivially)
class TimeSensitiveOfferBuilder(OfferBuilder):
    def __init__(self, cost_per_minute: Decimal = Decimal(1.0)):
        super().__init__()
        self.cost_per_minute = cost_per_minute

    def add_price(self):
        time = map.Map().trip_time(self.offer.departure_point, self.offer.destination_point)
        self.offer.price = time.minute * self.cost_per_minute


@manager.singleton
class OfferDirector:
    @staticmethod
    def make_offer_with_car(__passenger: passenger.Passenger,
                            __car: car.Car,
                            destination: map.Location,
                            builder: OfferBuilder =
                            DefaultOfferBuilder()) -> Optional[Offer]:
        builder.add_car_type(__car.car_type)
        builder.add_departure_point()
        builder.add_destination_point(destination)
        builder.add_offer_time()
        builder.add_passenger(__passenger)
        builder.add_payment_process()
        builder.add_price()
        return builder.create_offer()

    @staticmethod
    def make_offer_without_car(__passenger: passenger.Passenger,
                               destination: map.Location,
                               builder: OfferBuilder =
                               DefaultOfferBuilder()) -> Optional[Offer]:
        builder.add_car_type()
        builder.add_departure_point()
        builder.add_destination_point(destination)
        builder.add_offer_time()
        builder.add_passenger(__passenger)
        builder.add_payment_process()
        builder.add_price()
        return builder.create_offer()

    @staticmethod
    def make_offer_with_car_with_applepay(__passenger: passenger.Passenger, __car: car.Car,
                                          destination: map.Location,
                                          builder: OfferBuilder =
                                          DefaultOfferBuilder()) -> Optional[Offer]:
        builder.add_car_type(__car.car_type)
        builder.add_departure_point()
        builder.add_destination_point(destination)
        builder.add_offer_time()
        builder.add_passenger(__passenger)
        builder.add_payment_process(payment.PaymentHandlerType.ApplePayHandler)
        builder.add_price()
        return builder.create_offer()

    @staticmethod
    def make_offer_without_car_with_applepay(__passenger: passenger.Passenger,
                                             destination: map.Location,
                                             builder: OfferBuilder =
                                             DefaultOfferBuilder()) -> Optional[Offer]:
        builder.add_car_type()
        builder.add_departure_point()
        builder.add_destination_point(destination)
        builder.add_offer_time()
        builder.add_passenger(__passenger)
        builder.add_payment_process(payment.PaymentHandlerType.ApplePayHandler)
        builder.add_price()
        return builder.create_offer()
