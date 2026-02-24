from django.contrib import admin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_instructor', 'created_at']
    list_filter = ['is_instructor', 'is_staff', 'created_at']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Личная информация', {'fields': ('first_name', 'last_name', 'email', 'bio', 'avatar', 'phone', 'country')}),
        ('Разрешения', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_instructor', 'groups', 'user_permissions')}),
        ('Даты', {'fields': ('last_login', 'created_at', 'updated_at')}),
    )
    readonly_fields = ['created_at', 'updated_at']
