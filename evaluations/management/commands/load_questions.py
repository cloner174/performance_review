#به نام خدا

from django.core.management.base import BaseCommand
from evaluations.models import QuestionCategory, Question
from django.db import transaction


class Command(BaseCommand):
    
    help = 'Load initial questions into the database'
    
    def handle(self, *args, **options):
        data = [
            {
                'job_rank': 0,  # کارشناس (Karshenas)
                'categories': [
                    {
                        'name': 'دانش، مهارت وتوانایی',
                        'questions': [
                            'روحیه همکاری و مشارکت',
                            'نوآوری و خلاقیت و حل مسئله',
                            'برنامه‌ریزی و مدیریت زمان',
                            'ارتقاء دانش تخصصی و ظرفیت یادگیری',
                            'استفاده بهینه از منابع',
                            'مهارت‌های ارتباطی و مذاکره و متقاعدسازی',
                        ],
                    },
                    {
                        'name': 'نتایج عملکردی',
                        'questions': [
                            'تکریم ارباب رجوع (درون و برون سازمانی)',
                            'پیشبرد به موقع کارهای محوله و تفکر سیستمی',
                            'کمیت کار و سرعت عمل در انجام کار',
                            'دقت عمل و تمرکز در کار',
                            'مشارکت در عملکرد واحد',
                            'کیفیت کار، جدیت در کار و مسئولیت‌پذیری',
                        ],
                    },
                ],
            },
            {
                'job_rank': 1,  # مدیر (Modir)
                'categories': [
                    {
                        'name': 'دانش، مهارت و توانایی',
                        'questions': [
                            'روحیه همکاری، همراهی و حل تعارض',
                            'نوآوری و خلاقیت',
                            'مشارکت جویی',
                            'مدیریت تغییر، ارتقاء دانش و ظرفیت یادگیری',
                            'توانایی هدایت و رهبری کارکنان زیرمجموعه',
                            'مهارت‌های ارتباطی و مذاکره و متقاعدسازی',
                        ],
                    },
                    {
                        'name': 'نتایج عملکردی',
                        'questions': [
                            'تصمیم‌گیری، حل مسئله و تفکر سیستمی',
                            'سازمان‌دهی و تخصیص بهینه منابع در دسترس',
                            'برنامه‌ریزی و هدف‌گذاری',
                            'نظارت و کنترل',
                            'توسعه و توانمندسازی کارکنان',
                            'مسئولیت‌پذیری و نتیجه‌گرایی در انجام وظایف مورد انتظار',
                        ],
                    },
                ],
            },
            {
                'job_rank': 2,  # کارمند (Karmand)
                'categories': [
                    {
                        'name': 'دانش، مهارت و توانایی',
                        'questions': [
                            'همکاری و مشارکت',
                            'انعطاف‌پذیری و استفاده بهینه از منابع',
                            'ارتقاء دانش و علاقه به یادگیری',
                            'مهارت‌های ارتباطی',
                        ],
                    },
                    {
                        'name': 'نتایج عملکردی',
                        'questions': [
                            'تکریم ارباب رجوع (درون و برون سازمانی)',
                            'انجام و پیگیری به موقع کارهای محوله',
                            'کیفیت، دقت، سرعت و تمرکز در انجام کار',
                            'دقت عمل و تمرکز در کار',
                            'مشارکت در بهبود عملکرد واحد',
                            'جدیت و مسئولیت‌پذیری',
                        ],
                    },
                ],
            },
            {
                'job_rank': 3,  # کارگر (Kargar)
                'categories': [
                    {
                        'name': 'دانش، مهارت و توانایی',
                        'questions': [
                            'همکاری و مشارکت',
                            'استفاده بهینه از منابع',
                            'ارتقاء دانش و علاقه به یادگیری',
                            'مهارت‌های ارتباطی',
                        ],
                    },
                    {
                        'name': 'نتایج عملکردی',
                        'questions': [
                            'انجام و پیگیری به موقع کارهای محوله',
                            'کیفیت، دقت، سرعت و تمرکز در انجام کار',
                            'مشارکت در بهبود عملکرد واحد',
                            'جدیت و مسئولیت‌پذیری',
                        ],
                    },
                ],
            },
        ]
        
        with transaction.atomic():
            for entry in data:
                job_rank = entry['job_rank']
                for category_data in entry['categories']:
                    category_name = category_data['name']
                    category, created = QuestionCategory.objects.get_or_create(
                        name=category_name,
                        job_rank=job_rank
                    )
                    for order, question_text in enumerate(category_data['questions'], start=1):
                        Question.objects.get_or_create(
                            category=category,
                            text=question_text,
                            order=order
                        )
        
        self.stdout.write(self.style.SUCCESS('Successfully loaded questions'))
    
#cloner174