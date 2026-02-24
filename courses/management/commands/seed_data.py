from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from categories.models import Category
from courses.models import Course
from lessons.models import Section, Lesson
from reviews.models import Review
from accounts.models import UserProfile

User = get_user_model()


class Command(BaseCommand):
    help = 'Загружает демо-данные для тестирования'

    def handle(self, *args, **options):
        # Создаем категории
        categories_data = [
            {'name': 'Программирование', 'icon': 'code'},
            {'name': 'Дизайн', 'icon': 'palette'},
            {'name': 'Маркетинг', 'icon': 'megaphone'},
            {'name': 'Бизнес', 'icon': 'briefcase'},
            {'name': 'Языки', 'icon': 'globe'},
        ]
        
        categories = {}
        for i, cat_data in enumerate(categories_data):
            cat, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'icon': cat_data['icon'], 'order': i}
            )
            categories[cat_data['name']] = cat
            if created:
                self.stdout.write(f'✓ Создана категория: {cat.name}')

        # Создаем тестовых инструкторов
        instructors = []
        for i in range(3):
            user, created = User.objects.get_or_create(
                username=f'instructor{i+1}',
                defaults={
                    'email': f'instructor{i+1}@coursehub.kz',
                    'first_name': f'Инструктор',
                    'last_name': f'{i+1}',
                    'is_instructor': True,
                }
            )
            if created:
                user.set_password('password123')
                user.save()
                UserProfile.objects.get_or_create(user=user)
                self.stdout.write(f'✓ Создан инструктор: {user.username}')
            instructors.append(user)

        # Создаем тестовые курсы
        courses_data = [
            {
                'title': 'Python для начинающих',
                'description': 'Полный курс Python от основ до практики',
                'category': 'Программирование',
                'level': 'beginner',
                'price': 5000,
                'duration_hours': 40,
                'instructor_idx': 0,
            },
            {
                'title': 'Django веб-разработка',
                'description': 'Создавайте мощные веб-приложения с Django',
                'category': 'Программирование',
                'level': 'intermediate',
                'price': 7000,
                'duration_hours': 60,
                'instructor_idx': 0,
            },
            {
                'title': 'JavaScript Мастер-класс',
                'description': 'Современный JavaScript с ES6+',
                'category': 'Программирование',
                'level': 'intermediate',
                'price': 6000,
                'duration_hours': 45,
                'instructor_idx': 1,
            },
            {
                'title': 'UI/UX Дизайн',
                'description': 'Принципы проектирования интерфейсов',
                'category': 'Дизайн',
                'level': 'beginner',
                'price': 4000,
                'duration_hours': 35,
                'instructor_idx': 2,
            },
            {
                'title': 'Цифровой маркетинг',
                'description': 'Стратегии маркетинга в интернет',
                'category': 'Маркетинг',
                'level': 'intermediate',
                'price': 5500,
                'duration_hours': 40,
                'instructor_idx': 1,
            },
        ]

        for course_data in courses_data:
            course, created = Course.objects.get_or_create(
                title=course_data['title'],
                defaults={
                    'description': course_data['description'],
                    'category': categories[course_data['category']],
                    'instructor': instructors[course_data['instructor_idx']],
                    'level': course_data['level'],
                    'price': course_data['price'],
                    'duration_hours': course_data['duration_hours'],
                    'status': 'published',
                    'learning_outcomes': 'После завершения курса вы сможете применять полученные знания на практике',
                }
            )
            if created:
                self.stdout.write(f'✓ Создан курс: {course.title}')
                
                # Создаем разделы и уроки
                sections_data = [
                    {'title': 'Введение', 'lessons': 3},
                    {'title': 'Основные концепции', 'lessons': 5},
                    {'title': 'Практические примеры', 'lessons': 4},
                ]
                
                for section_idx, section_data in enumerate(sections_data):
                    section, _ = Section.objects.get_or_create(
                        course=course,
                        title=section_data['title'],
                        defaults={'order': section_idx}
                    )
                    
                    for lesson_idx in range(section_data['lessons']):
                        Lesson.objects.get_or_create(
                            section=section,
                            title=f"{section_data['title']} - Урок {lesson_idx + 1}",
                            defaults={
                                'description': f'Описание урока {lesson_idx + 1}',
                                'order': lesson_idx,
                                'duration_minutes': 30 + lesson_idx * 10,
                                'is_free': lesson_idx == 0,
                            }
                        )

        # Создаем тестовых студентов с отзывами
        for i in range(5):
            user, created = User.objects.get_or_create(
                username=f'student{i+1}',
                defaults={
                    'email': f'student{i+1}@coursehub.kz',
                    'first_name': f'Студент',
                    'last_name': f'{i+1}',
                }
            )
            if created:
                user.set_password('password123')
                user.save()
                UserProfile.objects.get_or_create(user=user)
                self.stdout.write(f'✓ Создан студент: {user.username}')

        # Добавляем отзывы
        for course in Course.objects.all()[:3]:
            for student in User.objects.filter(username__startswith='student')[:2]:
                Review.objects.get_or_create(
                    course=course,
                    author=student,
                    defaults={
                        'rating': 4 + (len(student.username) % 2),
                        'title': 'Отличный курс!',
                        'comment': 'Курс помог мне справиться с моими целями обучения.',
                    }
                )

        self.stdout.write(self.style.SUCCESS('✓ Демо-данные успешно загружены!'))
