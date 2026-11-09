from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from students.models import Student
from courses.models import Course
from enrollments.models import Enrollment
from .serializers import StudentSerializer, CourseSerializer, EnrollmentSerializer


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'])
    def transcript(self, request, pk=None):
        student = self.get_object()
        enrollments = student.enrollments.filter(status='COMPLETED')
        return Response({
            'student_id': student.student_id,
            'khmer_name': student.khmer_name,
            'gpa': float(student.gpa),
            'completed_courses': enrollments.count(),
        })


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]


class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]