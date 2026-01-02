from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/learn/', include('courses.urls')),
    path('api/learn/', include('lessons.urls')),
    path('api/quiz/', include('quizzes.urls')),
]
