from decimal import Decimal
from typing import List, Optional
from datetime import datetime

from amper_api.customer import Customer


class Document:
    def __init__(self):
        self.external_id: str = ""
        self.id: int = None
        self.document_lines: List[DocumentLine] = []
        self.customer_external_id: str = ""
        self.customer: Customer = None
        self.document_provider: Optional[DocumentProvider] = None
        self.visit: Visit = None
        self.document_type: DocumentType = None
        self.stock_location = None
        self.number: str = ""
        self.status: str = ""
        self.date: datetime = datetime.min
        self.due_date: Optional[datetime] = None
        self.description: str = ""
        self.value_net: Decimal = Decimal(0)
        self.value_gross: Decimal = Decimal(0)
        self.created_at: Optional[datetime] = None
        self.modified_at: Optional[datetime] = None
        self.ordinal: str = ""
        self.source_document: int = 0
        self.print_date: Optional[datetime] = None
        self.synchronization_date: Optional[datetime] = None
        self.delivery_date: Optional[datetime] = None
        self.percentage_discount: Decimal = Decimal(0)
        self.username: str = ""
        self.document_provider_short_name: str = ""
        self.document_type_name: str = ""
        self.payment_form_external_id: str = ""
        self.is_external_document: str = ""
        self.sales_rep_identifier: str = ""
        self.sales_rep_first_name: str = ""
        self.sales_rep_last_name: str = ""
        self.sales_rep_email: str = ""
        self.sales_rep_phone: str = ""
        self.document_metadata = None
        self.coords_details: CoordsDetails = None

    def FieldType(self, field_name):
        if field_name == "document_lines":
            return DocumentLine
        if field_name == "document_provider":
            return DocumentProvider
        if field_name == "visit":
            return Visit
        if field_name == "document_type":
            return DocumentType
        if field_name == "due_date":
            return datetime
        if field_name == "created_at":
            return datetime
        if field_name == "modified_at":
            return datetime
        if field_name == "print_date":
            return datetime
        if field_name == "synchronization_date":
            return datetime
        if field_name == "delivery_date":
            return datetime
        if field_name == "coords_details":
            return CoordsDetails


class DocumentLine:
    def __init__(self):
        self.id: int = 0
        self.external_id: str = ""
        self.document: str = ""
        self.product_symbol: str = ""
        self.product_ean: str = ""
        self.product_additional_fees_net: Decimal = Decimal(0)
        self.product_additional_fees_gross: Decimal = Decimal(0)
        self.product_name: str = ""
        self.vat: int = 0
        self.unit: str = ""
        self.quantity: Decimal = Decimal(0)
        self.unit_aggregate: str = ""
        self.quantity_aggregate: Decimal = Decimal(0)
        self.price_net: Decimal = Decimal(0)
        self.price_gross: Decimal = Decimal(0)
        self.value_net: Decimal = Decimal(0)
        self.value_gross: Decimal = Decimal(0)
        self.manufacturer: str = ""
        self.make: str = ""
        self.group: str = ""
        self.product_external_id: str = ""
        self.product_vat: int = 0
        self.base_price: Decimal = Decimal(0)
        self.percentage_discount: Decimal = Decimal(0)
        self.source_document_line: int = 0
        self.source_price_level_desc = None
        self.created_at: Optional[datetime] = None
        self.modified_at: Optional[datetime] = None
        self.document_promotion: str = ""
        self.promotion_condition: str = ""
        self.promotion_condition_relation: str = ""
        self.source_price_level: Optional[int] = None
        self.price_level_external_id: str = ""
        self.line_metadata: List[LineMetadata] = []
        self.applied_promotion: AppliedPromotion = None
        self.is_promotion_reward: bool = False
        self.piggy_bank_budget: Optional[int] = None
        self.piggy_bank_budget_built: Optional[int] = None
        self.user_discount: Optional[Decimal] = None
        self.product: int = 0
        self.budget: Optional[int] = None
        self.source_target_goal: Optional[int] = None
        self.export_rewards_to_a_separate_doc: bool = False

    def FieldType(self, field_name):
        if field_name == "applied_promotion":
            return AppliedPromotion
        if field_name == "line_metadata":
            return LineMetadata
        if field_name == "created_at":
            return datetime
        if field_name == "modified_at":
            return datetime
        if field_name == "source_price_level":
            return int
        if field_name == "piggy_bank_budget":
            return int
        if field_name == "piggy_bank_budget_built":
            return int
        if field_name == "user_discount":
            return int
        if field_name == "budget":
            return int
        if field_name == "source_target_goal":
            return int


class DocumentType:
    def __init__(self):
        self.id: int = 0
        self.name: str = ""
        self.series: str = ""
        self.template: str = ""
        self.annual: bool = False
        self.monthly: bool = False
        self.current_number: int = 0
        self.model_name: str = ""


class Visit:
    def __init__(self):
        self.id: int = 0
        self.customer_name: str = ""
        self.customer_short_name: str = ""
        self.sales_representatives: str = ""
        self.date_start: Optional[datetime] = None
        self.date_end: Optional[datetime] = None
        self.username: str = ""
        self.virtual_visit: bool = False
        self.coords_details: CoordsDetails = None
        self.customer: int = 0

    def FieldType(self, field_name):
        if field_name == "date_start":
            return datetime
        if field_name == "date_end":
            return datetime
        if field_name == "coords_details":
            return CoordsDetails


class AppliedPromotion:
    def __init__(self):
        self.id: int = 0
        self.name: str = ""
        self.short_code: str = ""
        self.external_id = None
        self.start: datetime = datetime.min
        self.end: datetime = datetime.min
        self.priority: int = 0
        self.description: str = ""
        self.internal_description: str = ""
        self.external_identifier: str = ""
        self.is_required: bool = False


class DocumentProvider:
    def __init__(self):
        self.id: int = 0
        self.name: str = ""
        self.short_name: str = ""


class Coords:
    def __init__(self):
        self.speed: str = ""
        self.heading: str = ""
        self.accuracy: str = ""
        self.altitude: str = ""
        self.latitude: str = ""
        self.longitude: str = ""
        self.altitudeAccuracy: str = ""

class CoordsDetails:
    def __init__(self):
        self.coords: Coords = None
        self.timestamp: str = ""

    def FieldType(self, field_name):
        if field_name == "coords":
            return Coords


class LineMetadata:
    def __init__(self):
        self.step: int = 0
        self.amount: Optional[Decimal] = None
        self.discount: Optional[Decimal] = None
        self.description: str = ""
        self.relation_id: Optional[int] = None
        self.condition_id: Optional[int] = None
        self.price_level_id: Optional[int] = None

    def FieldType(self, field_name):
        if field_name == "amount":
            return Decimal
        if field_name == "discount":
            return Decimal
        if field_name == "relation_id":
            return int
        if field_name == "condition_id":
            return int
        if field_name == "price_level_id":
            return int
