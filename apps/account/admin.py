from django.contrib import admin
from django.contrib.auth.models import Group



from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from apps.account.forms import UserChangeForm, UserCreationForm
from apps.account.models import ArtisanProfile, Role, User, UserPreferences


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    add_form = UserCreationForm
    form = UserChangeForm
    model = User

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ["full_name", "email", "phone_number", "is_staff", "role"]
    list_filter = ["is_staff", "role"]
    fieldsets = [
        (None, {"fields": ["email", "phone_number", "password"]}),
        ("Personal info", {"fields": ["full_name"]}),
        (
            "Permissions",
            {"fields": ["is_staff", "state", "role"]},
        ),
        ("Important dates", {"fields": ["created_at", "updated_at", "deleted_at"]}),
    ]

    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": [
                    "full_name",
                    "email",
                    "phone_number",
                    "password1",
                    "password2",
                    "is_staff",
                    "state",
                    "role",
                ],
            },
        )
    ]

    search_fields = ["full_name", "email", "phone_number"]
    ordering = ["-created_at"]
    readonly_fields = ["created_at", "updated_at"]
    filter_horizontal = []


@admin.register(ArtisanProfile)
class ArtisanProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "shop_name", "location", "profile_picture", "bio"]
    list_filter = ["user"]
    fieldsets = [
        (None, {"fields": ["user", "shop_name", "profile_picture", "bio", "location"]})
    ]

    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields":  ["user", "shop_name", "location", "profile_picture", "bio"],
            },
        )
    ]

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    exclude = ["deleted_at"]


@admin.register(UserPreferences)
class UserPreferencesAdmin(admin.ModelAdmin):
    exclude = ["deleted_at"]


# since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
