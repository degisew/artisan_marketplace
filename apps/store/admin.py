from django.contrib import admin
from apps.store.models import (
    Product,
    ProductAttribute,
    Category,
    CategoryAttribute

)


@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    exclude = ["deleted_at"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    exclude = ["deleted_at"]


@admin.register(CategoryAttribute)
class ProductCategoryAttributeAdmin(admin.ModelAdmin):
    exclude = ["deleted_at"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "slug",
        "name"
    )
    prepopulated_fields = {"slug": ("name",)}
    exclude = ["deleted_at"]
