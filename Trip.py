from datetime import datetime
import enum
import Driver
from Location import Traffic
import Offer
from AbstractManager import Manager, singleton
from uuid import uuid4, UUID


class Status(enum.Enum):
    started = 0
    in_progress = 1
    finished = 2
    canceled = 3
    deleted = 4


class Trip:
    def __init__(self, driver: Driver, offer: Offer):
        self.offer_id = offer.id
        self.driver_id = driver.id
        self.departure_time = datetime.now()
        self.estimated_trip_time = Traffic.trip_time(offer.departure_point, offer.destination_point)
        self.status = Status.started
        self.id = uuid4()


@singleton
class TripManager:
    def __init__(self):
        self.trips: list[Trip] = []

    def del_trip_by_id(self, id: int) -> bool:
        return Manager.del_by_id(self.trips, id)

    def find_trip_by_id(self, id: int) -> Trip | None:
        return Manager.find_by_id(self.trips, id)

    def add_trip(self, trip: Trip) -> bool:
        return Manager.add_element(self.trips, trip)
