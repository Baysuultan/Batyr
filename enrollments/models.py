from django.db import models
from django.conf import settings


class Enrollment(models.Model):
    """Запись пользователя на курс"""
    STATUS_CHOICES = [
        ('active', 'Активная'),
        ('completed', 'Завершена'),
        ('cancelled', 'Отменена'),
    ]

    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                               related_name='enrollments', verbose_name='Студент')
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE,
                              related_name='enrollments', verbose_name='Курс')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active',
                             verbose_name='Статус')
    progress = models.FloatField(default=0, verbose_name='Прогресс (%)')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name='Завершено')
    last_accessed = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'
        ordering = ['-enrolled_at']
        unique_together = ['student', 'course']

    def __str__(self):
        return f"{self.student.username} -> {self.course.title}"


class LessonProgress(models.Model):
    """Прогресс по урокам"""
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE,
                                  related_name='lesson_progress', verbose_name='Запись')
    lesson = models.ForeignKey('lessons.Lesson', on_delete=models.CASCADE,
                              verbose_name='Урок')
    is_completed = models.BooleanField(default=False, verbose_name='Завершен')
    watched_seconds = models.PositiveIntegerField(default=0, verbose_name='Просмотрено (сек)')
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Прогресс урока'
        verbose_name_plural = 'Прогресс уроков'
        unique_together = ['enrollment', 'lesson']

    def __str__(self):
        return f"{self.enrollment.student.username} - {self.lesson.title}"
