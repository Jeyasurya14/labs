from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from courses.models import Course, Chapter, Enrollment
from lessons.models import Lesson, LessonCompletion

User = get_user_model()

class DashboardTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.instructor = User.objects.create_user(username='instructor', password='password123')
        self.course = Course.objects.create(title="Test Course", instructor=self.instructor, is_published=True)
        self.chapter = Chapter.objects.create(course=self.course, title="Chapter 1", order=1)
        self.lesson = Lesson.objects.create(chapter=self.chapter, title="Lesson 1", order=1)
        self.client.force_authenticate(user=self.user)

    def test_enroll_course(self):
        url = reverse('course-enroll', kwargs={'pk': self.course.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Enrollment.objects.filter(user=self.user, course=self.course).exists())

    def test_my_courses(self):
        Enrollment.objects.create(user=self.user, course=self.course)
        url = reverse('my-courses')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], "Test Course")

    def test_complete_lesson(self):
        url = reverse('lesson-complete', kwargs={'pk': self.lesson.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(LessonCompletion.objects.filter(user=self.user, lesson=self.lesson).exists())
