from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    """Категория курсов"""
    name = models.CharField(max_length=150, unique=True, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    slug = models.SlugField(unique=True, max_length=150)
    icon = models.CharField(max_length=50, default='book', verbose_name='Иконка')
    color = models.CharField(max_length=7, default='#3498db', verbose_name='Цвет')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
