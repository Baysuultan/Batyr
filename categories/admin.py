from django.contrib import admin
from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'created_at']
    list_filter = ['order', 'created_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'slug', 'icon', 'color', 'order')
        }),
        ('Описание', {
            'fields': ('description',)
        }),
    )
