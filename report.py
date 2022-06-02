from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID

import manager
import trip
import user


class ReportStatus(Enum):
    PENDING = 0
    DECLINED = 1
    APPROVED = 2


class Report:
    def __init__(self, user_id: UUID, message: str, __trip: trip.Trip):
        self.user_id = user_id
        self.message = message
        self.time_stamp = datetime.now()
        self.trip = __trip
        self.status = ReportStatus.PENDING

    def __str__(self):
        return f"Time: {self.time_stamp}\nMessage: {self.message}"

    def approve(self):
        __user = user.UserManager().find_user_by_id(self.user_id)
        if user is not None:
            __user.rating -= 1.0
        self.status = ReportStatus.APPROVED

    def decline(self):
        self.status = ReportStatus.DECLINED


@manager.singleton
class ReportManager:
    def __init__(self):
        self.reports: List[Report] = []

    def del_report_by_id(self, _id: UUID) -> bool:
        return manager.Manager.del_by_id(self.reports, _id)

    def find_report_by_id(self, _id: UUID) -> Optional[Report]:
        return manager.Manager.find_by_id(self.reports, _id)

    def add_report(self, report: Report) -> bool:
        return manager.Manager.add_element(self.reports, report)
