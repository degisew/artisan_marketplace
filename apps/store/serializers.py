from typing import Any
from django.contrib.auth import get_user_model
from rest_framework import serializers
from apps.account.serializers import UserSerializer
from apps.core.models import DataLookup
from apps.core.serializers import DataLookupSerializer, DataTypeFormTypeResponseSerializer
from apps.store.models import (
    Product,
    ProductAttribute,
    Category,
    CategoryAttribute
)
from apps.store.services import PriceSetService


User = get_user_model()


class CategoryResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'slug'
        ]


class CategoryAttributeResponseSerializer(serializers.ModelSerializer):
    field_type = DataTypeFormTypeResponseSerializer()
    form_type = DataTypeFormTypeResponseSerializer()

    class Meta:
        model = CategoryAttribute
        fields = [
            'id',
            'field_name',
            'field_type',
            'form_type',
            'required'
        ]


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all()
    )

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'category',
            'material',
            'description',
            'quantity',
            'available_colors',
            'price'
        ]


class ProductCreationSerializer(serializers.Serializer):
    product = ProductSerializer()
    attributes = serializers.DictField(
        child=serializers.JSONField()
    )

    def create(self, validated_data) -> dict[str, Any]:
        user = self.context["request"].user
        validated_data["product"]["artisan"] = user
        try:
            return PriceSetService.create_product(validated_data)
        except Exception as e:
            raise e

    def to_representation(self, instance) -> dict[Any, Any]:
        representation = super().to_representation(instance)
        product = representation.pop("product")
        attributes = representation.pop("attributes")

        return {
            **product,
            **attributes
        }


class ProductAttributeResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = [
            'id',
            'field_name',
            'field_value',
        ]


class ProductResponseSerializer(serializers.ModelSerializer):
    category = CategoryResponseSerializer()
    artisan = UserSerializer()
    available_colors = DataLookupSerializer(many=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'artisan',
            'category',
            'material',
            'description',
            'quantity',
            'available_colors',
            'price',
        ]
