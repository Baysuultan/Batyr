from django.db import models
from django.conf import settings


class Notification(models.Model):
    """Уведомление пользователю"""
    TYPES = [
        ('course_update', 'Обновление курса'),
        ('new_course', 'Новый курс'),
        ('enrollment_confirmation', 'Подтверждение записи'),
        ('completion', 'Завершение курса'),
        ('message', 'Сообщение'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                            related_name='notifications', verbose_name='Пользователь')
    notification_type = models.CharField(max_length=50, choices=TYPES,
                                         verbose_name='Тип уведомления')
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    message = models.TextField(verbose_name='Сообщение')
    is_read = models.BooleanField(default=False, verbose_name='Прочитано')
    link = models.URLField(blank=True, default='', verbose_name='Ссылка')
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.title}"
