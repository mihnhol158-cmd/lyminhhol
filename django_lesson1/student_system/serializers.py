from rest_framework import serializers
from students.models import Student
from courses.models import Course
from enrollments.models import Enrollment


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'student_id', 'khmer_name', 'date_of_birth', 'gender',
                  'phone_number', 'city', 'country', 'profile_picture', 'gpa', 'is_active']


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'code', 'title', 'description', 'instructor',
                  'credits', 'level', 'capacity', 'status',
                  'start_date', 'end_date']


class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'course', 'status', 'grade',
                  'score', 'attendance_percentage', 'enrollment_date']
        read_only_fields = ['grade', 'enrollment_date']