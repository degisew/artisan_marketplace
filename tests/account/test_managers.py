import pytest
from django.contrib.auth import get_user_model
from conftest import SuperUserFactory, UserFactory

User = get_user_model()


@pytest.mark.django_db
def test_user_creation(user_factory) -> None:
    with pytest.raises(ValueError, match="The Email must be set"):
        UserFactory(email="", password="userpassword")
    user = user_factory()
    assert '@' in user.email
    assert not user.is_staff
    assert not user.is_superuser
    # assert user_factory.check_password("userpassword")


@pytest.mark.django_db
def test_super_user_creation(admin_user) -> None:
    admin = admin_user()
    assert '@' in admin.email
    # assert admin_user.check_password("adminpassword")
    assert admin.is_staff
    assert admin.is_superuser

    with pytest.raises(ValueError, match="Superuser must have is_staff=True."):
        SuperUserFactory(password="adminpassword", is_staff=False)

    with pytest.raises(ValueError, match="Superuser must have is_superuser=True."):
        SuperUserFactory(password="adminpassword", is_superuser=False)
