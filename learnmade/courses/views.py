from rest_framework import generics, permissions, status, views
from rest_framework.response import Response
from .models import Course, Enrollment
from .serializers import CourseListSerializer, CourseDetailSerializer

class CourseListView(generics.ListAPIView):
    queryset = Course.objects.filter(is_published=True)
    serializer_class = CourseListSerializer
    permission_classes = [permissions.AllowAny]

class CourseDetailView(generics.RetrieveAPIView):
    queryset = Course.objects.filter(is_published=True)
    serializer_class = CourseDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class EnrollCourseView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk, *args, **kwargs):
        course = generics.get_object_or_404(Course, pk=pk)
        enrollment, created = Enrollment.objects.get_or_create(user=request.user, course=course)
        if created:
            return Response({"status": "enrolled"}, status=status.HTTP_201_CREATED)
        return Response({"status": "already enrolled"}, status=status.HTTP_200_OK)

class MyCoursesView(generics.ListAPIView):
    serializer_class = CourseListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Course.objects.filter(enrollments__user=self.request.user)
