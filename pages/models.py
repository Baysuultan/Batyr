from django.db import models
from django.utils.text import slugify


class StaticPage(models.Model):
    """Статические страницы (О проекте, Условия, etc)"""
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    slug = models.SlugField(unique=True, max_length=200)
    content = models.TextField(verbose_name='Содержание')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Статическая страница'
        verbose_name_plural = 'Статические страницы'
        ordering = ['order']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class ContactMessage(models.Model):
    """Сообщение с формы контакта"""
    name = models.CharField(max_length=200, verbose_name='Имя')
    email = models.EmailField(verbose_name='Email')
    subject = models.CharField(max_length=200, verbose_name='Тема')
    message = models.TextField(verbose_name='Сообщение')
    is_replied = models.BooleanField(default=False, verbose_name='Ответ отправлен')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Сообщение контакта'
        verbose_name_plural = 'Сообщения контактов'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject}"
