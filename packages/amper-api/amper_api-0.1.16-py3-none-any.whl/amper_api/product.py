from decimal import Decimal
from typing import List


class ProductImage:
    def __init__(self):
        self.product_id: int = 0
        self.alt: str = ""
        self.image: str = ""
        self.file_name: str = ""
        self.order: int = 0
        self.thumbnail_width: int = 0


class Price:
    def __init__(self):
        self.product_external_id: str = ""
        self.price_level_external_id: str = ""
        self.external_id: str = ""
        self.price: Decimal = Decimal(0)
        self.discount: Decimal = Decimal(0)
        self.start_date: str = ""
        self.end_date: str = ""
        self.order: int = 0


class CategoryDiscount:
    def __init__(self):
        self.category_external_id: str = ""
        self.price_level_external_id: str = ""
        self.external_id: str = ""
        self.discount: Decimal = Decimal(0)
        self.order: int = 0
        self.start_date: str = ""
        self.end_date: str = ""
        self.allow_override_minimal_price: bool = False


class PriceLevel:
    def __init__(self):
        self.name: str = ""
        self.external_id: str = ""
        self.order: int = 0
        self.is_global: bool = False
        self.is_enabled: bool = False
        self.is_promotional: bool = False


class PriceLevelAssigment:
    def __init__(self):
        self.external_id: str = ""
        self.price_level: str = ""
        self.customer_category: str = ""
        self.customer: str = ""


class Stock:
    def __init__(self):
        self.product_external_id: str = ""
        self.stock_level_external_id: str = ""
        self.external_id: str = ""
        self.quantity: Decimal = Decimal(0)
        self.quantity_allocated: Decimal = Decimal(0)


class StockLocation:
    def __init__(self):
        self.name: str = ""
        self.external_id: str = ""


class ProductCategory:
    def __init__(self):
        self.external_id: str = ""
        self.parent_external_id: str = ""
        self.name: str = ""
        self.description: str = ''
        self.seo_tags: str = ""
        self.order: int = 1
        self.updatable_fields: str = ""


class ProductCategoryRelation:
    def __init__(self):
        self.external_id: str = ""
        self.category_external_id: str = ""
        self.product_external_id: str = ""


class CustomerProductRelation:
    def __init__(self):
        self.external_id: str = ""
        self.product_external_id: str = ""
        self.category_external_id: str = ""
        self.customer_external_id: str = ""
        self.excluded: bool = False


class ProductAttributes:
    def __init__(self, key, atr_name, atr_val, enabled_for_filtering=True, show_on_tile=False):
        self.key: str = key
        self.atr_name: str = atr_name
        self.atr_val: str = atr_val
        self.is_b2b: bool = True
        self.is_msf: bool = True
        self.is_b2c: bool = True
        self.enabled_for_filtering: bool = enabled_for_filtering
        self.show_on_tile: bool = show_on_tile


class Product:
    def __init__(self):
        self.attributes: List[ProductAttributes] = []
        self.name: str = ""
        self.friendly_name: str = ""
        self.short_description: str = ""
        self.description: str = ""
        self.short_code: str = ""
        self.sku: str = ""
        self.ean: str = ""
        self.brand_short_code: str = ""
        self.vat: int = 0
        self.available_on: str = '2020-01-01'
        self.is_published: bool = False
        self.is_featured: bool = False
        self.weight: Decimal = Decimal()
        self.default_unit_of_measure: str = ""
        self.external_id: str = ""
        self.updatable_fields: str = ""
        self.cumulative_unit_of_measure: str = ""
        self.cumulative_converter: Decimal = Decimal(0)
        self.can_be_split: bool = False
        self.cumulative_unit_ratio_splitter: Decimal = Decimal(0)
        self.unit_roundup: bool = False
        self.default_price: Decimal = Decimal()
        self.is_b2b_product: bool = False
        self.is_b2c_product: bool = False
        self.is_msf_product: bool = False
        self.is_b2m_product: bool = False
        self.is_msk_product: bool = False
        self.dimension_unit_of_measure: str = ""
        self.dimension_width: Decimal = Decimal(0)
        self.dimension_height: Decimal = Decimal(0)
        self.dimension_depth: Decimal = Decimal(0)
        self.is_product_saleable: bool = False
        self.piggy_bank_budget: Decimal = Decimal(0)
        self.concession_a: Decimal = Decimal(0)
        self.concession_b: Decimal = Decimal(0)
        self.concession_c: Decimal = Decimal(0)
        self.capacity: Decimal = Decimal(0)
        self.sorting_column: str = ""
        self.is_bestseller: bool = False
        self.is_for_sale: bool = False
        self.status_description: str = ""
        self.minimal_price: Decimal = Decimal(0)
        self.product_subtype: int = 0
        self.sanitized_description: str = ""
        self.cn_code: str = ""
        self.order: int = 0
        self.purchase_price: Decimal = Decimal(0)
        self.allow_override_minimal_price: bool = False


class RelatedProducts:
    def __init__(self):
        self.external_id: str = ""
        self.related_products: List[RelatedProduct] = []

    def FieldType(self, field_name):
        if field_name == "related_products":
            return RelatedProduct


class RelatedProduct:
    def __init__(self):
        self.external_id: str = ""


class ProductSets:
    def __init__(self):
        self.external_id: str = ""
        self.product_sets: List[ProductSet] = []

    def FieldType(self, field_name):
        if field_name == "product_sets":
            return ProductSet


class ProductSet:
    def __init__(self):
        self.external_id: str = ""


class UnitOfMeasure:
    def __init__(self):
        self.product_external_id: str = ""
        self.external_id: str = ""
        self.name: str = ""
        self.converter: Decimal = Decimal(0)
        self.can_be_split: bool = False
        self.cumulative_unit_ratio_splitter: Decimal = Decimal(0)
        self.unit_roundup: bool = False
        self.weight: Decimal = Decimal(0)
        self.capacity: Decimal = Decimal(0)


class DefaultPriceOverwriteForCategoryDiscount:
    def __init__(self):
        self.external_id: str = ""
        self.price_level: str = ""
        self.category_discount: str = ""
        self.order: int = 0


class Manufacturer:
    def __init__(self):
        self.external_id: str = ""
        self.name: str = ""
        self.slug: str = ""
        self.order: int = 0
        self.description: str = ""
        self.seo_tags: str = ""
        self.is_hidden: bool = False
        self.is_featured: bool = False
        self.short_code: str = ""
        self.updatable_fields: str = ""


class Brand:
    def __init__(self):
        self.external_id: str = ""
        self.manufacturer_external_id: str = ""
        self.name: str = ""
        self.slug: str = ""
        self.order: int = 0
        self.description: str = ""
        self.seo_tags: str = ""
        self.is_hidden: bool = False
        self.is_featured: bool = False
        self.short_code: str = ""
        self.updatable_fields: str = ""
