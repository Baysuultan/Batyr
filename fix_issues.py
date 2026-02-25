#!/usr/bin/env python
"""
Исправление найденных проблем
"""
import os
import django
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coursehub.settings')
django.setup()

from lessons.models import Lesson

print("=" * 80)
print("🔧 ИСПРАВЛЕНИЕ ПРОБЛЕМ")
print("=" * 80)
print()

# Исправляем ВСЕ уроки - переставляем слаги с нуля
print("1️⃣  Исправление всех слагов уроков...")

fixed_count = 0
for lesson in Lesson.objects.all():
    old_slug = lesson.slug
    base_slug = slugify(lesson.title)
    
    # Проверяем если слаг уже существует
    if not base_slug or (base_slug and base_slug[0].isdigit()) or (base_slug and base_slug.startswith('-')):
        # Попытаемся улучшить
        base_slug = f"lesson-{lesson.id}"
    
    counter = 1
    unique_slug = base_slug
    
    # Ищем уникальный слаг
    while Lesson.objects.filter(slug=unique_slug).exclude(id=lesson.id).exists():
        unique_slug = f"{base_slug}-{counter}"
        counter += 1
    
    if old_slug != unique_slug:
        lesson.slug = unique_slug
        lesson.save()
        print(f"  ✅ {lesson.title:50} (был: '{old_slug}' -> стал: '{unique_slug}')")
        fixed_count += 1
    else:
        print(f"  ✓ {lesson.title:50} - OK")

print()
print(f"✅ Исправлено: {fixed_count} уроков")
print()
print("=" * 80)
print("✅ ПРОБЛЕМЫ ИСПРАВЛЕНЫ!")
print("=" * 80)
print()

# Выводим все уроки и их слаги для проверки
print("📋 Все уроки и их URL (проверка):")
for course in __import__('courses.models', fromlist=['Course']).Course.objects.all():
    print(f"\n📚 {course.title}:")
    for section in course.sections.all():
        for lesson in section.lessons.all():
            url = f"/courses/{course.slug}/lessons/{lesson.slug}/"
            status = "✅" if lesson.slug and not lesson.slug.startswith('-') and lesson.slug != '' else "❌"
            print(f"  {status} {lesson.title:50} -> {url}")
