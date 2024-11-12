from django.contrib import admin

# Register your models here.

from .models import Department, Employee, Profile, QuestionCategory, Question, Evaluation, Answer


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'file_number', 'job_title', 'get_job_rank_display', 'department')
    search_fields = ('name', 'file_number', 'job_title')
    list_filter = ('job_rank', 'department')
    
    def get_job_rank_display(self, obj):
        return obj.get_job_rank_display()
    
    get_job_rank_display.short_description = 'Job Rank'


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'department')


@admin.register(QuestionCategory)
class QuestionCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_job_rank_display')
    list_filter = ('job_rank',)
    
    def get_job_rank_display(self, obj):
        return obj.get_job_rank_display()
    
    get_job_rank_display.short_description = 'Job Rank'


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'category', 'order')
    list_filter = ('category',)
    search_fields = ('text',)


@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ('employee', 'evaluator', 'date', 'month', 'total_score')
    search_fields = ('employee__name', 'evaluator__username')
    list_filter = ('month',)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('evaluation', 'question', 'choice')
    list_filter = ('evaluation', 'question')
    
#cloner174