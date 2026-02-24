from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'api'

router = DefaultRouter()
router.register(r'courses', views.CourseViewSet, basename='course')
router.register(r'reviews', views.ReviewViewSet, basename='review')
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'lessons', views.LessonViewSet, basename='lesson')

urlpatterns = [
    path('', include(router.urls)),
    path('enrollments/', views.EnrollmentListCreateView.as_view(), name='enrollment-list'),
    path('my-courses/', views.MyCoursesList.as_view(), name='my-courses'),
]
