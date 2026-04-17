from django.urls import path
from .views import (
    home,
    UploadStudentsView, 
    StudentListView, 
    SendEmailsView,
    SendCustomTemplateView,
    DeleteStudentView,
    DeleteAllStudentsView,
    AddStudentView
)

urlpatterns = [
    path('', home, name='home'),
    path('upload/', UploadStudentsView.as_view()),
    path('students/', StudentListView.as_view()),
    path('send-emails/', SendEmailsView.as_view()),
    path('send-template/', SendCustomTemplateView.as_view()),
    path('add-student/', AddStudentView.as_view()),
    path('delete-student/<int:student_id>/', DeleteStudentView.as_view()),
    path('delete-all/', DeleteAllStudentsView.as_view()),
]