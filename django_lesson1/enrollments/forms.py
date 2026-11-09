from django import forms
from .models import Enrollment

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['student', 'course', 'status']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

class GradeForm(forms.ModelForm):
    """Form សម្រាប់សាស្រ្តាចារ្យបញ្ចូលពិន្ទុ និងវត្តមាន"""
    class Meta:
        model = Enrollment
        fields = ['score', 'attendance_percentage', 'notes']
        widgets = {
            'score': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '100', 'step': '0.01'}),
            'attendance_percentage': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '100'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
