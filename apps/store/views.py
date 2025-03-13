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
from apps.store.filters import CategoryAttributeFilter, ProductFilter
from rest_framework.permissions import AllowAny
from apps.store.serializers import (
    CategoryResponseSerializer,
    ProductResponseSerializer,
    ProductCreationSerializer,
    CategoryAttributeResponseSerializer
)


class CategoryViewSet(AbstractModelViewSet):
    permission_classes = [AllowAny]
    http_method_names = ["get"]
    serializer_class = CategoryResponseSerializer
    queryset = Category.objects.all()


class CategoryAttributeViewSet(AbstractModelViewSet):
    permission_classes = [AllowAny]
    http_method_names = ["get"]
    filter_backends = [DjangoFilterBackend]
    filterset_class = CategoryAttributeFilter
    serializer_class = CategoryAttributeResponseSerializer
    queryset = CategoryAttribute.objects.all()


class ProductViewSet(AbstractModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = ProductResponseSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter
    http_method_names = ["get", "patch", "delete"]
    queryset = Product.objects.all()


class CreateProductViewSet(CreateModelMixin, GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = ProductCreationSerializer
    queryset = None
