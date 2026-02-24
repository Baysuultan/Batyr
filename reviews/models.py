from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings


class Review(models.Model):
    """Отзыв к курсу"""
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE,
                              related_name='reviews', verbose_name='Курс')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                              related_name='reviews', verbose_name='Автор')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)],
                                verbose_name='Рейтинг')
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    comment = models.TextField(verbose_name='Комментарий')
    is_verified = models.BooleanField(default=False, verbose_name='Проверенная покупка')
    helpful_count = models.PositiveIntegerField(default=0, editable=False, verbose_name='Полезные голосы')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']
        unique_together = ['course', 'author']

    def __str__(self):
        return f"{self.author.username} - {self.course.title} ({self.rating}⭐)"
