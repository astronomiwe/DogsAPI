from django.contrib import admin
from django.contrib.admin import ModelAdmin
from accounts.models import User


@admin.register(User)
class UserAdmin(ModelAdmin):
    fields = ('email', 'is_active', 'is_staff', 'is_superuser', 'avatar',
              'created_at', 'last_login')
    list_display = ('id', 'email', 'is_active', 'is_staff', 'is_superuser')
    readonly_fields = ('created_at', 'last_login')
