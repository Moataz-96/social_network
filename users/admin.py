# users/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.forms import CustomUserCreationForm, CustomUserChangeForm
from users.models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [
        "id",
        "email",
        "username",
        "gender",
        "age",
    ]
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("gender", "age")}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("gender", "age")}),)


admin.site.register(CustomUser, CustomUserAdmin)
