from abc import ABC, abstractmethod
from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from uuid import uuid4, UUID

from user import UserManager
from driver import Driver, Status
from manager import Manager, singleton
from map import Map
from offer import Offer
from report import Report, ReportManager


class Trip:
    def __init__(self, driver: Driver, offer: Offer):
        self.arrival_time = None
        self.departure_time = datetime.now()
        self.driver_id = driver.id
        self.driver_liked = False
        self.estimated_trip_time = Map().trip_time(offer.departure_point,
                                                   offer.destination_point)
        self.id = uuid4()
        self.passenger_id = offer.passenger_id
        self.passenger_liked = False
        self.payment_handler = offer.payment_handler
        self.price: Decimal = offer.price
        self.offer_id = offer.id
        self.state: ITripState = WaitingState()

    def next_state(self):
        self.state.next_state(self)

    def final_state(self):
        self.state.final_state(self)

    def driver_report(self, msg: str) -> Report:
        return Report(self.driver_id, msg, self)

    def passenger_report(self, msg: str) -> Report:
        return Report(self.passenger_id, msg, self)

    def like_driver(self):
        if not self.driver_liked:
            driver = UserManager().find_driver_by_id(self.driver_id)
            if driver is not None:
                driver.rating += 0.1

    def like_passenger(self):
        if not self.passenger_liked:
            passenger = UserManager().find_passenger_by_id(self.passenger_id)
            if passenger is not None:
                passenger.rating += 0.1


@singleton
class TripManager:
    def __init__(self):
        self.trips: List[Trip] = []

    def del_trip_by_id(self, _id: UUID) -> bool:
        return Manager.del_by_id(self.trips, _id)

    def find_trip_by_id(self, _id: UUID) -> Optional[Trip]:
        return Manager.find_by_id(self.trips, _id)

    def add_trip(self, trip: Trip) -> bool:
        return Manager.add_element(self.trips, trip)


class ITripState(ABC):
    @abstractmethod
    def next_state(self, trip: Trip):
        pass

    @abstractmethod
    def final_state(self, trip: Trip):
        pass


class WaitingState(ITripState):
    def __init__(self):
        self.wait_price = Decimal(10.5)

    def next_state(self, trip: Trip):
        passed_time = int((datetime.now() - trip.departure_time).total_seconds() / 60)
        trip.price += Decimal(self.wait_price * passed_time)
        trip.state = RidingState()

    def final_state(self, trip: Trip):
        passenger = UserManager().find_passenger_by_id(trip.passenger_id)
        if passenger is None:
            raise ValueError('Passenger should be valid')
        if trip.payment_handler.handle(
                trip.price) == 'Passenger have to pay by cash':
            ReportManager().add_report(trip.passenger_report('No payment'))
        trip.state = FinishedState()


class RidingState(ITripState):
    def next_state(self, trip: Trip):
        trip.arrival_time = datetime.now()
        trip.state = PaymentState()

    def final_state(self, trip: Trip):
        passenger = UserManager().find_passenger_by_id(trip.passenger_id)
        if passenger is None:
            raise ValueError('Passenger should be valid')
        trip.payment_handler.handle(trip.price)
        trip.state = FinishedState()


class PaymentState(ITripState):
    def next_state(self, trip: Trip):
        passenger = UserManager().find_passenger_by_id(trip.passenger_id)
        if passenger is None:
            raise ValueError('Passenger should be valid')
        print(trip.payment_handler.handle(trip.price))
        driver = UserManager().find_driver_by_id(trip.driver_id)
        if driver is None:
            raise ValueError('Driver should be valid')
        driver.status = Status.READY
        trip.state = FinishedState()

    def final_state(self, trip: Trip):
        self.next_state(trip)


class FinishedState(ITripState):
    def next_state(self, trip: Trip):
        pass

    def final_state(self, trip: Trip):
        pass
