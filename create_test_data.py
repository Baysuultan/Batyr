#!/usr/bin/env python
"""
Скрипт для создания тестовых данных (курсы, секции, уроки)
"""
import os
import django
from django.utils.text import slugify

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coursehub.settings')
django.setup()

from courses.models import Course
from lessons.models import Section, Lesson
from users.models import CustomUser

# YouTube видео ссылки (embed версии)
videos = [
    'https://www.youtube.com/embed/34Rp6KVGIEM',
    'https://www.youtube.com/embed/5l9nxwh5Wiw',
    'https://www.youtube.com/embed/aO4Mnz485uM',
    'https://www.youtube.com/embed/eMhhl1Wq8JA',
]

# Создаём инструктора если его нет
instructor, created = CustomUser.objects.get_or_create(
    username='instructor1',
    defaults={
        'first_name': 'Демиян',
        'last_name': 'Инструктор',
        'email': 'instructor@coursehub.kz',
        'is_staff': False
    }
)
if created:
    print(f"✅ Инструктор создан: {instructor.first_name} {instructor.last_name}")
else:
    print(f"📦 Инструктор уже существует: {instructor.first_name}")

# Создаём курс
course, created = Course.objects.get_or_create(
    slug='django-basics',
    defaults={
        'title': 'Django Основы',
        'description': 'Полный курс по изучению Django',
        'level': 'beginner',
        'price': 99.99,
        'instructor': instructor,
        'status': 'published',
        'thumbnail': '',
    }
)
if created:
    print(f"✅ Курс создан: {course.title}")
else:
    print(f"📦 Курс уже существует: {course.title}")

# Создаём секции и уроки
sections_data = [
    ('Введение', ['Приветствие', 'Установка Django', 'Первый проект']),
    ('Основы', ['Модели', 'Виды', 'Шаблоны']),
    ('API', ['REST Framework', 'Сериализаторы']),
]

for section_idx, (section_title, lesson_titles) in enumerate(sections_data):
    section, created = Section.objects.get_or_create(
        course=course,
        title=section_title,
        defaults={'order': section_idx + 1}
    )
    if created:
        print(f"✅ Секция создана: {section_title}")
    else:
        print(f"📦 Секция уже существует: {section_title}")
    
    for lesson_idx, lesson_title in enumerate(lesson_titles):
        video_idx = (section_idx * 3 + lesson_idx) % len(videos)
        video_url = videos[video_idx]
        
        # Генерируем уникальный slug
        base_slug = slugify(lesson_title)
        
        # Проверяем если уже существует песок с таким названием
        try:
            lesson = Lesson.objects.get(slug=base_slug)
            print(f"  📦 Урок уже существует: {lesson_title}")
            # Обновим видео если ещё не было
            if not lesson.video_url and video_url:
                lesson.video_url = video_url
                lesson.save()
                print(f"     ✅ Видео обновлено")
        except Lesson.DoesNotExist:
            # Create unique slug
            counter = 1
            unique_slug = base_slug
            while Lesson.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            
            lesson = Lesson.objects.create(
                section=section,
                title=lesson_title,
                slug=unique_slug,
                description=f'Урок: {lesson_title}',
                content=f'<p>Содержание урока {lesson_title}</p>',
                video_url=video_url,
                duration_minutes=15 + lesson_idx * 5,
                order=lesson_idx + 1,
                is_free=lesson_idx == 0,
            )
            print(f"  ✅ Урок создан: {lesson_title} ({video_url[-20:]}...)")

print("\n✅ Тестовые данные готовы!")

# Проверяем
lessons_with_videos = Lesson.objects.filter(video_url__isnull=False, video_url__gt='').count()
print(f"📊 Всего уроков с видео: {lessons_with_videos}")
print(f"📊 Всего уроков в курсе: {Lesson.objects.count()}")
