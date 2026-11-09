

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator

class Student(models.Model):
    """Model សម្រាប់ផ្ទុកព័ត៌មាននិស្សិត"""
    
    GENDER_CHOICES = [
        ('M', 'ប្រុស (Male)'),
        ('F', 'ស្រី (Female)'),
        ('O', 'ផ្សេងទៀត (Other)'),
    ]
    
    # One-to-One ភ្ជាប់ជាមួយ Django Built-in User Account
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student')
    student_id = models.CharField(max_length=20, unique=True, help_text="អត្តលេខនិស្សិត (ឧ. BBU2026001)")
    
    # ឈ្មោះជាភាសាខ្មែរ (Primary Name)
    khmer_name = models.CharField(max_length=150, blank=True, default='', verbose_name="ឈ្មោះជាភាសាខ្មែរ")
    
    date_of_birth = models.DateField(verbose_name="ថ្ងៃខែឆ្នាំកំណើត")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="ភេទ")
    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="លេខទូរស័ព្ទ")
    address = models.TextField(verbose_name="អាសយដ្ឋាន")
    city = models.CharField(max_length=100, verbose_name="រាជធានី/ខេត្ត")
    country = models.CharField(max_length=100, default='Cambodia', verbose_name="ប្រទេស")
    
    # រូបថតសិស្ស (Media file)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True, verbose_name="រូបថតសិស្ស")
    
    enrollment_date = models.DateField(auto_now_add=True)
    gpa = models.DecimalField(max_digits=3, decimal_places=2, default=0.00,
                              validators=[MinValueValidator(0), MaxValueValidator(4)])
    is_active = models.BooleanField(default=True, verbose_name="ស្ថានភាពសកម្ម")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['student_id']
        verbose_name_plural = "Students"
        indexes = [
            models.Index(fields=['student_id']),
            models.Index(fields=['khmer_name']),
        ]

    def get_primary_name(self):
        """ផ្តល់អាទិភាពបង្ហាញឈ្មោះខ្មែរមុន ប្រសិនបើគ្មាន ទើបបង្ហាញឈ្មោះឡាតាំង"""
        if self.khmer_name:
            return self.khmer_name
        full_name = self.user.get_full_name()
        return full_name if full_name else self.user.username

    def __str__(self):
        return f"{self.student_id} - {self.get_primary_name()}"

    def get_absolute_url(self):
        return reverse('students:student_detail', kwargs={'pk': self.pk})
