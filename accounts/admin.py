from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        ('Основные данные', {'fields': ('username', 'slug_username', 'first_name', 'password', 'authenticated')}),
        ('Личные данные', {'fields': ('pic', 'bio')})
    )