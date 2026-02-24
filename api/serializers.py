from rest_framework import serializers
from courses.models import Course
from reviews.models import Review
from categories.models import Category
from lessons.models import Lesson, Section
from enrollments.models import Enrollment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'color']


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ['id', 'title', 'order']


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'slug', 'description', 'duration_minutes', 'is_free']


class CourseListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    
    class Meta:
        model = Course
        fields = ['id', 'title', 'slug', 'description', 'price', 'rating', 
                 'thumbnail', 'category', 'level', 'students_count']


class CourseDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    sections = SectionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Course
        fields = ['id', 'title', 'slug', 'description', 'price', 'rating',
                 'thumbnail', 'category', 'level', 'duration_hours', 
                 'students_count', 'learning_outcomes', 'sections']


class ReviewSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'rating', 'title', 'comment', 'author_name', 'created_at']


class EnrollmentSerializer(serializers.ModelSerializer):
    course = CourseListSerializer(read_only=True)
    
    class Meta:
        model = Enrollment
        fields = ['id', 'course', 'status', 'progress', 'enrolled_at']
