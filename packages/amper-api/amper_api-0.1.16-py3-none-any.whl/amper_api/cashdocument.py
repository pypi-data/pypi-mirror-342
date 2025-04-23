from typing import List

from amper_api.customer import Customer
from amper_api.settlement import Settlement


class CashDocumentOperation:
    def __init__(self):
        self.id: int = 0
        self.settlement: Settlement = None
        self.settlement_external_id: str = ""
        self.amount: str = ""
        self.settlement_number: str = ""
        self.type: str = ""
        self.document_header: int = 0

    def FieldType(self, field_name):
        if field_name == "settlement":
            return Settlement


class CashDocument:
    def __init__(self):
        self.id: int = 0
        self.cash_document_operations: List[CashDocumentOperation] = []
        self.customer_external_id: str = ""
        self.customer: Customer = None
        self.number: str = ""
        self.created_at: str = ""
        self.status: str = ""
        self.type: str = ""
        self.date_of_exportation = None
        self.amount: str = ""
        self.user: str = ""
        self.description: str = ""
        self.is_system_operation: bool = False
        self.ordinal: str = ""
        self.cash_drawer: int = 0
        self.sales_rep_email: str = ""
        self.sales_rep_first_name: str = ""
        self.sales_rep_last_name: str = ""
        self.sales_rep_phone: str = ""
        self.sales_rep_identifier: str = ""

    def FieldType(self, field_name):
        if field_name == "cash_document_operations":
            return CashDocumentOperation
        if field_name == "customer":
            return Customer
