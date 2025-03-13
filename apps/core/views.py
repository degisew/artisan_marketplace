from rest_framework import viewsets
from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticated
)

from apps.core.models import DataLookup, SystemSetting
from apps.core.serializers import (
    DataLookupSerializer,
    DataLookupTypeSerializer,
    SystemSettingSerializer
)


# Base ViewSet
class AbstractModelViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]

    # def destroy(self, request, *args, **kwargs):
    #     """
    #     Soft delete data records.
    #     """

    #     instance = self.get_object()
    #     instance.object_state = DataLookup.objects.get(
    #         value=ObjectStateType.DELETED.value
    #     )
    #     instance.deleted_at = timezone.now()
    #     instance.save()

    #     return Response(status=status.HTTP_204_NO_CONTENT)


class DataLookupViewSet(AbstractModelViewSet):
    permission_classes = [AllowAny]
    http_method_names = ["get"]
    serializer_class = DataLookupSerializer
    queryset = DataLookup.objects.all()


# @extend_schema(tags=["Data Lookup"], request=DataLookupTypeSerializer)
class DataLookupTypeViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminUser]
    pagination_class = None
    queryset = DataLookup.objects.all().distinct("type").order_by("type")
    serializer_class = DataLookupTypeSerializer


class SystemSettingViewSet(AbstractModelViewSet):
    permission_classes = [AllowAny]
    http_method_names = ["get"]
    serializer_class = SystemSettingSerializer
    queryset = SystemSetting.objects.all()
