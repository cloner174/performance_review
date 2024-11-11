from django.db import models

# Create your models here.

from django.contrib.auth.models import User


class Employee(models.Model):
    
    file_number = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    job_title = models.CharField(max_length=100)
    job_rank = models.IntegerField(choices=[
        (0, 'کارشناس'),
        (1, 'کارشناس ارشد'),
        (2, 'مدیر'),
        (3, 'کارگر'),
    ])
    
    def __str__(self):
        return f"{self.name} ({self.file_number})"


class QuestionCategory(models.Model):
    
    name = models.CharField(max_length=100)
    job_rank = models.IntegerField()
    
    def __str__(self):
        return self.name


class Question(models.Model):
    
    category = models.ForeignKey(QuestionCategory, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    job_rank = models.IntegerField()
    order = models.IntegerField()
    
    def __str__(self):
        return f"{self.text} (Rank {self.job_rank})"


class Evaluation(models.Model):
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    evaluator = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    month = models.IntegerField()
    scores = models.JSONField(default=dict)  # نتایج شخصی و کلی ذخیره 
    
    def __str__(self):
        return f"Evaluation of {self.employee.name} on {self.date}"


class Answer(models.Model):
    
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.IntegerField(choices=[
        (5, 'عالی'),
        (4, 'بسیار خوب'),
        (3, 'خوب'),
        (2, 'متوسط'),
        (1, 'ضعیف'),
    ])
    
    def __str__(self):
        return f"{self.question.text}: {self.get_choice_display()}"
    
#cloner174