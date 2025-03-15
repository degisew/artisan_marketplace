from rest_framework import routers

from apps.core.views import (
    DataLookupTypeViewSet,
    DataLookupViewSet,
    SystemSettingViewSet,
)

router = routers.DefaultRouter(trailing_slash=False)

router.register("data-lookups", DataLookupViewSet, basename="data-lookups")
router.register("lookup-types", DataLookupTypeViewSet, basename="lookup-types")
router.register(
    "system-settings", SystemSettingViewSet, basename="system-settings"
)


urlpatterns = router.urls
