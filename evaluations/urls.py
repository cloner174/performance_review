#
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/create/', views.create_employee, name='create_employee'),
    path('employees/<int:employee_id>/evaluate/', views.evaluate_employee, name='evaluate_employee'),
    path('evaluations/<int:evaluation_id>/', views.view_evaluation, name='view_evaluation'),
    path('evaluations/<int:evaluation_id>/export/', views.export_evaluation_to_excel, name='export_evaluation_to_excel'),
    path('my-evaluations/', views.view_own_evaluations, name='view_own_evaluations'),
]
#cloner174