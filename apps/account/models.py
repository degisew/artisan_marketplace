from apps.core.models import AbstractBaseModel, DataLookup
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.account.managers import UserManager
from django.utils import timezone


class Role(AbstractBaseModel):
    name = models.CharField(max_length=50, verbose_name=_("Name"))

    code = models.CharField(max_length=50, verbose_name=_("Code"))

    class Meta:
        verbose_name = _("Role")
        verbose_name_plural = _("Roles")
        db_table = "roles"
        constraints = [
            # Constraint: Unique code
            models.UniqueConstraint(fields=["code"], name="roles_code_idx"),
        ]

    def __str__(self) -> str:
        return self.name


class User(AbstractBaseUser, PermissionsMixin, AbstractBaseModel):
    full_name = models.CharField(max_length=50, verbose_name=_("Full Name"))

    email = models.EmailField(unique=True, max_length=50, verbose_name=_("Email"))

    phone_number = models.CharField(
        max_length=15, blank=True, verbose_name=_("Phone Number")
    )

    password = models.CharField(
        verbose_name=_("Password"),
        max_length=200
    )

    is_staff = models.BooleanField(default=False, verbose_name=_("Is Staff"))

    is_superuser = models.BooleanField(default=False, verbose_name=_("Is SuperUser"))

    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))

    is_profile_complete = models.BooleanField(
        verbose_name=_("Is Profile Complete"),
        default=False
    )

    date_joined = models.DateTimeField(default=timezone.now)

    # type = models.ForeignKey(
    #     DataLookup,
    #     on_delete=models.RESTRICT,
    #     null=True,
    #     blank=True,
    #     related_name="+",
    #     limit_choices_to={"type": "user_type"},
    # )

    role = models.ForeignKey(
        Role, null=True, blank=True, on_delete=models.RESTRICT, related_name="+"
    )

    state = models.ForeignKey(
        DataLookup,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        related_name="+",
        limit_choices_to={"type": "account_state"},
    )

    objects = UserManager()

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["full_name"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        ordering = ("-created_at",)
        db_table = "users"
        # constraints = [
        #     models.UniqueConstraint(
        #         fields=["email"],
        #         condition=(
        #             models.Q(email__isnull=False) | models.Q(deleted_at__isnull=True)
        #         ),
        #         name="users_email_idx",
        #     )
        # ]

    def __str__(self) -> str:
        return self.full_name

    def update_profile_status(self) -> None:
        self.is_profile_complete = True
        self.save()


class ArtisanProfile(AbstractBaseModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='artisan_profile',
        verbose_name=_("User")
    )

    bio = models.TextField(
        verbose_name=_("Bio"),
        blank=True,
        null=True
    )

    profile_picture = models.ImageField(
        verbose_name=_("Profile Picture"),
        upload_to='mediafiles/artisan_profiles/',
        blank=True,
        null=True
    )

    shop_name = models.CharField(
        verbose_name=_("Shop Name"),
        max_length=100
    )

    location = models.CharField(
        verbose_name=_("Location"),
        max_length=100
    )


class UserPreferences(AbstractBaseModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        related_name="preferences",
        related_query_name="preference",
    )

    notification_enabled = models.BooleanField(
        default=True, verbose_name=_("Notification Enabled")
    )

    class Meta:
        verbose_name = _("User Preference")
        verbose_name_plural = _("User Preferences")
        # ordering = ("-created_at",)
        db_table = "user_preferences"

    def __str__(self):
        return self.user.full_name
