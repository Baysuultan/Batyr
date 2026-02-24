from django.shortcuts import render
from django.http import JsonResponse
from .models import StaticPage, ContactMessage
from courses.models import Course


def home(request):
    """Главная страница"""
    featured_courses = Course.objects.filter(status='published').order_by('-created_at')[:6]
    stats = {
        'total_courses': Course.objects.filter(status='published').count(),
        'total_students': 0,  # Можно добавить через aggregate
        'total_instructors': 0,
    }
    context = {
        'featured_courses': featured_courses,
        'stats': stats,
    }
    return render(request, 'pages/home.html', context)


def about(request):
    """Страница О проекте"""
    page = StaticPage.objects.filter(slug='about').first()
    if not page:
        page = StaticPage(
            title='О проекте',
            slug='about',
            content='<h1>CourseHub</h1><p>Портал онлайн курсов</p>'
        )
    context = {'page': page}
    return render(request, 'pages/static_page.html', context)


def privacy(request):
    """Политика конфиденциальности"""
    page = StaticPage.objects.filter(slug='privacy').first()
    if not page:
        page = StaticPage(
            title='Политика конфиденциальности',
            slug='privacy',
            content='<h1>Политика конфиденциальности</h1>'
        )
    context = {'page': page}
    return render(request, 'pages/static_page.html', context)


def terms(request):
    """Условия использования"""
    page = StaticPage.objects.filter(slug='terms').first()
    if not page:
        page = StaticPage(
            title='Условия использования',
            slug='terms',
            content='<h1>Условия использования</h1>'
        )
    context = {'page': page}
    return render(request, 'pages/static_page.html', context)


def contact(request):
    """Форма контакта"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success', 'message': 'Сообщение отправлено'})
        
        return render(request, 'pages/contact_success.html')
    
    return render(request, 'pages/contact.html')


def page_not_found(request, exception=None):
    """Страница 404"""
    return render(request, 'errors/404.html', status=404)


def server_error(request):
    """Страница 500"""
    return render(request, 'errors/500.html', status=500)

