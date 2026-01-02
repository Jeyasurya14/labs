from django.urls import path
from .views import LessonDetailView, CompleteLessonView

urlpatterns = [
    path('lessons/<int:pk>/', LessonDetailView.as_view(), name='lesson-detail'),
    path('lessons/<int:pk>/complete/', CompleteLessonView.as_view(), name='lesson-complete'),
]
