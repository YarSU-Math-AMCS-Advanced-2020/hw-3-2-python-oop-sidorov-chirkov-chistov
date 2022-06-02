from abc import ABC, abstractmethod
from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from uuid import uuid4, UUID

import driver
import manager
import map
import offer
import report
import user


class Trip:
    def __init__(self, __driver: driver.Driver, __offer: offer.Offer):
        self.arrival_time = None
        self.departure_time = datetime.now()
        self.driver_id = __driver.id
        self.driver_liked = False
        self.estimated_trip_time = map.Map().trip_time(__offer.departure_point,
                                                       __offer.destination_point)
        self.id = uuid4()
        self.passenger_id = __offer.passenger_id
        self.passenger_liked = False
        self.payment_handler = __offer.payment_handler
        self.price: Decimal = __offer.price
        self.offer_id = __offer.id
        self.state: ITripState = WaitingState()

    def next_state(self):
        self.state.next_state(self)

    def final_state(self):
        self.state.final_state(self)

    def driver_report(self, msg: str) -> report.Report:
        return report.Report(self.driver_id, msg, self)

    def passenger_report(self, msg: str) -> report.Report:
        return report.Report(self.passenger_id, msg, self)

    def like_driver(self):
        if not self.driver_liked:
            __driver = user.UserManager().find_driver_by_id(self.driver_id)
            if __driver is not None:
                __driver.rating += 0.1

    def like_passenger(self):
        if not self.passenger_liked:
            passenger = user.UserManager().find_passenger_by_id(self.passenger_id)
            if passenger is not None:
                passenger.rating += 0.1


@manager.singleton
class TripManager:
    def __init__(self):
        self.trips: List[Trip] = []

    def del_trip_by_id(self, _id: UUID) -> bool:
        return manager.Manager.del_by_id(self.trips, _id)

    def find_trip_by_id(self, _id: UUID) -> Optional[Trip]:
        return manager.Manager.find_by_id(self.trips, _id)

    def add_trip(self, trip: Trip) -> bool:
        return manager.Manager.add_element(self.trips, trip)


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
        passenger = user.UserManager().find_passenger_by_id(trip.passenger_id)
        if passenger is None:
            raise ValueError('Passenger should be valid')
        if trip.payment_handler.handle(
                trip.price) == 'Passenger have to pay by cash':
            report.ReportManager().add_report(trip.passenger_report('No payment'))
        trip.state = FinishedState()


class RidingState(ITripState):
    def next_state(self, trip: Trip):
        trip.arrival_time = datetime.now()
        trip.state = PaymentState()

    def final_state(self, trip: Trip):
        passenger = user.UserManager().find_passenger_by_id(trip.passenger_id)
        if passenger is None:
            raise ValueError('Passenger should be valid')
        trip.payment_handler.handle(trip.price)
        trip.state = FinishedState()


class PaymentState(ITripState):
    def next_state(self, trip: Trip):
        passenger = user.UserManager().find_passenger_by_id(trip.passenger_id)
        if passenger is None:
            raise ValueError('Passenger should be valid')
        print(trip.payment_handler.handle(trip.price))
        __driver = user.UserManager().find_driver_by_id(trip.driver_id)
        if __driver is None:
            raise ValueError('Driver should be valid')
        __driver.status = driver.Status.READY
        trip.state = FinishedState()

    def final_state(self, trip: Trip):
        self.next_state(trip)


class FinishedState(ITripState):
    def next_state(self, trip: Trip):
        pass

    def final_state(self, trip: Trip):
        pass
