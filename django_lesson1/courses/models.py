from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Course(models.Model):
    """Model សម្រាប់ផ្ទុកព័ត៌មានវគ្គសិក្សា/មុខវិជ្ជា"""
    
    LEVEL_CHOICES = [
        ('100', 'ឆ្នាំទី ១ (Beginner)'),
        ('200', 'ឆ្នាំទី ២ (Intermediate)'),
        ('300', 'ឆ្នាំទី ៣ (Advanced)'),
        ('400', 'ឆ្នាំទី ៤ (Expert)'),
    ]
    
    STATUS_CHOICES = [
        ('ACTIVE', 'កំពុងបង្រៀន (Active)'),
        ('INACTIVE', 'ផ្អាក (Inactive)'),
        ('ARCHIVED', 'ទុកជាឯកសារ (Archived)'),
    ]
    
    code = models.CharField(max_length=20, unique=True, help_text="កូដមុខវិជ្ជា (ឧ. IT-101)")
    title = models.CharField(max_length=200, help_text="ឈ្មោះមុខវិជ្ជា")
    description = models.TextField(help_text="ការពិពណ៌នាមុខវិជ្ជា")
    instructor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='courses_taught')
    credits = models.PositiveIntegerField(default=3, help_text="ចំនួនក្រេឌីត")
    level = models.CharField(max_length=3, choices=LEVEL_CHOICES, default='100')
    capacity = models.PositiveIntegerField(default=40, help_text="ចំនួននិស្សិតអតិបរមា")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ACTIVE')
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['code']
        verbose_name_plural = "Courses"

    def __str__(self):
        return f"{self.code} - {self.title}"

    def get_absolute_url(self):
        return reverse('courses:course_detail', kwargs={'pk': self.pk})

    @property
    def is_available(self):
        return self.status == 'ACTIVE'
