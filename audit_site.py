#!/usr/bin/env python
"""
Скрипт для полного аудита сайта - проверка всех URL и ошибок
"""
import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coursehub.settings')
django.setup()

from django.urls import get_resolver, URLPattern, URLResolver
from django.test import Client
from courses.models import Course
from lessons.models import Lesson, Section
from pages.models import StaticPage
from django.contrib.auth import get_user_model

User = get_user_model()

def get_all_urls():
    """Получает все URL маршруты из проекта"""
    resolver = get_resolver()
    urls = []
    
    def get_patterns(patterns, prefix=''):
        for pattern in patterns:
            if isinstance(pattern, URLResolver):
                get_patterns(pattern.url_patterns, prefix + str(pattern.pattern))
            elif isinstance(pattern, URLPattern):
                urls.append(prefix + str(pattern.pattern))
    
    get_patterns(resolver.url_patterns)
    return urls

def test_urls():
    """Тестирует все URL на доступность"""
    print("=" * 80)
    print("🔍 АУДИТ URL МАРШРУТОВ")
    print("=" * 80)
    print()
    
    client = Client()
    
    # Важные страницы для проверки
    test_urls = [
        ('/', 'Главная страница'),
        ('/courses/', 'Список курсов'),
        ('/about/', 'О проекте'),
        ('/terms/', 'Условия'),
        ('/privacy/', 'Политика конфиденциальности'),
        ('/accounts/login/', 'Вход'),
        ('/accounts/register/', 'Регистрация'),
        ('/admin/', 'Админ панель'),
    ]
    
    # Добавляем динамические URL
    for course in Course.objects.filter(status='published')[:3]:
        test_urls.append((f'/courses/{course.slug}/', f'Курс: {course.title}'))
        for lesson in course.sections.first().lessons.all()[:1]:
            test_urls.append((
                f'/courses/{course.slug}/lessons/{lesson.slug}/',
                f'Урок: {lesson.title}'
            ))
    
    errors_found = []
    success_count = 0
    
    for url, description in test_urls:
        try:
            response = client.get(url)
            if response.status_code == 200:
                print(f"✅ {response.status_code} - {url:40} ({description})")
                success_count += 1
            elif response.status_code in [301, 302]:
                print(f"↗️  {response.status_code} - {url:40} (Редирект)")
            else:
                print(f"⚠️  {response.status_code} - {url:40} ({description})")
                errors_found.append((url, response.status_code, description))
        except Exception as e:
            print(f"❌ ERROR - {url:40} ({str(e)[:40]})")
            errors_found.append((url, 'Exception', description))
    
    print()
    print(f"✅ Успешно: {success_count}/{len(test_urls)}")
    
    if errors_found:
        print(f"⚠️  Ошибок найдено: {len(errors_found)}")
        print()
        print("Детали ошибок:")
        for url, status, desc in errors_found:
            print(f"  • {url} ({status}) - {desc}")
    
    print()
    return len(errors_found) == 0

def check_templates():
    """Проверяет что все шаблоны загружаются"""
    print("=" * 80)
    print("📄 ПРОВЕРКА ШАБЛОНОВ")
    print("=" * 80)
    print()
    
    from django.template.loader import get_template
    from django.template import TemplateDoesNotExist
    
    templates = [
        'base.html',
        'pages/home.html',
        'pages/static_page.html',
        'courses/list.html',
        'courses/detail.html',
        'courses/lessons.html',
        'courses/lesson_detail.html',
        'accounts/login.html',
        'accounts/register.html',
        'accounts/profile.html',
        'accounts/profile_edit.html',
        'errors/404.html',
        'errors/500.html',
    ]
    
    loaded = 0
    missing = []
    
    for template in templates:
        try:
            get_template(template)
            print(f"✅ {template}")
            loaded += 1
        except TemplateDoesNotExist:
            print(f"❌ {template} - НЕ НАЙДЕН")
            missing.append(template)
    
    print()
    print(f"✅ Загружено: {loaded}/{len(templates)}")
    if missing:
        print(f"❌ Отсутствуют: {len(missing)}")
        for t in missing:
            print(f"  • {t}")
    
    print()
    return len(missing) == 0

