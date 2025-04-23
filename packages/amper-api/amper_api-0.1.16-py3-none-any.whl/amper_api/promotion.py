from decimal import Decimal
from typing import List, Optional
from datetime import datetime


class Promotion:
    def __init__(self):
        self.id: Optional[int] = None
        self.external_id: str = ""
        self.name: str = ""
        self.start: Optional[datetime] = None
        self.end: Optional[datetime] = None
        self.priority: Optional[int] = None
        self.description: str = ""
        self.short_code: str = ""
        self.is_enabled: Optional[bool] = None
        self.updatable_fields: str = ""
        self.external_identifier: str = ""
        self.internal_description: str = ""
        self.replace_gratifications: str = ""

    def FieldType(self, field_name):
        if field_name == "id":
            return int
        if field_name == "start":
            return datetime
        if field_name == "end":
            return datetime
        if field_name == "priority":
            return int
        if field_name == "is_enabled":
            return bool


class PromotionCustomer:
    def __init__(self):
        self.external_id: str = ""
        self.promotion_external_id: str = ""
        self.customer_external_id: str = ""


class PromotionCustomerCategory:
    def __init__(self):
        self.external_id: str = ""
        self.promotion_external_id: str = ""
        self.customer_category_external_id: str = ""


class ConditionRelation:
    def __init__(self):
        self.external_id: str = ""
        self.parent_relation_external_id: str = ""
        self.promotion_external_id: str = ""
        self.relation: str = ""
        self.order: Optional[int] = None
        self.multiply_reward: Optional[int] = None

    def FieldType(self, field_name):
        if field_name == "order":
            return int
        if field_name == "multiply_reward":
            return int


class ConditionRelationPromotionCondition:
    def __init__(self):
        self.external_id: str = ""
        self.condition_relation_external_id: str = ""
        self.promotion_condition_external_id: str = ""
        self.order: Optional[int] = None

    def FieldType(self, field_name):
        if field_name == "order":
            return int


class PromotionCondition:
    def __init__(self):
        self.external_id: str = ""
        self.name: str = ""


class PromotionConditionItem:
    def __init__(self):
        self.external_id: str = ""
        self.promotion_condition_external_id: str = ""
        self.product_external_id: str = ""
        self.product_category_external_id: str = ""
        self.value: Decimal = Decimal(0)
        self.value_type: str = ""
        self.value_max: Decimal = Decimal(0)
        self.create_temporary_category: bool = False
        self.temporary_category_name: str = ""
        self.temporary_category_products: List[str] = []


class PromotionRewards:
    def __init__(self):
        self.external_id: str = ""
        self.promotion_external_id: str = ""
        self.condition_relation_external_id: str = ""
        self.product_external_id: str = ""
        self.product_category_external_id: str = ""
        self.quantity: Decimal = Decimal(0)
        self.price: Decimal = Decimal(0)
        self.value_type: str = ""
        self.reward_value: Decimal = Decimal(0)
        self.reward: str = ""
