from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Quiz, Question, Choice

User = get_user_model()

class QuizTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.quiz = Quiz.objects.create(title="Test Quiz", pass_score_percentage=50)
        self.question = Question.objects.create(quiz=self.quiz, text="What is 2+2?")
        self.choice1 = Choice.objects.create(question=self.question, text="4", is_correct=True)
        self.choice2 = Choice.objects.create(question=self.question, text="3", is_correct=False)
        self.client.force_authenticate(user=self.user)

    def test_submit_quiz_pass(self):
        url = reverse('quiz-submit', kwargs={'pk': self.quiz.pk})
        data = {'answers': [{'question_id': self.question.id, 'choice_id': self.choice1.id}]}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['passed'])
        self.assertEqual(response.data['score'], 1)

    def test_submit_quiz_fail(self):
        url = reverse('quiz-submit', kwargs={'pk': self.quiz.pk})
        data = {'answers': [{'question_id': self.question.id, 'choice_id': self.choice2.id}]}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertFalse(response.data['passed'])
        self.assertEqual(response.data['score'], 0)
