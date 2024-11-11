from django.db import models

# Create your models here.

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Department(models.Model):
    
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name


class Employee(models.Model):
    
    JOB_RANK_CHOICES = [
        (0, 'کارشناس'),       # Karshenas
        (1, 'مدیر'),          # Modir
        (2, 'کارمند'),        # Karmand
        (3, 'کارگر'),         # Kargar
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    file_number = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    job_rank = models.IntegerField(choices=JOB_RANK_CHOICES, null=True)
    job_title = models.CharField(max_length=100)
    department = models.ForeignKey(Department, null=True, blank=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return f"{self.name} ({self.file_number})"


class Profile(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    department = models.ForeignKey(Department, null=True, blank=True, on_delete=models.SET_NULL)
    # سایر مشخصات اگر نیازه اضافه بشه
    
    def __str__(self):
        return self.user.username


class QuestionCategory(models.Model):
    
    name = models.CharField(max_length=100)
    job_rank = models.IntegerField(choices=Employee.JOB_RANK_CHOICES, null=True)
    
    def __str__(self):
        return f"{self.name} - {self.get_job_rank_display()}"


class Question(models.Model):
    
    category = models.ForeignKey(QuestionCategory, on_delete=models.CASCADE, null=True)
    text = models.CharField(max_length=500)
    order = models.IntegerField(null=True)
    
    def __str__(self):
        return f"{self.text} (Order {self.order})"


class Evaluation(models.Model):
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)
    evaluator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date = models.DateField(auto_now_add=True, null=True)
    month = models.IntegerField(null=True)
    total_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    scores = models.JSONField(default=dict)
    
    def __str__(self):
        return f"Evaluation of {self.employee.name} on {self.date}"
    
    class Meta:
        permissions = [
            ('view_own_evaluation', 'Can view own evaluation'),
            ('edit_department_evaluation', 'Can edit department evaluations'),
            ('view_all_evaluations', 'Can view all evaluations'),
        ]


class Answer(models.Model):
    
    CHOICES = [
        (5, 'عالی'),
        (4, 'بسیار خوب'),
        (3, 'خوب'),
        (2, 'متوسط'),
        (1, 'ضعیف'),
    ]
    
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE, null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    choice = models.IntegerField(choices=CHOICES, null=True)
    
    def __str__(self):
        return f"{self.question.text}: {self.get_choice_display()}"
    

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
#cloner174