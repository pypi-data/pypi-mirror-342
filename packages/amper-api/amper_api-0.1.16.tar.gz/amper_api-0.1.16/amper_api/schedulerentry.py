from typing import Optional
from datetime import datetime


class SchedulerEntry:
    def __init__(self):
        self.external_id: str = ""
        self.name: str = ""
        self.customer_external_id: str = ""
        self.cron_expression: str = ""
        self.related_user_login: str = ""
        self.sales_representative_identifier: str = ""
        self.is_enabled: bool = False
        self.updatable_fields: str = ""
        self.entry_date: datetime = datetime.min
        self.ended_at: Optional[datetime] = None
        self.ex_dates: Optional[datetime] = None

    def FieldType(self, field_name):
        if field_name == "ended_at":
            return datetime
        if field_name == "ex_dates":
            return datetime
