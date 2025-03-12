from typing import Iterable
from django.conf import settings
from django.db import models
from apps.core.models import AbstractBaseModel, DataLookup
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _


class Category(AbstractBaseModel):
    name = models.CharField(
        verbose_name=_("Name"),
        max_length=100
    )

    value = models.CharField(
        verbose_name=_("Value"),
        max_length=100
    )

    slug = models.SlugField(
        max_length=100
    )

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        db_table = 'category'

    def __str__(self) -> str:
        return self.name

    def save(self, force_insert: bool, force_update: bool, using: str | None, update_fields: Iterable[str] | None) -> None:
        self.slug = slugify(self.name)


class CategoryAttribute(AbstractBaseModel):
    """A model for defining attributes for some sub-category level
    since most of the products share the same attribute
    as a some category(not usually per each product item).
    This will be used in the front-end form.
    """
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="+",
        verbose_name=_("Product Category"),
    )

    field_name = models.CharField(
        max_length=100,
        verbose_name=_("Field Name")
    )

    field_type = models.ForeignKey(
        DataLookup,
        on_delete=models.SET_NULL,
        null=True,
        related_name="+",
        verbose_name=_("Field Type"),
        limit_choices_to={"type": "attribute_field_type"},
    )

    # TODO: Think about this. whether DataLookup is good or not
    form_type = models.ForeignKey(
        DataLookup,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        verbose_name=_("Form Type"),
        limit_choices_to={"type": "attribute_form_type"},
    )

    required = models.BooleanField(verbose_name=_("Required"), default=True)

    class Meta:
        verbose_name: str = "Product Category Attribute"
        verbose_name_plural: str = "Product Category Attributes"
        db_table: str = "product_category_attribute"

    def __str__(self) -> str:
        return self.field_name


class Product(AbstractBaseModel):
    name = models.CharField(
        max_length=100,
        verbose_name=_("Name")
    )

    artisan = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='products'
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="product_categories",
        verbose_name=_("Category"),
        limit_choices_to={"tn_children_pks": ""}
    )

    material = models.CharField(max_length=50, blank=True, null=True)

    description = models.TextField(
        verbose_name=_("Description")
    )

    quantity = models.IntegerField(
        verbose_name=_("Quantity")
    )

    available_colors = models.ForeignKey(
        DataLookup,
        on_delete=models.CASCADE,
        null=True,
        limit_choices_to={"type": "product_color_type"}
    )

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name=_("Price")
    )

    class Meta:
        verbose_name: str = "Product"
        verbose_name_plural: str = "Products"
        db_table: str = "product"

    def update_price(self, price, is_for_sale):
        self.price = price
        self.save()

    def __str__(self) -> str:
        return self.name


class ProductAttribute(AbstractBaseModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="product_attributes"
    )

    field_name = models.CharField(
        max_length=100,
        verbose_name=_("Name")
    )

    field_value = models.CharField(
        max_length=200,
        verbose_name=_("Value"),
    )

    class Meta:
        verbose_name: str = "Product Attribute"
        verbose_name_plural: str = "Product Attributes"
        db_table: str = "product_attribute"

    def __str__(self) -> str:
        return self.field_name
