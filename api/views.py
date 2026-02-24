from rest_framework import viewsets, filters, generics, permissions
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

from courses.models import Course
from reviews.models import Review
from categories.models import Category
from lessons.models import Lesson
from enrollments.models import Enrollment

from .serializers import (
    CourseDetailSerializer, CourseListSerializer, ReviewSerializer,
    CategorySerializer, LessonSerializer, EnrollmentSerializer
)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 100


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    """API для курсов"""
    queryset = Course.objects.filter(status='published').select_related('category', 'instructor')
    serializer_class = CourseDetailSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'level']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'rating', 'price']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CourseDetailSerializer
        return CourseListSerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """API для категорий"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class ReviewViewSet(viewsets.ModelViewSet):
    """API для отзывов"""
    serializer_class = ReviewSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['course']
    ordering_fields = ['rating', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        return Review.objects.select_related('author', 'course')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class LessonViewSet(viewsets.ReadOnlyModelViewSet):
    """API для уроков"""
    queryset = Lesson.objects.select_related('section')
    serializer_class = LessonSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['section']
    search_fields = ['title']


class EnrollmentListCreateView(generics.ListCreateAPIView):
    """API для записей"""
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Enrollment.objects.filter(student=self.request.user)

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)


class MyCoursesList(generics.ListAPIView):
    """Мои курсы"""
    serializer_class = CourseListSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        user = self.request.user
        return Course.objects.filter(
            enrollments__student=user
        ).select_related('category', 'instructor').distinct()

