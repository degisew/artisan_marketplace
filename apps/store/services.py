from typing import Any
from django.db import IntegrityError, transaction
from apps.store.models import Product, ProductAttribute


class PriceSetService:
    """A service layer for handling daily Product price set.

    Returns:
        dict: returns a recorded product, its attributes, and response status.
    """

    @staticmethod
    @transaction.atomic
    def create_product(payload) -> dict[str, Any]:
        try:
            product = payload.get("product", {})
            valid_colors = product.pop("available_colors", [])
            attributes = payload.get("attributes", {})

            product_instance = Product.objects.create(**product)
            # M2M relationship set
            product_instance.available_colors.set(valid_colors)
            product_attributes = PriceSetService.create_product_attributes(
                product_instance, attributes
            )

            return {"product": product, "attributes": product_attributes}
        except IntegrityError:
            raise ValueError("A database conflict occurred. Please check your input.")
        except Exception as e:
            raise e

    @staticmethod
    def create_product_attributes(product, attributes) -> dict[str, Any]:
        data = [
            ProductAttribute(field_name=field, field_value=value, product=product)
            for field, value in attributes.items()
        ]
        try:
            ProductAttribute.objects.bulk_create(data)
            return attributes
        except Exception as e:
            raise e
