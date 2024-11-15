from django.db import models

# Create your models here.

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.models import Group

JOB_RANK_GROUPS = {
    0: 'مدیر ارشد',  # Senior Manager
    1: 'مدیر',       # Manager
    2: 'کارمند',     # Employee
}


class Department(models.Model):
    
    name = models.CharField(max_length=100, unique=True)
    manager = models.ForeignKey(
        'Employee',
        related_name='managed_departments',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text='مدیر دپارتمان'
    )
    
    def __str__(self):
        return self.name
    

class JobRank(models.Model):
    
    name = models.CharField(max_length=100, unique=True, default='کارمند')
    
    def __str__(self):
        return self.name
    


class Employee(models.Model):
    
    JOB_RANK_CHOICES = [
        (0, 'مدیر ارشد'),       # Karshenas
        (1, 'مدیر'),          # Modir
        (2, 'کارمند'),        # Karmand
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    file_number = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    job_rank = models.ForeignKey(JobRank, null=True, on_delete=models.SET_NULL)
    job_title = models.CharField(max_length=100)
    department = models.ForeignKey(Department, null=True, blank=True, on_delete=models.SET_NULL)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the Employee instance first
        
        if self.user:
            # Get the group name based on the job rank
            group_name = JOB_RANK_GROUPS.get(self.job_rank)
            if group_name:
                # Get or create the corresponding group
                group, created = Group.objects.get_or_create(name=group_name)
                # Remove the user from all job rank groups
                for name in JOB_RANK_GROUPS.values():
                    group_to_remove = Group.objects.filter(name=name).first()
                    if group_to_remove:
                        self.user.groups.remove(group_to_remove)
                # Add the user to the correct group
                self.user.groups.add(group)
                self.user.save()
    
    def __str__(self):
        return f"{self.name} ({self.file_number})"



    


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    department = models.ForeignKey(Department, null=True, blank=True, on_delete=models.SET_NULL)
    job_rank = models.ForeignKey(JobRank, null=True, blank=True, on_delete=models.SET_NULL)
    group = models.ForeignKey(Group, null=True, blank=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return self.user.username
    


class QuestionCategory(models.Model):
    name = models.CharField(max_length=100)
    job_rank = models.ForeignKey(JobRank, null=True, blank=True, on_delete=models.SET_NULL)
    
    class Meta:
        unique_together = ('name', 'job_rank')
    
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
    else:
        instance.profile.save()
    # Update the profile's group
    groups = instance.groups.all()
    if groups.exists():
        # Assuming the user has only one job rank group
        instance.profile.group = groups.first()
        instance.profile.save()

#cloner174