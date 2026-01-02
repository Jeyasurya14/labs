from rest_framework import serializers
from .models import Quiz, Question, Choice, QuizAttempt

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'text'] # Don't expose is_correct here

class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'choices', 'order']

class QuizListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'time_limit_minutes', 'pass_score_percentage']

class QuizDetailSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'time_limit_minutes', 'pass_score_percentage', 'questions']

class QuizAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizAttempt
        fields = ['id', 'user', 'quiz', 'score', 'accuracy_percentage', 'passed', 'completed_at']
        read_only_fields = ['score', 'accuracy_percentage', 'passed', 'completed_at', 'user']
