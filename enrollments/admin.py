from django.contrib import admin
from .models import Enrollment, LessonProgress


class LessonProgressInline(admin.TabularInline):
    model = LessonProgress
    extra = 0
    readonly_fields = ['lesson', 'completed_at', 'created_at']
    can_delete = False


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'status', 'progress', 'enrolled_at']
    list_filter = ['status', 'enrolled_at']
    search_fields = ['student__username', 'course__title']
    readonly_fields = ['enrolled_at', 'last_accessed', 'completed_at']
    inlines = [LessonProgressInline]


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ['enrollment', 'lesson', 'is_completed', 'created_at']
    list_filter = ['is_completed', 'created_at']
    search_fields = ['enrollment__student__username', 'lesson__title']
    readonly_fields = ['created_at', 'completed_at']
