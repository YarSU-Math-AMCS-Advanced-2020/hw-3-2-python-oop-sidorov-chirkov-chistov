from datetime import datetime
from decimal import Decimal
from uuid import uuid4, UUID
from abc import ABC, abstractmethod

from payment import payment_process
from client import ClientManager
from report import Report
from driver import Driver, Status
from map import Map
from offer import Offer
from manager import Manager, singleton


class Trip:
    def __init__(self, driver: Driver, offer: Offer):
        self.offer_id = offer.id
        self.driver_id = driver.id
        self.customer_id = offer.customer_id
        self.departure_time = datetime.now()
        self.estimated_trip_time = Map().trip_time(offer.departure_point, offer.destination_point)
        self.price: Decimal = offer.price
        self.state: ITripState = WaitingState()
        self.arrival_time = None
        self.id = uuid4()
        self.driver_liked = False
        self.customer_liked = False

    def next_state(self):
        self.state.next_state(self)

    def final_state(self):
        self.state.final_state(self)

    def driver_report(self, msg: str) -> Report:
        return Report(msg, self, self.driver_id)

    def customer_report(self, msg: str) -> Report:
        return Report(msg, self, self.customer_id)

    def like_driver(self):
        if not self.driver_liked:
            driver = ClientManager().find_client_by_id(self.driver_id)
            if driver is not None:
                driver.rating += 0.1

    def like_customer(self):
        if not self.customer_liked:
            customer = ClientManager().find_client_by_id(self.customer_id)
            if customer is not None:
                customer.rating += 0.1


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
        customer = ClientManager().find_client_by_id(trip.customer_id)
        if payment_process(customer, self.wait_price) == 'Client have to pay by cash':
            trip.customer_report('No payment')
            # TODO: we have to store reports
        trip.state = FinishedState()


class RidingState(ITripState):
    def next_state(self, trip: Trip):
        trip.arrival_time = datetime.now()
        trip.state = PaymentState()

    def final_state(self, trip: Trip):
        customer = ClientManager().find_client_by_id(trip.customer_id)
        payment_process(customer, trip.price)
        trip.state = FinishedState()


class PaymentState(ITripState):
    def next_state(self, trip: Trip):
        customer = ClientManager().find_client_by_id(trip.customer_id)
        print(payment_process(customer, trip.price))
        driver = ClientManager().find_client_by_id(trip.driver_id)
        if driver is not None:
            driver.status = Status.READY
        trip.state = FinishedState()

    def final_state(self, trip: Trip):
        self.next_state(trip)


class FinishedState(ITripState):
    def next_state(self, trip: Trip):
        pass

    def final_state(self, trip: Trip):
        pass
