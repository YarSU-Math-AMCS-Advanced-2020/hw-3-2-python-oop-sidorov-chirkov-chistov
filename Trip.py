from datetime import datetime
from decimal import Decimal
from Client import ClientManager
from Report import Report
import Driver
from Location import Traffic
import Offer
from AbstractManager import Manager, singleton
from uuid import uuid4, UUID
from abc import ABC, abstractmethod


class Trip:
    def __init__(self, driver: Driver, offer: Offer):
        self.offer_id = offer.id
        self.driver_id = driver.id
        self.customer_id = offer.client_id
        self.departure_time = datetime.now()
        self.estimated_trip_time = Traffic.trip_time(offer.departure_point, offer.destination_point)
        self.price: Decimal = offer.price
        self.state: ITripState = WaitingState()
        self.arrival_time = None
        self.id = uuid4()
        self.driver_liked = False
        self.customer_liked = False

    def next_state(self):
        self.state.next_state(self)

    def __interrupt(self):
        self.state = FinishedState()

    def driver_charge(self, msg: str) -> Report:
        return Report(msg, self, self.driver_id)

    def customer_charge(self, msg: str) -> Report:
        return Report(msg, self, self.customer_id)

    def like_driver(self):
        if not self.driver_liked:
            dr = ClientManager().find_client_by_id(self.driver_id)
            if dr is not None:
                dr.rating += 0.1

    def like_customer(self):
        if not self.customer_liked:
            cu = ClientManager().find_client_by_id(self.customer_id)
            if cu is not None:
                cu.rating += 0.1


@singleton
class TripManager:
    def __init__(self):
        self.trips: list[Trip] = []

    def del_trip_by_id(self, id: UUID) -> bool:
        return Manager.del_by_id(self.trips, id)

    def find_trip_by_id(self, id: UUID) -> Trip | None:
        return Manager.find_by_id(self.trips, id)

    def add_trip(self, trip: Trip) -> bool:
        return Manager.add_element(self.trips, trip)


class ITripState(ABC):
    @abstractmethod
    def next_state(self, trip: Trip):
        pass


class WaitingState(ITripState):
    def next_state(self, trip: Trip):
        passed_time = int((datetime.now() - trip.departure_time).total_seconds() / 60)
        wait_min_price = 10.5
        trip.price += Decimal(wait_min_price * passed_time)
        trip.state = RidingState()


class RidingState(ITripState):
    def next_state(self, trip: Trip):
        trip.arrival_time = datetime.now()
        trip.state = PaymentState()


class PaymentState(ITripState):
    def next_state(self, trip: Trip):
        # here we have to get payment(call payment func)
        trip.state = FinishedState()


class FinishedState(ITripState):
    def next_state(self, trip: Trip):
        trip.state = FinishedState()
