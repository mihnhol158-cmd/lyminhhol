from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('', views.student_list, name='student_list'),
    path('register/', views.register_student, name='register'),
    path('<int:pk>/', views.student_detail, name='student_detail'),
    path('<int:pk>/update/', views.student_update, name='student_update'),
    path('cbv/list/', views.StudentListView.as_view(), name='student_list_cbv'),
    path('cbv/create/', views.StudentCreateView.as_view(), name='student_create_cbv'),
]
