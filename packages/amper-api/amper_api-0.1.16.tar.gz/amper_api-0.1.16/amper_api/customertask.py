from decimal import Decimal
from typing import List, Optional
from datetime import datetime


class CustomerTask:
    def __init__(self):
        self.external_id: str = ""
        self.name: str = ""
        self.date_start: Optional[datetime] = None
        self.date_end: Optional[datetime] = None
        self.goals: List[CustomerTaskGoal] = []
        self.customers: List[TaskCustomers] = []

    def FieldType(self, field_name):
        if field_name == "date_start":
            return datetime
        if field_name == "date_end":
            return datetime
        if field_name == "goals":
            return CustomerTaskGoal
        if field_name == "customers":
            return TaskCustomers


class CustomerTaskGoal:
    def __init__(self):
        self.product_external_id: str = ""
        self.type: str = ""
        self.goal_value: Decimal = Decimal(0)


class TaskCustomers:
    def __init__(self):
        self.customer_external_id: str = ""
