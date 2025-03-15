from faker import Faker
import pytest
import factory
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify
from apps.core.models import DataLookup, SystemSetting

from apps.account.models import Role
from apps.store.models import (
    Category,
    CategoryAttribute,
    Product,
    ProductAttribute
)


User = get_user_model()


fake = Faker()


class RoleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Role

    name = "Admin"
    code = "admin"

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Forcing factory boy to use managers create method."""
        return model_class.objects.create(*args, **kwargs)


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        skip_postgeneration_save = True  # Prevents unnecessary save()

    email = factory.Faker("email")
    password = factory.PostGenerationMethodCall("set_password", "password123")

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Ensures the manager's create_user method is used."""
        password = kwargs.pop("password", "defaultpassword")
        return model_class.objects.create_user(password=password, *args, **kwargs)


class SuperUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        skip_postgeneration_save = True  # Prevents unnecessary save()

    email = 'admin@gmail.com'
    password = factory.PostGenerationMethodCall("set_password", "1234")
    is_staff = True
    is_superuser = True

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Ensures create_superuser() is used, triggering validation."""
        password = kwargs.pop("password", "adminpassword")
        return model_class.objects.create_superuser(password=password, *args, **kwargs)


class DataLookupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DataLookup

    type = factory.LazyAttribute(lambda _: fake.word())
    name = factory.LazyAttribute(lambda _: fake.word())
    value = factory.Sequence(lambda n: f"value_{n}")
    category = factory.LazyAttribute(lambda _: fake.word())
    description = factory.Faker("sentence")
    index = factory.Sequence(lambda n: n)
    is_default = False
    is_active = True
    remark = factory.Faker("sentence")


class SystemSettingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SystemSetting

    name = factory.LazyAttribute(lambda _: fake.word())
    key = factory.LazyAttribute(lambda _: fake.unique.word())
    default_value = factory.LazyAttribute(lambda _: fake.word())
    current_value = factory.LazyAttribute(lambda _: fake.word())
    data_type = factory.SubFactory(DataLookupFactory)


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.LazyAttribute(lambda _: fake.word())
    slug = factory.LazyAttribute(lambda obj: slugify(obj.name))


class CategoryAttributeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CategoryAttribute

    category = factory.SubFactory(CategoryFactory)
    field_name = factory.LazyAttribute(lambda _: fake.word())
    field_type = factory.SubFactory(DataLookupFactory)


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.LazyAttribute(lambda _: fake.word())
    artisan = factory.SubFactory(
        UserFactory
    )  # Assuming a User factory is defined
    category = factory.SubFactory("your_app.factories.CategoryFactory")
    description = factory.LazyAttribute(lambda _: fake.text())
    quantity = factory.LazyAttribute(lambda _: fake.random_int(min=1, max=100))
    price = factory.LazyAttribute(lambda _: fake.random_number(digits=5))


class ProductAttributeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductAttribute

    field_name = factory.LazyAttribute(lambda _: fake.word())
    field_value = factory.LazyAttribute(lambda _: fake.word())
    product = factory.SubFactory(ProductFactory)


@pytest.fixture
def api_client() -> APIClient:
    """Returns an APIClient instance."""
    return APIClient()


@pytest.fixture
def user_factory(db):
    """Creates and returns a regular user."""
    # return UserFactory(password="userpassword")
    return UserFactory


@pytest.fixture
def admin_user(db):
    """Creates and returns a superuser."""
    # return SuperUserFactory(password="adminpassword")
    return SuperUserFactory


@pytest.fixture
def authenticated_client(api_client, user_factory):
    """Creates an authenticated user and logs them in."""
    user = user_factory(password="password123")  # Uses your UserFactory
    api_client.force_authenticate(user=user)
    return api_client, user


@pytest.fixture
def role_factory(db):
    return RoleFactory


@pytest.fixture
def category_factory(db):
    return CategoryFactory


@pytest.fixture
def category_attribute_factory(db):
    return CategoryAttributeFactory


@pytest.fixture
def product_factory(db):
    return ProductFactory


@pytest.fixture
def product_attribute_factory(db):
    return ProductAttributeFactory


@pytest.fixture
def data_lookup_factory(db):
    return DataLookupFactory


@pytest.fixture
def system_setting_factory(db):
    return SystemSettingFactory
