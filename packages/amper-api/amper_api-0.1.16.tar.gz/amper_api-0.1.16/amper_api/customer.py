from decimal import Decimal
from typing import List, Optional
from datetime import datetime

from amper_api.product import PriceLevel


class Account:
    def __init__(self):
        self.name: str = ""
        self.short_name: str = ""
        self.external_id: str = ""
        self.city: str = ""
        self.postal_code: str = ""
        self.street: str = ""
        self.email: str = ""
        self.phone: str = ""
        self.voivodeship: str = ""
        self.tax_id: str = ""
        self.customers: List[Customer] = []

    def FieldType(self, field_name):
        if field_name == "customers":
            return Customer


class Customer:
    def __init__(self):
        self.external_id: str = ""
        self.name: str = ""
        self.friendly_name: str = ""
        self.short_name: str = ""
        self.primary_email: str = ""
        self.phone: str = ""
        self.city: str = ""
        self.postal_code: str = ""
        self.street: str = ""
        self.tax_id: str = ""
        self.comments: str = ""
        self.price_level_external_id: str = ""
        self.complementary_price_level_external_id: str = ""
        self.payment_form_external_id: str = ""
        self.login: str = ""
        self.password: str = ""
        self.trade_credit_limit: Decimal = Decimal(0)
        self.overdue_limit: Decimal = Decimal(0)
        self.discount: Decimal = Decimal(0)
        self.currency_code: str = ""
        self.id: int = 0
        self.overdue_settlements: int = 0
        self.max_num_of_overdue_settlements: int = 0
        self.currency_format: str = ""
        self.ftp_host: str = ""
        self.ftp_port: str = ""
        self.ftp_user: str = ""
        self.ftp_pass: str = ""
        self.ftp_secure: bool = False
        self.type: str = ""
        self.added_at: datetime = datetime.now()
        self.updated_at: Optional[datetime] = None
        self.first_login_at: Optional[datetime] = None
        self.is_free_shipping: bool = False
        self.account: Optional[int] = None
        self.default_address: str = ""
        self.currency: str = ""
        self.updatable_fields: str = ""
        self.stock_location_external_id: str = ""
        self.concession_a_valid_until: Optional[datetime] = None
        self.concession_b_valid_until: Optional[datetime] = None
        self.concession_c_valid_until: Optional[datetime] = None
        self.default_sales_rep_identifier: str = ""
        self.check_minimal_price: bool = False
        self.is_locked_for_sale: bool = False
        self.ean: str = ""
        self.latitude: Optional[Decimal] = None
        self.longitude: Optional[Decimal] = None
        self.export_customer: bool = False
        self.value_restrictions: Optional[Decimal] = None
        self.value_restrictions_limit: Optional[Decimal] = None
        self.weight_restrictions: Optional[Decimal] = None
        self.weight_restrictions_limit: Optional[Decimal] = None
        self.free_shipping_from: Optional[Decimal] = None

    def FieldType(self, field_name):
        if field_name == "updated_at":
            return datetime
        if field_name == "first_login_at":
            return datetime
        if field_name == "account":
            return int
        if field_name == "concession_a_valid_until":
            return datetime
        if field_name == "concession_b_valid_until":
            return datetime
        if field_name == "concession_c_valid_until":
            return datetime
        if field_name == "latitude":
            return Decimal
        if field_name == "longitude":
            return Decimal
        if field_name == "value_restrictions":
            return Decimal
        if field_name == "value_restrictions_limit":
            return Decimal
        if field_name == "weight_restrictions":
            return Decimal
        if field_name == "weight_restrictions_limit":
            return Decimal
        if field_name == "free_shipping_from":
            return Decimal


class CustomerProductLogisticMinimum:
    def __init__(self):
        self.external_id: str = ""
        self.product_external_id: str = ""
        self.customer_external_id: str = ""
        self.logistic_minimum: Decimal = Decimal(0)


class Address:
    def __init__(self):
        self.name: str = ""
        self.city: str = ""
        self.postal_code: str = ""
        self.street: str = ""
        self.street_continuation: str = ""
        self.email: str = ""
        self.phone: str = ""
        self.voivodeship: str = ""
        self.external_id: str = ""
        self.customer_external_id: str = ""
        self.updatable_fields: str = ""


