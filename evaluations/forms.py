#
from django import forms
from .models import Question, QuestionCategory, Answer


class EvaluationForm(forms.Form):
    def __init__(self, *args, **kwargs):
        job_rank = kwargs.pop('job_rank', None)
        super().__init__(*args, **kwargs)

        # Fetch questions grouped by category
        categories = QuestionCategory.objects.filter(job_rank=job_rank)
        self.categories = []

        for category in categories:
            questions = Question.objects.filter(category=category)
            self.categories.append({
                'category': category,
                'questions': questions,
            })
            for question in questions:
                field_name = f"question_{question.id}"
                self.fields[field_name] = forms.ChoiceField(
                    choices = Answer.CHOICES,
                    widget=forms.RadioSelect,
                    label=question.text,
                )


from .models import Employee, Department, JobRank

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['file_number', 'name', 'job_title', 'job_rank', 'department']

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name']

class JobRankForm(forms.ModelForm):
    class Meta:
        model = JobRank
        fields = ['name']

#cloner174