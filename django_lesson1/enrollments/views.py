
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Enrollment

@login_required
def enrollment_list(request):
    enrollments = Enrollment.objects.select_related('student', 'course').all()
    return render(request, 'enrollments/enrollment_list.html', {'enrollments': enrollments})
# Create your views here.
