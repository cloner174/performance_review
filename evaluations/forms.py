#
from django import forms
from .models import Question, QuestionCategory


class EvaluationForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        job_rank = kwargs.pop('job_rank')
        super().__init__(*args, **kwargs)
        self.categories = []
        categories = QuestionCategory.objects.filter(job_rank=job_rank)
        for category in categories:
            category_fields = []
            questions = category.question_set.order_by('order')
            for question in questions:
                field_name = f'question_{question.id}'
                self.fields[field_name] = forms.ChoiceField(
                    label=question.text,
                    choices=[
                        (5, 'عالی'),
                        (4, 'بسیار خوب'),
                        (3, 'خوب'),
                        (2, 'متوسط'),
                        (1, 'ضعیف'),
                    ],
                    widget=forms.RadioSelect(),
                    initial=3,
                )
                category_fields.append(self[field_name])
            
            self.categories.append({'name': category.name, 'fields': category_fields})
    
#cloner174