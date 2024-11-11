from django import forms
from .models import Employee, Evaluation, Answer, Question


class EvaluationForm(forms.Form):
    def __init__(self, *args, **kwargs):
        job_rank = kwargs.pop('job_rank')
        super().__init__(*args, **kwargs)
        # Load questions based on job_rank
        questions = Question.objects.filter(category__job_rank=job_rank).order_by('order')
        for question in questions:
            self.fields[f'question_{question.id}'] = forms.ChoiceField(
                label=question.text,
                choices=[
                    (5, 'عالی'),
                    (4, 'بسیار خوب'),
                    (3, 'خوب'),
                    (2, 'متوسط'),
                    (1, 'ضعیف'),
                ],
                widget=forms.RadioSelect(),
                initial=3,  # 'خوب'
            )
    
#cloner174