class CustomerCategory:
    def __init__(self):
        self.external_id: str = ""
        self.parent_external_id: str = ""
        self.name: str = ""
        self.description: str = ""
        self.seo_tags: str = ""
        self.order: str = ""
        self.updatable_fields: str = ""


class CustomerCategoryRelation:
    def __init__(self):
        self.external_id: str = ""
        self.category_external_id: str = ""
        self.customer_external_id: str = ""


class CustomerSalesRepresentative:
    def __init__(self):
        self.external_id: str = ""
        self.sales_representative_identifier: str = ""
        self.customer_category_external_id: str = ""
        self.customer_external_id: str = ""


class PaymentForm:
    def __init__(self):
        self.external_id: str = ""
        self.name: str = ""
        self.is_cash: bool = False
        self.default_payment_date_in_days: int = 14


class CustomerForExport:
    def __init__(self):
        self.external_id: str = ""
        self.name: str = ""
        self.short_name: str = ""
        self.primary_email: str = ""
        self.phone: str = ""
        self.city: str = ""
        self.postal_code: str = ""
        self.street: str = ""
        self.tax_id: str = ""
        self.comments: str = ""
        self.price_level_external_id: str = ""
        self.payment_form_external_id: str = ""
        self.login: str = ""
        self.password: str = ""
        self.trade_credit_limit: Decimal = Decimal(0)
        self.overdue_limit: Decimal = Decimal(0)
        self.discount: Decimal = Decimal(0)
        self.currency_code: str = ""
        self.id: int = 0
        self.overdue_settlements: int = 0
        self.currency_format: str = ""
        self.ftp_host: str = ""
        self.ftp_port: str = ""
        self.ftp_user: str = ""
        self.ftp_pass: str = ""
        self.ftp_secure: bool = False
        self.type: str = ""
        self.added_at: datetime = datetime.now()
        self.updated_at: Optional[datetime] = None
        self.first_login_at: Optional[datetime] = None
        self.is_free_shipping: bool = False
        self.currency: str = ""
        self.updatable_fields: str = ""
        self.stock_location_external_id: str = ""
        self.concession_a_valid_until: Optional[datetime] = None
        self.concession_b_valid_until: Optional[datetime] = None
        self.concession_c_valid_until: Optional[datetime] = None
        self.default_sales_rep_identifier: str = ""
        self.account: int = 0
        self.default_price: PriceLevel = None
        self.payment_form: PaymentForm = None
        self.default_sales_rep: SalesRepresetnative = None
        self.default_stock_location = None
        self.default_address: Address = None

    def FieldType(self, field_name):
        if field_name == "default_sales_rep":
            return SalesRepresetnative
        if field_name == "default_address":
            return Address
        if field_name == "payment_form":
            return PaymentForm
        if field_name == "default_price":
            return PriceLevel
        if field_name == "updated_at":
            return datetime
        if field_name == "first_login_at":
            return datetime
        if field_name == "concession_a_valid_until":
            return datetime
        if field_name == "concession_b_valid_until":
            return datetime
        if field_name == "concession_c_valid_until":
            return datetime


class SalesRepresetnative:
    def __init__(self):
        self.id: int = 0
        self.deleted = None
        self.identifier: str = ""
        self.first_name: str = ""
        self.last_name: str = ""
        self.phone: str = ""
        self.email: str = ""
        self.status: str = ""
        self.keycloak_id: str = ""
        self.supervisor: str = ""


class CustomerNote:
    def __init__(self):
        self.id: int = 0
        self.author: str = ""
        self.customer: int = 0
        self.body: str = ""
        self.note_type: CustomerNoteType = None
        self.added_at: datetime = datetime.min
        self.created_by: str = ""
        self.customer_external_id: str = ""

    def FieldType(self, field_name):
        if field_name == "note_type":
            return CustomerNoteType


class CustomerNoteType:
    def __init__(self):
        self.id: int = 0
        self.type: str = ""
        self.value: str = ""
        self.order: int = 0
