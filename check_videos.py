#!/usr/bin/env python
"""
Проверка видео в БД
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coursehub.settings')
django.setup()

from lessons.models import Lesson

print("=" * 80)
print("📹 ПРОВЕРКА ВИДЕО В УРОКАХ")
print("=" * 80)

lessons = Lesson.objects.filter(video_url__isnull=False, video_url__gt='')

if not lessons:
    print("⚠️  Нет уроков с видео")
else:
    print(f"\n✅ Найдено {lessons.count()} уроков с видео:\n")
    
    for idx, lesson in enumerate(lessons, 1):
        print(f"{idx}. {lesson.section.course.title} > {lesson.section.title} > {lesson.title}")
        print(f"   📺 {lesson.video_url}")
        print(f"   ⏱️  Длительность: {lesson.duration_minutes} минут")
        print()

print("=" * 80)
print(f"📊 Статистика:")
print(f"   • Всего уроков: {Lesson.objects.count()}")
print(f"   • Уроков с видео: {lessons.count()}")
print(f"   • Уроков без видео: {Lesson.objects.exclude(video_url__isnull=False, video_url__gt='').count()}")
print("=" * 80)
