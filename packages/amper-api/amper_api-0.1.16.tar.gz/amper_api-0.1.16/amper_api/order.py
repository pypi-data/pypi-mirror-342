from decimal import Decimal
from typing import List, Optional
from datetime import datetime

from amper_api.promotion import Promotion
from amper_api.customer import Customer


class OrderList:
    def __init__(self):
        self.token: str = ""
        self.created: datetime = datetime.min
        self.status: str = ""
        self.user_email: str = ""
        self.total_gross: str = ""


class OrderLine:
    def __init__(self):
        self.id: int = None
        self.attributes = []
        self.product_external_id: str = ""
        self.product_short_code: str = ""
        self.external_id: str = ""
        self.product_name: str = ""
        self.product_sku: str = ""
        self.quantity: Decimal = Decimal(0)
        self.base_price_net: str = ""
        self.discount: str = ""
        self.unit_price_net: str = ""
        self.unit_price_gross: str = ""
        self.tax_rate: str = ""
        self.is_promotion_reward: bool = False
        self.product: int = 0
        self.promotion_condition: Optional[int] = None
        self.promotion: Promotion = None
        self.source_stock_location_name: str = ""

    def FieldType(self, field_name):
        if field_name == "attributesList":
            return None
        if field_name == "promotion":
            return Promotion
        if field_name == "promotion_condition":
            return int
        if field_name == "id":
            return int

class ShippingAddress:
    def __init__(self):
        self.external_id: str = ""
        self.id: int = 0
        self.deleted = None
        self.name: str = ""
        self.city: str = ""
        self.postal_code: str = ""
        self.street: str = ""
        self.street_continuation: str = ""
        self.email: str = ""
        self.phone = None
        self.voivodeship: str = ""
        self.customer: int = 0


class Order:
    def __init__(self):
        self.id: Optional[int] = None
        self.external_id: str = ""
        self.token: str = ""
        self.lines: List[OrderLine] = []
        self.customer_external_id: str = ""
        self.shipping_address: ShippingAddress = None
        self.billing_address: ShippingAddress = None
        self.customer: Customer = None
        self.created: datetime = datetime.min
        self.updated: datetime = datetime.min
        self.status: str = ""
        self.user_email: str = ""
        self.shipping_price_net: str = ""
        self.shipping_price_gross: str = ""
        self.products_total_net: str = ""
        self.products_total_gross: str = ""
        self.total_net: str = ""
        self.total_gross: str = ""
        self.paid: Decimal = Decimal(0)
        self.discount_amount: Decimal = Decimal(0)
        self.customer_note: str = ""
        self.shipment_type: Optional[int] = None
        self.order_number: str = ""
        self.order_type: str = ""
        self.form_of_payment: str = ""

    def FieldType(self, field_name):
        if field_name == "lines":
            return OrderLine
        elif field_name == "shipping_address":
            return ShippingAddress
        elif field_name == "billing_address":
            return ShippingAddress
        elif field_name == "customer":
            return Customer
        elif field_name == "id":
            return int
        elif field_name == "shipment_type":
            return int
