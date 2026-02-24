#!/usr/bin/env python
"""
Исправление слагов уроков
"""
import os
import django
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coursehub.settings')
django.setup()

from lessons.models import Lesson

print("🔧 Исправление слагов уроков...\n")

for lesson in Lesson.objects.all():
    if not lesson.slug or lesson.slug.strip() == '':
        old_slug = lesson.slug
        new_slug = slugify(lesson.title)
        
        # Проверяем уникальность
        counter = 1
        original_slug = new_slug
        while Lesson.objects.filter(slug=new_slug).exclude(id=lesson.id).exists():
            new_slug = f"{original_slug}-{counter}"
            counter += 1
        
        lesson.slug = new_slug
        lesson.save()
        print(f"✅ {lesson.title}: '{old_slug}' -> '{new_slug}'")

print("\n✅ Готово!")

# Проверяем
print("\n📋 Окончательный список уроков:\n")
for lesson in Lesson.objects.all():
    print(f"• {lesson.title}")
    print(f"  📺 Видео: {lesson.video_url}")
    print(f"  🔗 URL: /courses/{lesson.section.course.slug}/lessons/{lesson.slug}/")
    print()
