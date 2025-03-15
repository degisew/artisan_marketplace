
from django_filters import FilterSet
from django_filters import rest_framework as filters

from apps.store.models import Category, Product, CategoryAttribute


class CategoryFilter(FilterSet):
    name = filters.CharFilter(field_name='name')

    class Meta:
        model = Category
        fields = []


class CategoryAttributeFilter(FilterSet):
    category = filters.UUIDFilter(field_name='category')

    class Meta:
        model = CategoryAttribute
        fields = ["category"]


class ProductFilter(FilterSet):
    category = filters.UUIDFilter(field_name='category')

    class Meta:
        model = Product
        fields = ["category"]
