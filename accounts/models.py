from django.db import models
from django.conf import settings


class UserProfile(models.Model):
    """Расширенный профиль пользователя"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                               related_name='profile', verbose_name='Пользователь')
    
    # Закладки и избранное
    favorite_courses = models.ManyToManyField('courses.Course', related_name='favorited_by',
                                             blank=True, verbose_name='Избранные курсы')
    
    # Настройки
    notifications_enabled = models.BooleanField(default=True, verbose_name='Уведомления включены')
    newsletter_subscribed = models.BooleanField(default=True, verbose_name='Подписка на рассылку')
    theme = models.CharField(max_length=10, choices=[('light', 'Светлая'), ('dark', 'Тёмная')],
                            default='light', verbose_name='Тема')
    
    # Статистика
    courses_completed = models.PositiveIntegerField(default=0, editable=False,
                                                   verbose_name='Завершено курсов')
    certificates_earned = models.PositiveIntegerField(default=0, editable=False,
                                                     verbose_name='Сертификатов получено')
    
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return f"Профиль {self.user.username}"
