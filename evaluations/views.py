from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponse, HttpResponseForbidden
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from django.views import View

from .models import Employee, Evaluation, Answer, Question, Department, Profile
from .forms import EvaluationForm

import openpyxl


@login_required
def home(request):
    user = request.user
    if user.is_superuser:
        return redirect('/admin/')
    if is_employee(user):
        return redirect('view_own_evaluations')
    elif is_manager(user) or is_general_manager(user):
        return redirect('employee_list')
    else:
        return render(request, 'evaluations/unauthorized.html')


def is_employee(user):
    return user.groups.filter(name='کارمند').exists()


def is_manager(user):
    return user.groups.filter(name='مدیر').exists()


def is_general_manager(user):
    return user.groups.filter(name='مدیر ارشد').exists()


def user_department(user):
    return user.profile.department if hasattr(user, 'profile') else None


@login_required
def employee_list(request):
    if is_general_manager(request.user):
        employees = Employee.objects.all()
    elif is_manager(request.user):
        department = user_department(request.user)
        employees = Employee.objects.filter(department=department)
    else:
        raise PermissionDenied
    
    return render(request, 'evaluations/employee_list.html', {'employees': employees})


@login_required
def create_employee(request):
    if not is_general_manager(request.user):
        raise PermissionDenied
    
    if request.method == 'POST':
        file_number = request.POST.get('file_number')
        name = request.POST.get('name')
        job_title = request.POST.get('job_title')
        job_rank = request.POST.get('job_rank')
        department_id = request.POST.get('department')
        
        username = f"user_{file_number}"
        password = User.objects.make_random_password()
        user = User.objects.create_user(username=username, password=password)
        
        employee_group = Group.objects.get(name='کارمند')
        user.groups.add(employee_group)
        
        employee = Employee.objects.create(
            user=user,
            file_number=file_number,
            name=name,
            job_title=job_title,
            job_rank=job_rank,
            department_id=department_id
        )
        
        if hasattr(user, 'profile'):
            user.profile.department_id = department_id
            user.profile.save()
        else:
            Profile.objects.create(user=user, department_id=department_id)
        # send_mail(
        #     'اطلاعات ورود به سیستم',
        #     f'نام کاربری: {username}\nرمز عبور: {password}',
        #     'from@example.com',
        #     [user.email],
        # )
        return redirect('employee_list')
    
    else:
        departments = Department.objects.all()
        return render(request, 'evaluations/create_employee.html', {'departments': departments})


@login_required
def evaluate_employee(request, employee_id):
    
    employee = get_object_or_404(Employee, id=employee_id)
    user = request.user
    
    if is_general_manager(user):
        pass
    elif is_manager(user):
        if employee.department != user_department(user):
            raise PermissionDenied
    else:
        raise PermissionDenied
    
    if request.method == 'POST':
        form = EvaluationForm(request.POST, job_rank=employee.job_rank)
        if form.is_valid():
            month = int(request.POST.get('month', timezone.now().month))
            evaluation = Evaluation.objects.create(
                employee=employee,
                evaluator=user,
                month=month
            )
            total_questions = 0
            scores = [0]*5  # Index 0 for 'عالی', Index 4 for 'ضعیف'
            for field_name, value in form.cleaned_data.items():
                question_id = field_name.split('_')[1]
                question = Question.objects.get(id=question_id)
                choice = int(value)
                Answer.objects.create(
                    evaluation=evaluation,
                    question=question,
                    choice=choice
                )
                index = 5 - choice  # معکوس
                scores[index] += 1
                total_questions += 1
            # محاسبه امتیاز
            weights = [100, 80, 70, 60, 50]
            weighted_scores = [(scores[i] * weights[i]) / total_questions for i in range(5)]
            total_score = sum(weighted_scores)
            evaluation.scores = {
                'individual_scores': weighted_scores,
                'total_score': total_score
            }
            evaluation.total_score = total_score
            evaluation.save()
            return redirect('view_evaluation', evaluation_id=evaluation.id)
    else:
        form = EvaluationForm(job_rank=employee.job_rank)
    
    return render(request, 'evaluations/evaluate_employee.html', {
        'employee': employee,
        'form': form,
    })


@login_required
def view_evaluation(request, evaluation_id):
    evaluation = get_object_or_404(Evaluation, id=evaluation_id)
    user = request.user
    
    if is_general_manager(user):
        pass
    elif is_manager(user):
        if evaluation.employee.department != user_department(user):
            raise PermissionDenied
    elif is_employee(user):
        if evaluation.employee.user != user:
            raise PermissionDenied
    else:
        raise PermissionDenied
    
    answers = Answer.objects.filter(evaluation=evaluation)
    return render(request, 'evaluations/view_evaluation.html', {
        'evaluation': evaluation,
        'answers': answers,
    })


@login_required
def export_evaluation_to_excel(request, evaluation_id):
    evaluation = get_object_or_404(Evaluation, id=evaluation_id)
    user = request.user
    
    if is_general_manager(user):
        pass
    
    elif is_manager(user):
        if evaluation.employee.department != user_department(user):
            raise PermissionDenied
    
    elif is_employee(user):
        if evaluation.employee.user != user:
            raise PermissionDenied
    else:
        raise PermissionDenied
    
    answers = Answer.objects.filter(evaluation=evaluation)
    
    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet.title = 'Evaluation'
    
    sheet['A1'] = 'شرح عوامل ارزیابی'
    sheet['B1'] = 'امتیاز'
    
    for idx, answer in enumerate(answers, start=2):
        sheet.cell(row=idx, column=1).value = answer.question.text
        sheet.cell(row=idx, column=2).value = answer.get_choice_display()
    
    idx += 1
    sheet.cell(row=idx, column=1).value = 'مجموع امتیازات'
    sheet.cell(row=idx, column=2).value = evaluation.total_score
    
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    filename = f"evaluation_{evaluation.employee.file_number}_{evaluation.month}.xlsx"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    wb.save(response)
    return response


@login_required
def view_own_evaluations(request):
    user = request.user
    if not is_employee(user):
        raise PermissionDenied
    
    evaluations = Evaluation.objects.filter(employee__user=user)
    return render(request, 'evaluations/own_evaluations.html', {'evaluations': evaluations})
#cloner174