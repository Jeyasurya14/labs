from django.urls import path
from .views import CourseListView, CourseDetailView, EnrollCourseView, MyCoursesView

urlpatterns = [
    path('courses/', CourseListView.as_view(), name='course-list'),
    path('courses/my/', MyCoursesView.as_view(), name='my-courses'),
    path('courses/<int:pk>/', CourseDetailView.as_view(), name='course-detail'),
    path('courses/<int:pk>/enroll/', EnrollCourseView.as_view(), name='course-enroll'),
]
