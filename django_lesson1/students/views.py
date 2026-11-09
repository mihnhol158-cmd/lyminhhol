from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Student
from .forms import StudentForm, UserForm, StudentRegistrationForm

# ==================== 1. Function-Based Views ====================

@login_required
def student_list(request):
    """បង្ហាញបញ្ជីសិស្ស ជាមួយមុខងារស្វែងរកតាមឈ្មោះខ្មែរ និង Pagination"""
    search_query = request.GET.get('q', '').strip()
    students_qs = Student.objects.select_related('user').all()
    
    if search_query:
        students_qs = students_qs.filter(
            Q(student_id__icontains=search_query) |
            Q(khmer_name__icontains=search_query) |
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query)
        )
    
    paginator = Paginator(students_qs.order_by('student_id'), 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'students/student_list.html', {
        'students': page_obj,
        'page_obj': page_obj,
        'search_query': search_query,
    })

@login_required
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    enrollments = student.enrollments.select_related('course').all()
    return render(request, 'students/student_detail.html', {'student': student, 'enrollments': enrollments})

@login_required
def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student_form = StudentForm(request.POST, request.FILES, instance=student)
        user_form = UserForm(request.POST, instance=student.user)
        if student_form.is_valid() and user_form.is_valid():
            student_form.save()
            user_form.save()
            messages.success(request, f"បានកែប្រែទិន្នន័យ {student.student_id} ដោយជោគជ័យ!")
            return redirect('students:student_detail', pk=student.pk)
    else:
        student_form = StudentForm(instance=student)
        user_form = UserForm(instance=student.user)
    
    return render(request, 'students/student_form.html', {
        'student_form': student_form,
        'user_form': user_form,
        'student': student,
    })

def register_student(request):
    """ចុះឈ្មោះគណនីសិស្សថ្មី"""
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            student = Student.objects.create(
                user=user,
                student_id=form.cleaned_data['student_id'],
                khmer_name=form.cleaned_data.get('khmer_name', ''),
                date_of_birth=form.cleaned_data['date_of_birth'],
                gender=form.cleaned_data['gender'],
                phone_number=form.cleaned_data.get('phone_number', ''),
                address=form.cleaned_data['address'],
                city=form.cleaned_data['city'],
                country=form.cleaned_data['country'],
            )
            messages.success(request, "ការចុះឈ្មោះបានជោគជ័យ!")
            login(request, user)
            return redirect('students:student_detail', pk=student.pk)
    else:
        form = StudentRegistrationForm()
    return render(request, 'students/register.html', {'form': form})

# ==================== 2. Class-Based Views ====================

class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    template_name = 'students/student_list.html'
    context_object_name = 'students'
    paginate_by = 20

class StudentDetailView(LoginRequiredMixin, DetailView):
    model = Student
    template_name = 'students/student_detail.html'
    context_object_name = 'student'

class StudentCreateView(LoginRequiredMixin, CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'students/student_form.html'
    success_url = reverse_lazy('students:student_list')

    def form_valid(self, form):
        if not hasattr(self.request.user, 'student'):
            form.instance.user = self.request.user
        else:
            student_id = form.cleaned_data.get('student_id', '')
            user, _ = User.objects.get_or_create(username=f"std_{student_id.lower()}")
            form.instance.user = user
        return super().form_valid(form)
