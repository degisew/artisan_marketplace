import pytest
from django.db.utils import IntegrityError

pytestmark = pytest.mark.django_db


class TestRoleModel:
    def test_role_creation(self, role_factory):
        role = role_factory()
        assert role.name == "Admin"
        assert role.code == "admin"

    def test_role_str(self, role_factory):
        role = role_factory()
        assert str(role) == "Admin"

    def test_unique_role_code(self, role_factory):
        role_factory()
        with pytest.raises(IntegrityError):
            role_factory(code="admin")
