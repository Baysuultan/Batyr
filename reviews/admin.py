from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['author', 'course', 'rating', 'is_verified', 'created_at']
    list_filter = ['rating', 'is_verified', 'created_at']
    search_fields = ['author__username', 'course__title']
    readonly_fields = ['helpful_count', 'created_at', 'updated_at']
    fieldsets = (
        ('Информация о отзыве', {
            'fields': ('course', 'author', 'rating', 'title')
        }),
        ('Содержание', {
            'fields': ('comment',)
        }),
        ('Статистика', {
            'fields': ('is_verified', 'helpful_count', 'created_at', 'updated_at')
        }),
    )
