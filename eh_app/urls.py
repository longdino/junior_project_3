from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('students', views.studentList, name='student_list'),
	path('override_final', views.override_final, name='override_status'),
]
