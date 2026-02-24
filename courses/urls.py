from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.course_list, name='list'),
    path('<slug:slug>/', views.course_detail, name='detail'),
    path('<slug:slug>/enroll/', views.enroll, name='enroll'),
    path('<slug:slug>/unenroll/', views.unenroll, name='unenroll'),
    path('<slug:slug>/lessons/', views.course_lessons, name='lessons'),
    path('lessons/<slug:lesson_slug>/', views.lesson_detail, name='lesson_detail'),
]
