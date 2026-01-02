from rest_framework import serializers
from .models import Course, Chapter
from lessons.models import Lesson
from users.serializers import UserSerializer

class LessonListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'order', 'duration_minutes', 'is_free_preview', 'content_type']

class ChapterSerializer(serializers.ModelSerializer):
    lessons = LessonListSerializer(many=True, read_only=True)

    class Meta:
        model = Chapter
        fields = ['id', 'title', 'order', 'description', 'lessons']

class CourseListSerializer(serializers.ModelSerializer):
    instructor = UserSerializer(read_only=True)
    chapter_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'instructor', 'cover_image', 'created_at', 'chapter_count']

    def get_chapter_count(self, obj):
        return obj.chapters.count()

class CourseDetailSerializer(serializers.ModelSerializer):
    instructor = UserSerializer(read_only=True)
    chapters = ChapterSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'instructor', 'cover_image', 'created_at', 'updated_at', 'chapters']
