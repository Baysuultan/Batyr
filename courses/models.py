from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
from django.utils.text import slugify
from django.conf import settings
from PIL import Image


class Course(models.Model):
    """Модель курса"""
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('published', 'Опубликован'),
        ('archived', 'Архивирован'),
    ]

    title = models.CharField(max_length=200, verbose_name='Название')
    slug = models.SlugField(unique=True, max_length=200)
    description = models.TextField(verbose_name='Описание')
    category = models.ForeignKey('categories.Category', on_delete=models.SET_NULL, 
                                 null=True, related_name='courses', verbose_name='Категория')
    instructor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                   related_name='courses_created', verbose_name='Инструктор')
    thumbnail = models.ImageField(upload_to='course_thumbnails/',
                                  validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])])
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                               validators=[MinValueValidator(0)], verbose_name='Цена')
    level = models.CharField(max_length=20, choices=[
        ('beginner', 'Начинающий'),
        ('intermediate', 'Средний'),
        ('advanced', 'Продвинутый'),
    ], default='beginner', verbose_name='Уровень')
    duration_hours = models.PositiveIntegerField(default=0, verbose_name='Длительность (часов)')
    students_count = models.PositiveIntegerField(default=0, editable=False, verbose_name='Количество студентов')
    rating = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)],
                              editable=False, verbose_name='Рейтинг')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name='Статус')
    
    tags = models.CharField(max_length=500, blank=True, default='', verbose_name='Теги')
    prerequisites = models.TextField(blank=True, default='', verbose_name='Предварительные знания')
    learning_outcomes = models.TextField(blank=True, default='', verbose_name='Результаты обучения')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['status']),
            models.Index(fields=['instructor']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        # Оптимизация изображения
        if self.thumbnail:
            try:
                img = Image.open(self.thumbnail.path)
                if img.height > 600 or img.width > 800:
                    img.thumbnail((800, 600))
                    img.save(self.thumbnail.path)
            except Exception:
                pass

    @property
    def total_lessons(self):
        return self.sections.aggregate(
            total=models.Count('lessons')
        )['total'] or 0
