from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Avg
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .models import Course
from lessons.models import Lesson, Section
from reviews.models import Review
from enrollments.models import Enrollment, LessonProgress


def course_list(request):
    """Список курсов с фильтрацией"""
    courses = Course.objects.filter(status='published').select_related('category', 'instructor')
    
    # Поиск
    search = request.GET.get('search', '')
    if search:
        courses = courses.filter(
            Q(title__icontains=search) | 
            Q(description__icontains=search)
        )
    
    # Фильтр по категории
    category = request.GET.get('category', '')
    if category:
        courses = courses.filter(category__slug=category)
    
    # Сортировка
    sort = request.GET.get('sort', '-created_at')
    courses = courses.order_by(sort)
    
    # Уровень сложности
    level = request.GET.get('level', '')
    if level:
        courses = courses.filter(level=level)
    
    # Пагинация
    paginator = Paginator(courses, 12)
    page = request.GET.get('page')
    try:
        courses = paginator.page(page)
    except PageNotAnInteger:
        courses = paginator.page(1)
    except EmptyPage:
        courses = paginator.page(paginator.num_pages)
    
    context = {
        'courses': courses,
        'search': search,
        'category': category,
        'level': level,
        'sort': sort,
    }
    return render(request, 'courses/list.html', context)


def course_detail(request, slug):
    """Детали курса"""
    course = get_object_or_404(Course.objects.select_related('category', 'instructor'), slug=slug)
    
    # Проверяем, записан ли пользователь
    is_enrolled = False
    if request.user.is_authenticated:
        is_enrolled = Enrollment.objects.filter(
            student=request.user,
            course=course
        ).exists()
    
    # Отзывы
    reviews = Review.objects.filter(course=course).select_related('author')
    avg_rating = Review.objects.filter(course=course).aggregate(Avg('rating'))['rating__avg'] or 0
    
    # Разделы и уроки
    sections = Section.objects.filter(course=course).prefetch_related('lessons')
    
    context = {
        'course': course,
        'is_enrolled': is_enrolled,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'sections': sections,
    }
    return render(request, 'courses/detail.html', context)


@login_required(login_url='accounts:login')
def enroll(request, slug):
    """Запись на курс"""
    course = get_object_or_404(Course, slug=slug)
    
    enrollment, created = Enrollment.objects.get_or_create(
        student=request.user,
        course=course
    )
    
    if created:
        course.students_count += 1
        course.save()
        messages.success(request, f'Вы записались на курс "{course.title}"')
    else:
        messages.info(request, 'Вы уже записаны на этот курс')
    
    return redirect('courses:detail', slug=slug)


@login_required(login_url='accounts:login')
def unenroll(request, slug):
    """Отписка от курса"""
    course = get_object_or_404(Course, slug=slug)
    
    enrollment = Enrollment.objects.filter(
        student=request.user,
        course=course
    ).first()
    
    if enrollment:
        enrollment.delete()
        course.students_count = max(0, course.students_count - 1)
        course.save()
        messages.success(request, f'Вы отписались от курса "{course.title}"')
    
    return redirect('courses:detail', slug=slug)


@login_required(login_url='accounts:login')
def course_lessons(request, slug):
    """Уроки курса"""
    course = get_object_or_404(Course, slug=slug)
    
    # Проверяем доступ
    is_enrolled = Enrollment.objects.filter(
        student=request.user,
        course=course
    ).exists()
    
    if not is_enrolled:
        messages.error(request, 'Сначала запишитесь на курс')
        return redirect('courses:detail', slug=slug)
    
    sections = Section.objects.filter(course=course).prefetch_related('lessons')
    
    context = {
        'course': course,
        'sections': sections,
    }
    return render(request, 'courses/lessons.html', context)


def lesson_detail(request, lesson_slug):
    """Детали урока"""
    lesson = get_object_or_404(Lesson.objects.select_related('section'), slug=lesson_slug)
    course = lesson.section.course
    
    # Проверяем доступ для незарегистрированных пользователей
    if not request.user.is_authenticated and not lesson.is_free:
        messages.error(request, 'Войдите, чтобы просмотреть этот урок')
        return redirect('accounts:login')
    
    # Проверяем, записан ли пользователь
    is_enrolled = False
    if request.user.is_authenticated:
        is_enrolled = Enrollment.objects.filter(
            student=request.user,
            course=course
        ).exists()
        
        if not is_enrolled and not lesson.is_free:
            messages.error(request, 'Запишитесь на курс для доступа к урокам')
            return redirect('courses:detail', slug=course.slug)
    
    # Получаем другие уроки раздела
    other_lessons = lesson.section.lessons.exclude(id=lesson.id)
    
    context = {
        'lesson': lesson,
        'course': course,
        'other_lessons': other_lessons,
        'is_enrolled': is_enrolled,
    }
    return render(request, 'courses/lesson_detail.html', context)

