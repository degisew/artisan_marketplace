from django.contrib.auth import get_user_model
from rest_framework import serializers
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


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'name',
            'value',
            'slug'
        ]


class CategoryAttributeResponseSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    field_type = DataTypeFormTypeResponseSerializer()
    form_type = DataTypeFormTypeResponseSerializer()

    class Meta:
        model = CategoryAttribute
        fields = [
            'id',
            'category',
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


class ProductPriceSetSerializer(serializers.Serializer):
    product = ProductSerializer()
    # category = serializers.PrimaryKeyRelatedField(
    #     queryset=Category.objects.all()
    # )

    # available_colors = serializers.PrimaryKeyRelatedField(
    #     queryset=DataLookup.objects.filter(
    #         type="product_color_type"
    #     )
    # )

    # name = serializers.CharField()

    # price = serializers.DecimalField(max_digits=10, decimal_places=2)

    # quantity = serializers.IntegerField()

    # material = serializers.CharField()

    # description = serializers.CharField()

    attributes = serializers.DictField(
        child=serializers.JSONField()
    )

    # def validate(self, attrs):

    def create(self, validated_data):
        return PriceSetService.create_product(validated_data)


class ProductAttributeResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = [
            'id',
            'field_name',
            'field_value',
        ]


class ProductResponseSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

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
