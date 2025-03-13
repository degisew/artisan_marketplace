from rest_framework.routers import DefaultRouter
from apps.store.views import (
    CategoryAttributeViewSet,
    ProductViewSet,
    CreateProductViewSet,
    CategoryViewSet
)

router = DefaultRouter()


router.register('products', ProductViewSet, 'products')
router.register('form-metadata', CategoryAttributeViewSet, 'form-metadata')
router.register('create-product', CreateProductViewSet, 'create-product')
router.register('categories', CategoryViewSet, 'categories')

urlpatterns = router.urls
