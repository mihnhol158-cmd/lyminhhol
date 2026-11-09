from django.db import models

# Create your models here.
from django.db import models
from students.models import Student
from courses.models import Course
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator

class Enrollment(models.Model):
    """Model សម្រាប់កត់ត្រាការចុះឈ្មោះរៀន និងលទ្ធផលពិន្ទុ"""
    
    STATUS_CHOICES = [
        ('ENROLLED', 'កំពុងរៀន (Enrolled)'),
        ('COMPLETED', 'បានបញ្ចប់ (Completed)'),
        ('DROPPED', 'បោះបង់ (Dropped)'),
        ('SUSPENDED', 'ផ្អាកការសិក្សា (Suspended)'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrollment_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ENROLLED')
    
    grade = models.CharField(max_length=2, blank=True, null=True, help_text="និទ្ទេស (A, B, C, D, F)")
    score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True,
                                validators=[MinValueValidator(0), MaxValueValidator(100)])
    attendance_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0,
                                                validators=[MinValueValidator(0), MaxValueValidator(100)])
    completed_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'course') # សិស្សម្នាក់មិនអាចចុះឈ្មោះមុខវិជ្ជាដដែលលើសពីម្ដងឡើយ
        ordering = ['-enrollment_date']

    def __str__(self):
        return f"{self.student.student_id} - {self.course.code}"

    def calculate_grade(self):
        """ស្វែងរកនិទ្ទេស Letter Grade ស្វ័យប្រវត្តិផ្អែកលើពិន្ទុជាក់ស្តែង"""
        if self.score is None:
            return None
        if self.score >= 90:
            return 'A'
        elif self.score >= 80:
            return 'B'
        elif self.score >= 70:
            return 'C'
        elif self.score >= 60:
            return 'D'
        else:
            return 'F'

    def save(self, *args, **kwargs):
        """គណនា Grade មុនពេល Save ចូល Database"""
        if self.score is not None and not self.grade:
            self.grade = self.calculate_grade()
        super().save(*args, **kwargs)

