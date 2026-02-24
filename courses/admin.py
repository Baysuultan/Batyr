from django.contrib import admin
from .models import Course


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'instructor', 'category', 'status', 'price', 'rating', 'created_at']
    list_filter = ['status', 'category', 'level', 'created_at']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['students_count', 'rating', 'created_at', 'updated_at', 'total_lessons']
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'slug', 'category', 'instructor', 'status')
        }),
        ('Описание и содержание', {
            'fields': ('description', 'thumbnail', 'level', 'duration_hours', 'prerequisites', 'learning_outcomes', 'tags')
        }),
        ('Цена и рейтинг', {
            'fields': ('price', 'rating', 'students_count')
        }),
        ('Статистика', {
            'fields': ('created_at', 'updated_at', 'total_lessons'),
            'classes': ('collapse',)
        }),
    )
    
    def total_lessons(self, obj):
        return obj.total_lessons
    total_lessons.short_description = 'Всего уроков'
