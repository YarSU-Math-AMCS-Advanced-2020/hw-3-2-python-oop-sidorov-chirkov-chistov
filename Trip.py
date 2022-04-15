import datetime
import enum
import Driver
import Offer
import AbstractManager


class Status(enum.Enum):
    started = 0
    in_progress = 1
    finished = 2
    canceled = 3
    deleted = 4


class TripInfo:
    def __init__(self, offer: Offer, departure_time: datetime, estimated_trip_time: datetime, driver: Driver):
        self.offer_id = offer.id
        self.departure_time = departure_time
        self.estimated_trip_time = estimated_trip_time
        self.driver_id = id(driver)


class Trip:
    def __init__(self, trip_info: TripInfo):
        self.trip_info = trip_info
        self.status = Status.started


class TripManager(AbstractManager.Manager):
    def __init__(self):
        self.trips: list[Trip] = []

    def del_trip_by_id(self, id: int):
        return self.del_by_id(self.trips, id)

    def find_trip_by_id(self, id: int):
        return self.find_by_id(self.trips, id)

    def add_trip(self, trip: Trip):
        return self.add_element(self.trips, trip)