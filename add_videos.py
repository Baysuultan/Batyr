#!/usr/bin/env python
"""
Скрипт для добавления YouTube видео в уроки
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coursehub.settings')
django.setup()

from lessons.models import Lesson

# YouTube видео ссылки
videos = [
    'https://youtu.be/34Rp6KVGIEM?si=XZDcvf098o3pP6cM',
    'https://youtu.be/5l9nxwh5Wiw?si=xMJS0tz1TlDOqcis',
    'https://youtu.be/aO4Mnz485uM?si=n2MjelLTVMXlyRGj',
    'https://youtu.be/eMhhl1Wq8JA?si=ULV9AANYOy2PjEIP',
]

# Конвертируем YouTube ссылки в embed формат
def convert_to_embed(youtube_url):
    """Конвертирует YouTube ссылку в embed версию"""
    if 'youtu.be' in youtube_url:
        video_id = youtube_url.split('/')[-1].split('?')[0]
        return f'https://www.youtube.com/embed/{video_id}'
    elif 'youtube.com' in youtube_url:
        video_id = youtube_url.split('v=')[1].split('&')[0]
        return f'https://www.youtube.com/embed/{video_id}'
    return youtube_url

# Получаем все уроки и добавляем видео
lessons = Lesson.objects.all().order_by('id')
print(f"Всего уроков: {lessons.count()}")
print()

# Если уроков меньше 4, создаём их
for idx, video_url in enumerate(videos, 1):
    embed_url = convert_to_embed(video_url)
    
    # Находим или создаём урок
    try:
        lesson = Lesson.objects.all()[idx - 1]
        lesson.video_url = embed_url
        lesson.duration_minutes = 15 + idx * 5  # Примерная длительность
        lesson.save()
        print(f"✅ Урок {idx}: {lesson.title}")
        print(f"   Видео: {embed_url[:60]}...")
        print()
    except IndexError:
        print(f"⚠️  Урок {idx} не найден")

print("✅ Все видео успешно добавлены!")
