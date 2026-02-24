from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'notifications_enabled', 'newsletter_subscribed', 'theme']
    list_filter = ['notifications_enabled', 'newsletter_subscribed', 'theme']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['courses_completed', 'certificates_earned', 'updated_at']
