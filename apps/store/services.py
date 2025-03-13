from typing import Any
from django.db import IntegrityError, transaction
from apps.store.models import Product, ProductAttribute


class PriceSetService:
    """A service layer for handling daily Product price set.

    Returns:
        dict: returns a recorded product, its attributes, and response status.
    """
    @staticmethod
    @transaction.atomic()
    def create_product(user, payload) -> dict[str, Any]:
        product = payload.get("product", {})
        attributes = payload.get("attributes", {})

        product_instance = Product.objects.create(artisan=user, **product)
        product_attributes = PriceSetService.create_product_attributes(
            product_instance,
            attributes
        )
        return {
            "product": product,
            "attributes": product_attributes
        }

    @staticmethod
    def create_product_attributes(product, attributes) -> dict[str, Any]:
        data = [
            ProductAttribute(field_name=field, field_value=value, product=product)
            for field, value in attributes.items()
        ]
        try:
            ProductAttribute.objects.bulk_create(data, batch_size=100)
            return attributes
        except IntegrityError as e:
            print(f"Failed to create product attributes: {e}")
            return {}
