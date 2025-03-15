import pytest
from django.db import IntegrityError
from apps.store.models import Category, CategoryAttribute
from django.utils.text import slugify

pytestmark = pytest.mark.django_db


class TestCategoryModel:
    def test_slug_is_auto_generated_if_blank(self):
        category = Category.objects.create(name="Pottery")
        assert category.slug == slugify("Pottery")

    def test_slug_is_not_overwritten_if_provided(self):
        category = Category.objects.create(name="Pottery", slug="custom-slug")
        assert category.slug == "custom-slug"

    def test_category_name_is_unique(self, category_factory):
        category_factory(name="UniqueName")
        with pytest.raises(Exception):
            category_factory(name="UniqueName")

    def test_category_slug_is_unique(self, category_factory):
        category_factory(slug="unique-slug")
        with pytest.raises(Exception):
            category_factory(slug="unique-slug")


class TestCategoryAttributeModel:
    def test_category_attribute_has_valid_category(self, category_factory, category_attribute_factory):
        category = category_factory()
        attribute = category_attribute_factory(category=category)
        assert attribute.category == category

    # def test_category_attribute_field_type_constraint(self, category_factory, data_lookup_factory):
    #     valid_lookup = data_lookup_factory(type="attribute_field_type")
    #     category = category_factory()

    #     category_attribute = CategoryAttribute.objects.create(
    #         category=category,
    #         field_name="Color",
    #         field_type=valid_lookup
    #     )
    #     assert category_attribute.field_type == valid_lookup

    #     invalid_lookup = data_lookup_factory(type="wrong_type")

        # with pytest.raises(IntegrityError):
        #     CategoryAttribute.objects.create(
        #         category=category,
        #         field_name="Size",
        #         field_type=invalid_lookup
        #     )


class TestProductModel:
    def test_product_creation(self, product_factory, category_factory, user_factory):
        user = user_factory()
        category = category_factory()
        product = product_factory(artisan=user, category=category)
        assert product.name
        assert product.artisan == user
        assert product.category == category

    def test_product_with_colors(self, product_factory, data_lookup_factory, category_factory, user_factory):
        user = user_factory()
        category = category_factory()
        product = product_factory(artisan=user, category=category)

        color1 = data_lookup_factory(type="product_color_type", value="Red")
        color2 = data_lookup_factory(type="product_color_type", value="Blue")
        product.available_colors.set([color1, color2])

        # Verify many-to-many relationship
        assert color1 in product.available_colors.all()
        assert color2 in product.available_colors.all()

    def test_product_price_precision(self, product_factory, category_factory, user_factory):
        user = user_factory()
        category = category_factory()
        product = product_factory(artisan=user, category=category, price=199.99)
        assert product.price == 199.99


class TestProductAttributeModel:
    def test_product_attribute_creation(self, product_factory, product_attribute_factory, category_factory, user_factory):
        user = user_factory()
        category = category_factory()
        product = product_factory(artisan=user, category=category)

        attribute = product_attribute_factory(product=product, field_name="Color", field_value="Red")
        assert attribute.product == product
        assert attribute.field_name == "Color"
        assert attribute.field_value == "Red"

    def test_product_attribute_field_value_length(self, product_factory, product_attribute_factory, category_factory, user_factory):
        user = user_factory()
        category = category_factory()
        product = product_factory(artisan=user, category=category)

        # Test with maximum length for `field_value`
        long_value = "A" * 200
        attribute = product_attribute_factory(product=product, field_name="Size", field_value=long_value)
        assert attribute.field_value == long_value

    # def test_product_attribute_with_invalid_field_value(self, product_factory, product_attribute_factory, category_factory, user_factory):
    #     user = user_factory()
    #     category = category_factory()
    #     product = product_factory(artisan=user, category=category)

    #     long_val = "A" * 300
    #     with pytest.raises(IntegrityError):
    #         product_attribute_factory(product=product, field_name="Color", field_value=long_val)
