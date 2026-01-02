from django.db import models
from django.conf import settings
from courses.models import Chapter

class Lesson(models.Model):
    LESSON_TYPES = (
        ('video', 'Video'),
        ('text', 'Text'),
        ('code', 'Code Snippet'),
    )

    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=255)
    order = models.PositiveIntegerField()
    content_type = models.CharField(max_length=20, choices=LESSON_TYPES, default='text')
    video_url = models.URLField(blank=True, null=True)
    text_content = models.TextField(blank=True, help_text="Markdown supported")
    code_snippet = models.TextField(blank=True, help_text="Code to display")
    duration_minutes = models.PositiveIntegerField(default=0)
    is_free_preview = models.BooleanField(default=False)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

class LessonCompletion(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='completed_lessons')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='completions')
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'lesson')

    def __str__(self):
        return f"{self.user.username} completed {self.lesson.title}"
