from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets, status
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from apps.account.models import ArtisanProfile, Role
from apps.account.permissions import RoleAccessPolicy, UserAccessPolicy
from apps.account.serializers import (
    ArtisanProfileResponseSerializer,
    PasswordChangeSerializer,
    RoleSerializer,
    UserResponseSerializer,
    UserSerializer,
    ArtisanProfileSerializer
)

from apps.core.views import AbstractModelViewSet


User = get_user_model()


class RoleViewSet(AbstractModelViewSet):
    permission_classes = [RoleAccessPolicy]
    http_method_names = ["get"]
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class UserViewSet(AbstractModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    @extend_schema(
        responses=ArtisanProfileResponseSerializer
    )
    @action(detail=False, url_path="profile")
    def get_profile(self, request) -> Response:
        profile = ArtisanProfile.objects.get(
            user=request.user
        )
        serialized_data = ArtisanProfileSerializer(profile).data
        user = serialized_data.pop("user")
        response = {**serialized_data, **user}
        return Response(
            response,
            status=status.HTTP_200_OK
        )


class PasswordChangeViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PasswordChangeSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # Generate a new JWT token
        refresh = RefreshToken.for_user(request.user)
        return Response({
            "message": "Password changed successfully",
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }, status=status.HTTP_200_OK)
