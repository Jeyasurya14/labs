from rest_framework import generics, permissions, status, views
from rest_framework.response import Response
from .models import Quiz, QuizAttempt, Question, Choice
from .serializers import QuizListSerializer, QuizDetailSerializer, QuizAttemptSerializer

class QuizListView(generics.ListAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class QuizDetailView(generics.RetrieveAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

class QuizSubmitView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk, *args, **kwargs):
        quiz = generics.get_object_or_404(Quiz, pk=pk)
        data = request.data.get('answers', []) # Expected format: [{"question_id": 1, "choice_id": 2}, ...]
        
        score = 0
        total_questions = quiz.questions.count()

        if total_questions == 0:
            return Response({"error": "Quiz has no questions"}, status=status.HTTP_400_BAD_REQUEST)

        # Basic scoring logic
        for answer in data:
            question_id = answer.get('question_id')
            choice_id = answer.get('choice_id')
            
            try:
                question = Question.objects.get(pk=question_id, quiz=quiz)
                choice = Choice.objects.get(pk=choice_id, question=question)
                if choice.is_correct:
                    score += 1
            except (Question.DoesNotExist, Choice.DoesNotExist):
                continue

        accuracy = (score / total_questions) * 100
        passed = accuracy >= quiz.pass_score_percentage

        attempt = QuizAttempt.objects.create(
            user=request.user,
            quiz=quiz,
            score=score,
            accuracy_percentage=accuracy,
            passed=passed
        )

        return Response(QuizAttemptSerializer(attempt).data, status=status.HTTP_201_CREATED)
