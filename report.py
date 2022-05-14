import enum
from datetime import datetime
from uuid import UUID

from client import ClientManager
from trip import Trip


class ReportStatus(enum.Enum):
    PENDING = 0
    DECLINED = 1
    APPROVED = 2


class Report:
    def __init__(self, msg: str, trip: Trip, client_id: UUID):
        self.msg = msg
        self.trip = trip
        self.client_id = client_id
        self.time_stamp = datetime.now()
        self.status = ReportStatus.PENDING

    def __str__(self):
        return f"Time: {self.time_stamp}\nMessage: {self.msg}"

    def approve(self):
        cl = ClientManager().find_client_by_id(self.client_id)
        if cl is not None:
            cl.rating -= 1.0
        self.status = ReportStatus.APPROVED

    def decline(self):
        self.status = ReportStatus.DECLINED
