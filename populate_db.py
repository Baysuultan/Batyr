#!/usr/bin/env python
"""
Скрипт для заполнения БД реалистичными данными
"""
import os
import django
from datetime import datetime, timedelta
from django.utils.text import slugify
from django.core.files.base import ContentFile
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coursehub.settings')
django.setup()

from django.contrib.auth import get_user_model
from courses.models import Course
from lessons.models import Section, Lesson
from categories.models import Category
from reviews.models import Review
from enrollments.models import Enrollment

User = get_user_model()

# YouTube видео (embed URLs)
VIDEOS = [
    'https://www.youtube.com/embed/34Rp6KVGIEM',
    'https://www.youtube.com/embed/5l9nxwh5Wiw',
    'https://www.youtube.com/embed/aO4Mnz485uM',
    'https://www.youtube.com/embed/eMhhl1Wq8JA',
    'https://www.youtube.com/embed/J1gE6CLcbRQ',  # Python basics
    'https://www.youtube.com/embed/7qHMXu_pPME',  # JavaScript
]

# Курсы для добавления
COURSES_DATA = [
    {
        'title': 'Python для начинающих',
        'slug': 'python-beginners',
        'description': 'Полный курс по изучению Python с нуля. Исследуйте основы программирования, работу с переменными, функциями и объектно-ориентированным программированием (ООП). Идеально подходит для абсолютных новичков.',
        'level': 'beginner',
        'price': '49.99',
        'duration': 20,
        'category': 'Программирование',
        'sections': [
            {
                'title': 'Основы Python',
                'lessons': [
                    ('Введение в Python', 'Состояние Python, установка, первый скрипт', 15),
                    ('Переменные и типы данных', 'На что способны переменные Python', 20),
                    ('Операторы и выражения', 'Математические и логические операторы', 18),
                    ('Управление потоком: if/else', 'Условные операторы и их применение', 22),
                ]
            },
            {
                'title': 'Функции и программирование',
                'lessons': [
                    ('Определение функций', 'Как писать переиспользуемый код', 25),
                    ('Параметры и возвращаемые значения', 'Передача данных в функции', 20),
                    ('Области видимости (Scope)', 'Локальные и глобальные переменные', 18),
                ]
            },
        ]
    },
    {
        'title': 'JavaScript Эксперт',
        'slug': 'javascript-expert',
        'description': 'Продвинутый курс JavaScript. Изучите асинхронное программирование, работу с DOM, AJAX, Promise, async/await и создание интерактивных веб-приложений.',
        'level': 'advanced',
        'price': '79.99',
        'duration': 35,
        'category': 'Веб-разработка',
        'sections': [
            {
                'title': 'Асинхронный JavaScript',
                'lessons': [
                    ('Callbacks и обработка ошибок', 'Основы асинхронности в JS', 25),
                    ('Promise: от создания к использованию', 'Работа с обещаниями (Promises)', 28),
                    ('Async/Await: современный подход', 'Письмо асинхронного кода как синхронного', 30),
                ]
            },
            {
                'title': 'DOM и события',
                'lessons': [
                    ('Манипуляция DOM', 'Изменение структуры страницы из JavaScript', 22),
                    ('Система событий', 'Обработка клика, ввода, скролла', 24),
                    ('AJAX и Fetch API', 'Загрузка данных без перезагрузки страницы', 26),
                ]
            },
        ]
    },
    {
        'title': 'React для веб-разработчиков',
        'slug': 'react-developers',
        'description': 'Научитесь создавать современные веб-приложения с React. Компоненты, состояние, жизненный цикл, hooks и управление состоянием с Redux.',
        'level': 'intermediate',
        'price': '69.99',
        'duration': 30,
        'category': 'Веб-разработка',
        'sections': [
            {
                'title': 'Основы React',
                'lessons': [
                    ('Введение в React', 'Что такое React и зачем нужен', 20),
                    ('JSX и компоненты', 'Создание переиспользуемых компонентов', 22),
                    ('Состояние иProps', 'Управление данными в компонентах', 25),
                    ('События и формы', 'Обработка пользовательского ввода', 23),
                ]
            },
            {
                'title': 'Продвинутые концепции',
                'lessons': [
                    ('Hooks: useState и useEffect', 'Modern React с функциональными компонентами', 28),
                    ('Custom Hooks', 'Создание собственных хуков', 25),
                    ('Контекст и Provider', 'Передача данных через дерево компонентов', 24),
                ]
            },
        ]
    },
    {
        'title': 'Django: Полный путь от нуля',
        'slug': 'django-complete',
        'description': 'Узнайте Django, один из лучших веб-фреймворков Python. От создания первого проекта до развертывания в production на облачных платформах.',
        'level': 'intermediate',
        'price': '89.99',
        'duration': 40,
        'category': 'Программирование',
        'sections': [
            {
                'title': 'Django базы',
                'lessons': [
                    ('Установка и настройка проекта', 'Первый Django проект', 18),
                    ('Модели и миграции', 'Работа с базой данных', 25),
                    ('Views и URLs', 'Маршрутизация и обработка запросов', 24),
                    ('Шаблоны (Templates)', 'Создание HTML страниц', 22),
                ]
            },
            {
                'title': 'REST API и продвинутые темы',
                'lessons': [
                    ('Django REST Framework', 'Создание API для приложений', 28),
                    ('Аутентификация и авторизация', 'Безопасность вашего приложения', 26),
                    ('Развертывание на Render/Heroku', 'Публикация в интернет', 20),
                ]
            },
        ]
    },
    {
        'title': 'Веб-дизайн: Теория и практика',
        'slug': 'web-design',
        'description': 'Научитесь создавать красивые и удобные веб-интерфейсы. Теория дизайна, UX/UI, прототипирование, работа с Figma и CSS Grid/Flexbox.',
        'level': 'beginner',
        'price': '59.99',
        'duration': 25,
        'category': 'Дизайн',
        'sections': [
            {
                'title': 'Основы дизайна',
                'lessons': [
                    ('Теория цвета и типография', 'Базовые принципы визуального дизайна', 20),
                    ('User Experience (UX)', 'Создание удобных интерфейсов', 22),
                    ('User Interface (UI)', 'Визуальное оформление и составляющие', 21),
                ]
            },
            {
                'title': 'Практическая реализация',
                'lessons': [
                    ('Макетирование и сетки', 'CSS Grid и Flexbox', 24),
                    ('Отзывчивый дизайн (Responsive)', 'Адаптация под разные экраны', 23),
                    ('Прототипирование в Figma', 'От идеи к макету', 25),
                ]
            },
        ]
    },
]

