from rest_framework.routers import DefaultRouter
from apps.account.views import (
    RoleViewSet,
    UserViewSet,
    PasswordChangeViewSet
)

router = DefaultRouter()

router.register('roles', RoleViewSet, basename='roles')
router.register('users', UserViewSet, 'users')
router.register('change-password', PasswordChangeViewSet, 'change-password')

urlpatterns = router.urls
