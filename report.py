import enum
from datetime import datetime
from uuid import UUID

from client import ClientManager
from manager import singleton, Manager
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
        client = ClientManager().find_client_by_id(self.client_id)
        if client is not None:
            client.rating -= 1.0
        self.status = ReportStatus.APPROVED

    def decline(self):
        self.status = ReportStatus.DECLINED


@singleton
class ReportManager:
    def __init__(self):
        self.reports: list[Report] = []

    def del_report_by_id(self, id: UUID) -> bool:
        return Manager.del_by_id(self.reports, id)

    def find_report_by_id(self, id: UUID) -> Report | None:
        return Manager.find_by_id(self.reports, id)

    def add_report(self, report: Report) -> bool:
        return Manager.add_element(self.reports, report)