def check_static_files():
    """Проверяет статические файлы"""
    print("=" * 80)
    print("📁 ПРОВЕРКА СТАТИЧЕСКИХ ФАЙЛОВ")
    print("=" * 80)
    print()
    
    import os
    
    static_files = [
        'css/style.css',
        'js/main.js',
    ]
    
    base_static = 'c:/Users/Байсултан/Desktop/САЙТ МОЦ/static'
    
    found = 0
    missing = []
    
    for file in static_files:
        full_path = os.path.join(base_static, file)
        if os.path.exists(full_path):
            size = os.path.getsize(full_path) / 1024  # KB
            print(f"✅ {file:30} ({size:.1f} KB)")
            found += 1
        else:
            print(f"❌ {file:30} - НЕ НАЙДЕН")
            missing.append(file)
    
    print()
    print(f"✅ Найдено: {found}/{len(static_files)}")
    if missing:
        print(f"❌ Отсутствуют: {len(missing)}")
    
    print()
    return len(missing) == 0

def check_database():
    """Проверяет целостность данных в БД"""
    print("=" * 80)
    print("💾 ПРОВЕРКА БАЗЫ ДАННЫХ")
    print("=" * 80)
    print()
    
    issues = []
    
    # Проверяем курсы
    courses = Course.objects.all()
    print(f"Курсы: {courses.count()}")
    for course in courses:
        if not course.title:
            issues.append(f"Курс {course.id} без названия")
        if not course.description:
            issues.append(f"Курс '{course.title}' без описания")
        if course.sections.count() == 0:
            issues.append(f"Курс '{course.title}' без секций")
    
    # Проверяем уроки
    lessons = Lesson.objects.all()
    print(f"Уроков: {lessons.count()}")
    for lesson in lessons:
        if not lesson.title:
            issues.append(f"Урок {lesson.id} без названия")
        if not lesson.slug:
            issues.append(f"Урок '{lesson.title}' без слага")
        if not lesson.section:
            issues.append(f"Урок '{lesson.title}' без секции")
    
    # Проверяем страницы
    pages = StaticPage.objects.all()
    print(f"Статических страниц: {pages.count()}")
    for page in pages:
        if not page.title or not page.content:
            issues.append(f"Страница '{page.slug}' неполная")
    
    # Проверяем пользователей
    users = User.objects.all()
    print(f"Пользователей: {users.count()}")
    
    print()
    if issues:
        print(f"⚠️  Найдено проблем: {len(issues)}")
        for issue in issues:
            print(f"  • {issue}")
    else:
        print("✅ Данные в порядке")
    
    print()
    return len(issues) == 0

def check_settings():
    """Проверяет критичные настройки"""
    print("=" * 80)
    print("⚙️  ПРОВЕРКА НАСТРОЕК")
    print("=" * 80)
    print()
    
    from django.conf import settings
    
    checks = [
        ('DEBUG', settings.DEBUG, False, 'Для production должно быть False'),
        ('ALLOWED_HOSTS', len(settings.ALLOWED_HOSTS) > 0, True, 'ALLOWED_HOSTS пуст'),
        ('STATIC_URL', settings.STATIC_URL, '/static/', 'STATIC_URL неправильно'),
        ('TEMPLATES DIRS', len(settings.TEMPLATES[0]['DIRS']) > 0, True, 'TEMPLATES DIRS пуст'),
    ]
    
    issues = []
    
    for name, value, expected, issue in checks:
        if isinstance(expected, bool):
            if bool(value) == expected:
                print(f"✅ {name}: OK")
            else:
                print(f"⚠️  {name}: {issue}")
                issues.append(issue)
        else:
            if str(value) == str(expected):
                print(f"✅ {name}: {value}")
            else:
                print(f"⚠️  {name}: {value} (ожидается {expected})")
                issues.append(f"{name} неправильно")
    
    print()
    if issues:
        print(f"⚠️  Найдено проблем: {len(issues)}")
    else:
        print("✅ Настройки в порядке")
    
    print()
    return len(issues) == 0

def main():
    print("\n" + "=" * 80)
    print("🔍 ПОЛНЫЙ АУДИТ САЙТА COURSEHUB")
    print("=" * 80 + "\n")
    
    results = {
        'URLs': test_urls(),
        'Шаблоны': check_templates(),
        'Статические файлы': check_static_files(),
        'База данных': check_database(),
        'Настройки': check_settings(),
    }
    
    print("\n" + "=" * 80)
    print("📊 ИТОГОВЫЙ ОТЧЕТ")
    print("=" * 80)
    print()
    
    for check_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {check_name}")
    
    all_pass = all(results.values())
    
    print()
    if all_pass:
        print("🎉 ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ УСПЕШНО!")
    else:
        print("⚠️  НЕКОТОРЫЕ ПРОВЕРКИ НЕ ПРОШЛИ. ТРЕБУЕТСЯ ВНИМАНИЕ.")
    
    print("=" * 80)
    print()

if __name__ == '__main__':
    main()
