from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from apps.account.models import Role
from apps.account.serializers import (
    PasswordChangeSerializer,
    RoleSerializer,
    UserSerializer
)

from apps.core.views import AbstractModelViewSet


User = get_user_model()


class RoleViewSet(AbstractModelViewSet):
    permission_classes = [AllowAny]
    http_method_names = ["get"]
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class UserViewSet(AbstractModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
    queryset = User.objects.all()


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
