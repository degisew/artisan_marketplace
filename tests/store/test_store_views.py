import pytest
from rest_framework import status


pytestmark = pytest.mark.django_db


@pytest.mark.django_db
class TestCategoryViewSet:
    @pytest.fixture(autouse=True)
    def setup(self, api_client, user_factory):
        self.client = api_client
        self.user = user_factory(password="password123")
        self.user.save()

        self.url = "/api/v1/store/categories/"

    def test_access_policy_with_allowed_users(self, category_factory, role_factory):
        self.user.role = role_factory(name="Artisan", code="artisan")
        self.user.save()

        self.client.force_authenticate(user=self.user)
        category_factory()

        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) > 0

    def test_access_policy_with_disallowed_users(self, category_factory, role_factory):
        self.user.save()
        # assign normal user role
        self.user.role = role_factory(name="abcd", code="abcd")

        self.client.force_authenticate(user=self.user)
        category_factory()

        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_unauthenticated(self):
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
