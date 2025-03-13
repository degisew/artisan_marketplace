from typing import Any
from django.db import transaction
from apps.store.models import Product, ProductAttribute


class PriceSetService:
    """A service layer for handling daily Product price set.

    Returns:
        dict: returns a recorded product, its attributes, and response status.
    """
    @staticmethod
    @transaction.atomic()
    def create_product(payload) -> dict[str, Any]:
        product = payload["product"]
        attributes = payload["attributes"]

        product_instance = Product.objects.create(**product)

        product_attributes = PriceSetService.create_product_attributes(
            product_instance,
            attributes
        )

        return {
            "product": product,
            "updated_attributes": product_attributes
        }

    @staticmethod
    def create_product_attributes(product, attributes) -> list[Any]:
        product_attributes = {attr.field_name: attr for attr in product.product_attributes.all()}

        for field_name, field_value in attributes.items():
            if field_name in product_attributes:
                product_attributes[field_name].field_value = field_value

        ProductAttribute.objects.bulk_create(product_attributes.values(), ["field_value"])

        return list(product_attributes.values())
