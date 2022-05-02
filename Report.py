from datetime import datetime
from uuid import UUID
from Trip import Trip


class Report:
    def __init__(self, msg: str, trip: Trip, client_id: UUID):
        self.msg = msg
        self.trip = trip
        self.client_id = client_id
        self.time_stamp = datetime.now()

    def __str__(self):
        return f"Time: {self.time_stamp}\nMessage: {self.msg}"

    def on_approved(self):
        pass
