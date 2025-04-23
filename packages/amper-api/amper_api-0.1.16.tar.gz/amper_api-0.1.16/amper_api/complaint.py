from datetime import datetime
from typing import List, Optional

from amper_api.customer import Customer


class Complaint:
    def __init__(self):
        self.id: int = 0
        self.lines: List[ComplaintLine] = []
        self.attachments = []
        self.notes = []
        self.number: str = ""
        self.note: str = ""
        self.status: str = ""
        self.created_at: datetime = datetime.min
        self.updated_at: datetime = datetime.min
        self.updated_by: Customer = None
        self.created_by: Customer = None
        self.customer_external_id: str = ""
        self.customer: Customer = None

    def FieldType(self, field_name):
        if field_name == "lines":
            return ComplaintLine
        if field_name == "updated_by":
            return Customer
        if field_name == "created_by":
            return Customer
        if field_name == "customer":
            return Customer

class ComplaintLine:
    def __init__(self):
        self.id: int = 0
        self.product_id: int = 0
        self.name: str = ""
        self.purchase_date: str = ""
        self.order: str = ""
        self.description: str = ""
        self.complaint: int = 0
        self.product_external_id: str = ""
