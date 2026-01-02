from rest_framework import generics, permissions, status, views
from rest_framework.response import Response
from .models import Lesson, LessonCompletion
from .serializers import LessonDetailSerializer

class LessonDetailView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonDetailSerializer
    permission_classes = [permissions.IsAuthenticated] # Or allow free preview logic later

class CompleteLessonView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk, *args, **kwargs):
        lesson = generics.get_object_or_404(Lesson, pk=pk)
        # Check if user is enrolled in the course? Ideally yes, skipping for MVP speed
        completion, created = LessonCompletion.objects.get_or_create(user=request.user, lesson=lesson)
        return Response({"status": "completed"}, status=status.HTTP_200_OK)
