from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.conf import settings

from courses.models import Course
from enrollments.models import Enrollment
from .models import UserProfile

# Импортируем нашу модель пользователя
User = settings.AUTH_USER_MODEL


def register(request):
    """Регистрация нового пользователя"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        # Валидация
        if password1 != password2:
            messages.error(request, 'Пароли не совпадают')
            return redirect('accounts:register')
        
        # Проверяем существование пользователя
        from django.contrib.auth import get_user_model
        UserModel = get_user_model()
        
        if UserModel.objects.filter(username=username).exists():
            messages.error(request, 'Пользователь с таким именем уже существует')
            return redirect('accounts:register')
        
        if UserModel.objects.filter(email=email).exists():
            messages.error(request, 'Email уже зарегистрирован')
            return redirect('accounts:register')
        
        # Создаем пользователя
        user = UserModel.objects.create_user(
            username=username,
            email=email,
            password=password1
        )
        
        # Создаем профиль
        UserProfile.objects.create(user=user)
        
        messages.success(request, 'Регистрация успешна! Войдите в свой аккаунт.')
        return redirect('accounts:login')
    
    return render(request, 'accounts/register.html')


@login_required(login_url='accounts:login')
def profile(request):
    """Профиль пользователя"""
    user = request.user
    
    # Получаем или создаем профиль
    profile, created = UserProfile.objects.get_or_create(user=user)
    
    # Мои курсы
    my_courses = Enrollment.objects.filter(student=user).select_related('course')
    favorites = profile.favorite_courses.all()
    
    context = {
        'my_courses': my_courses,
        'favorite_courses': favorites,
        'profile': profile,
    }
    return render(request, 'accounts/profile.html', context)


@login_required(login_url='accounts:login')
def profile_edit(request):
    """Редактирование профиля"""
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)
    
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.save()
        
        profile.bio = request.POST.get('bio', profile.bio)
        profile.phone = request.POST.get('phone', profile.phone)
        profile.country = request.POST.get('country', profile.country)
        
        # Загрузка аватара
        if 'avatar' in request.FILES:
            profile.avatar = request.FILES['avatar']
        
        profile.save()
        
        messages.success(request, 'Профиль обновлен')
        return redirect('accounts:profile')
    
    context = {
        'profile': profile,
        'user': user,
    }
    return render(request, 'accounts/profile_edit.html', context)

