from decimal import Decimal


class Settlement:
    def __init__(self):
        self.customer: str = ""
        self.account: str = ""
        self.number: str = ""
        self.value: Decimal = Decimal(0)
        self.value_to_pay: Decimal(0)
        self.date: str = ""
        self.due_date: str = ""
        self.external_id: str = ""
