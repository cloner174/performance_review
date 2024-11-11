from django.core.management.base import BaseCommand
from evaluations.models import Question, QuestionCategory


class Command(BaseCommand):
    
    help = 'Load initial questions and categories into the database'
    
    def handle(self, *args, **options):
        # گروه بندی ها و رده بندی ها و سوالات مربوطه
        data = [
            {
                'job_rank': 0,
                'category_name': 'شاخص‌های عملکردی کارشناس',
                'questions': [
                    'روحیه همکاری ومشارکت',
                    'نو آوری وخلاقیت وحل مسئله',
                    #  سایر سوالات رنک 0 اینجا
                ]
            },
            # سایر شغل ها اینجا
        ]
        
        for entry in data:
            category, _ = QuestionCategory.objects.get_or_create(
                name=entry['category_name'],
                job_rank=entry['job_rank']
            )
            for order, text in enumerate(entry['questions'], start=1):
                Question.objects.get_or_create(
                    category=category,
                    text=text,
                    job_rank=entry['job_rank'],
                    order=order
                )
        
        self.stdout.write(self.style.SUCCESS('Successfully loaded questions and categories'))
    
#cloner174