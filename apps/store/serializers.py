from django.contrib.auth import get_user_model
from rest_framework import serializers
from apps.account.serializers import UserSerializer
from apps.core.models import DataLookup
from apps.core.serializers import DataTypeFormTypeResponseSerializer
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

    available_colors = serializers.PrimaryKeyRelatedField(
        queryset=DataLookup.objects.filter(
            type="product_color_type"
        )
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

    def create(self, validated_data):
        user = self.context["request"].user
        return PriceSetService.create_product(user, validated_data)

    def to_representation(self, instance):
        product = instance.get("product")
        attributes = instance.get("attributes")

        product_data = ProductResponseSerializer(product).data

        return {
            **product_data,
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