def get_or_create_user(username, first_name, last_name, email):
    """Создает или получает пользователя"""
    user, created = User.objects.get_or_create(
        username=username,
        defaults={
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'is_staff': False,
        }
    )
    if created:
        user.set_password('password123')
        user.save()
    return user

def get_or_create_category(name):
    """Создает или получает категорию"""
    slug = slugify(name)
    
    try:
        category = Category.objects.get(name=name)
        return category
    except Category.DoesNotExist:
        # Если категория с таким названием не существует, создаем её
        counter = 1
        unique_slug = slug
        while Category.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{slug}-{counter}"
            counter += 1
        
        category = Category.objects.create(name=name, slug=unique_slug)
        return category

def create_course(course_data, instructor):
    """Создает курс с секциями и уроками"""
    # Создаем или получаем категорию
    category = get_or_create_category(course_data['category'])
    
    # Создаем курс
    course, created = Course.objects.get_or_create(
        slug=course_data['slug'],
        defaults={
            'title': course_data['title'],
            'description': course_data['description'],
            'category': category,
            'instructor': instructor,
            'price': course_data['price'],
            'level': course_data['level'],
            'duration_hours': course_data['duration'],
            'status': 'published',
            'thumbnail': '',
            'tags': 'курс, онлайн, образование',
            'prerequisites': 'Базовые знания computer science приветствуются',
            'learning_outcomes': 'По окончанию курса вы потребуется на уровень выше',
        }
    )
    
    if created:
        print(f"✅ Курс создан: {course.title}")
    else:
        print(f"📦 Курс уже существует: {course.title}")
        return course
    
    # Создаем секции и уроки
    for section_idx, section_data in enumerate(course_data['sections'], 1):
        section, created = Section.objects.get_or_create(
            course=course,
            title=section_data['title'],
            defaults={'order': section_idx}
        )
        
        if created:
            print(f"  ✅ Секция: {section.title}")
        
        # Создаем уроки в секции
        for lesson_idx, (title, desc, duration) in enumerate(section_data['lessons'], 1):
            base_slug = slugify(title)
            
            # Ищем уникальный слаг
            counter = 1
            unique_slug = base_slug
            while Lesson.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            
            video_url = random.choice(VIDEOS)
            
            lesson, lesson_created = Lesson.objects.get_or_create(
                slug=unique_slug,
                defaults={
                    'section': section,
                    'title': title,
                    'description': desc,
                    'content': f'<h3>{title}</h3><p>{desc}</p><p>Этот урок охватывает все необходимые концепции для: {desc.lower()}</p>',
                    'video_url': video_url,
                    'duration_minutes': duration,
                    'order': lesson_idx,
                    'is_free': lesson_idx == 1,
                }
            )
            
            if lesson_created:
                print(f"    ✅ Урок: {title} ({duration} мин)")
    
    return course

