from django.shortcuts import render
from students.models import Student
from courses.models import Course
from enrollments.models import Enrollment

def home(request):
    """ទំព័រដើម បង្ហាញស្ថិតិសរុប"""
    total_students = Student.objects.count()
    active_students = Student.objects.filter(is_active=True).count()
    total_courses = Course.objects.count()
    active_courses = Course.objects.filter(status='ACTIVE').count()
    total_enrollments = Enrollment.objects.count()
    
    return render(request, 'home.html', {
        'total_students': total_students,
        'active_students': active_students,
        'total_courses': total_courses,
        'active_courses': active_courses,
        'total_enrollments': total_enrollments,
    })
