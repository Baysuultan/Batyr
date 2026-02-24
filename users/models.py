from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from PIL import Image


class CustomUser(AbstractUser):
    """Пользовательская модель User с расширенными полями"""
    bio = models.TextField(blank=True, default='', max_length=500)
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])]
    )
    phone = models.CharField(max_length=20, blank=True, default='')
    country = models.CharField(max_length=100, blank=True, default='')
    is_instructor = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_full_name() or self.username}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Оптимизация изображения аватара
        if self.avatar:
            try:
                img = Image.open(self.avatar.path)
                if img.height > 300 or img.width > 300:
                    img.thumbnail((300, 300))
                    img.save(self.avatar.path)
            except Exception:
                pass
