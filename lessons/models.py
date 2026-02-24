from django.db import models
from django.utils.text import slugify
from django.core.validators import URLValidator


class Section(models.Model):
    """Раздел курса"""
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE,
                              related_name='sections', verbose_name='Курс')
    title = models.CharField(max_length=200, verbose_name='Название раздела')
    description = models.TextField(blank=True, default='', verbose_name='Описание')
    order = models.PositiveIntegerField(verbose_name='Порядок')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'
        ordering = ['order']
        unique_together = ['course', 'order']

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Lesson(models.Model):
    """Урок в курсе"""
    section = models.ForeignKey(Section, on_delete=models.CASCADE,
                               related_name='lessons', verbose_name='Раздел')
    title = models.CharField(max_length=200, verbose_name='Название урока')
    slug = models.SlugField(unique=True, max_length=200)
    description = models.TextField(verbose_name='Описание')
    content = models.TextField(blank=True, default='', verbose_name='Содержание (Markdown)')
    video_url = models.URLField(blank=True, default='', verbose_name='Ссылка на видео')
    resources = models.TextField(blank=True, default='', verbose_name='Ресурсы (ссылки)')
    duration_minutes = models.PositiveIntegerField(default=0, verbose_name='Длительность (минут)')
    order = models.PositiveIntegerField(verbose_name='Порядок в разделе')
    is_free = models.BooleanField(default=False, verbose_name='Бесплатный урок')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ['section', 'order']
        unique_together = ['section', 'order']

    def __str__(self):
        return f"{self.section.course.title} - {self.title}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