def create_reviews(course, num_reviews=5):
    """Создает отзывы для курса"""
    comments = [
        'Отличный курс! Очень понятно объясняется материал.',
        'Преподаватель известен своим пациентным объяснением сложных тем.',
        'Получил все необходимые знания для работы. Рекомендую!',
        'Невероятный курс, стоит каждого рубля.',
        'Лучший курс из всех, что я проходил. Спасибо!',
        'Материал изложен структурированно и логично.',
        'Практические задания помогли закрепить знания.',
        'Преподаватель ответил на все мои вопросы.',
    ]
    
    titles = [
        'Отличный материал',
        'Стоит своих денег',
        'Рекомендую',
        'Очень помогло',
        'Лучший преподаватель',
    ]
    
    ratings_list = [4, 5, 5, 4, 5, 5, 4, 5]
    
    for i in range(num_reviews):
        comment = random.choice(comments)
        title = random.choice(titles)
        rating = random.choice(ratings_list)
        
        # Создаем или берем студента
        student = get_or_create_user(
            f'student{course.id}_{i}',
            f'Студент{i}',
            f'Курса{i}',
            f'student{course.id}_{i}@example.com'
        )
        
        # Создаем или получаем запись на курс
        enrollment, _ = Enrollment.objects.get_or_create(
            student=student,
            course=course,
            defaults={'status': 'active', 'progress': random.uniform(30, 100)}
        )
        
        # Создаем отзыв
        Review.objects.get_or_create(
            author=student,
            course=course,
            defaults={
                'rating': rating,
                'title': title,
                'comment': comment,
                'is_verified': True,
            }
        )

def main():
    print("=" * 80)
    print("📚 ЗАПОЛНЕНИЕ БД КУРСАМИ И ДАННЫМИ")
    print("=" * 80)
    print()
    
    # Создаем инструкторов
    print("👨‍🏫 Создание инструкторов...")
    instructors = []
    instructors_data = [
        ('irina_soloveva', 'Ирина', 'Соловева', 'irina@coursehub.kz'),
        ('dmitry_petrov', 'Дмитрий', 'Петров', 'dmitry@coursehub.kz'),
        ('elena_ivanova', 'Елена', 'Иванова', 'elena@coursehub.kz'),
        ('alexey_popov', 'Алексей', 'Попов', 'alexey@coursehub.kz'),
    ]
    
    for username, first_name, last_name, email in instructors_data:
        user = get_or_create_user(username, first_name, last_name, email)
        instructors.append(user)
        if user.pk:
            print(f"  ✅ {first_name} {last_name}")
    
    print()
    
    # Создаем курсы
    print("📖 Создание курсов...")
    courses = []
    for idx, course_data in enumerate(COURSES_DATA):
        instructor = instructors[idx % len(instructors)]
        course = create_course(course_data, instructor)
        courses.append(course)
        print()
    
    # Добавляем отзывы к курсам
    print("⭐ Добавление отзывов...")
    for course in courses:
        create_reviews(course, num_reviews=4)
        print(f"  ✅ Отзывы добавлены к {course.title}")
    
    print()
    print("=" * 80)
    print("✅ ГОТОВО!")
    print("=" * 80)
    print()
    print(f"📊 Статистика:")
    print(f"   • Курсов: {Course.objects.count()}")
    print(f"   • Уроков: {Lesson.objects.count()}")
    print(f"   • Инструкторов: {User.objects.filter(courses_created__isnull=False).distinct().count()}")
    print(f"   • Студентов: {User.objects.filter(enrollments__isnull=False).distinct().count()}")
    print(f"   • Записей на курсы: {Enrollment.objects.count()}")
    print(f"   • Отзывов: {Review.objects.count()}")
    print()

if __name__ == '__main__':
    main()
