from apps.core.views import AbstractModelViewSet
from rest_framework.viewsets import GenericViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.mixins import (
    CreateModelMixin
)
from apps.store.models import (
    Product,
    Category,
    CategoryAttribute
)
from apps.store.filters import (
    CategoryFilter,
    CategoryAttributeFilter,
    ProductFilter,
)
from apps.store.permissions import (
    CategoryAccessPolicy,
    CategoryAttributeAccessPolicy,
    ProductAccessPolicy
)
from apps.store.serializers import (
    CategoryResponseSerializer,
    ProductResponseSerializer,
    ProductCreationSerializer,
    CategoryAttributeResponseSerializer
)


class CategoryViewSet(AbstractModelViewSet):
    permission_classes = [CategoryAccessPolicy]
    http_method_names = ["get"]
    filter_backends = [DjangoFilterBackend]
    filterset_class = CategoryFilter
    serializer_class = CategoryResponseSerializer
    queryset = Category.objects.all()


class CategoryAttributeViewSet(AbstractModelViewSet):
    permission_classes = [CategoryAttributeAccessPolicy]
    http_method_names = ["get"]
    filter_backends = [DjangoFilterBackend]
    filterset_class = CategoryAttributeFilter
    serializer_class = CategoryAttributeResponseSerializer
    queryset = CategoryAttribute.objects.all()


class ProductViewSet(AbstractModelViewSet):
    permission_classes = [ProductAccessPolicy]
    serializer_class = ProductResponseSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter
    http_method_names = ["get", "patch", "delete"]
    queryset = Product.objects.all()


class CreateProductViewSet(CreateModelMixin, GenericViewSet):
    permission_classes = [ProductAccessPolicy]
    serializer_class = ProductCreationSerializer
    queryset = None
