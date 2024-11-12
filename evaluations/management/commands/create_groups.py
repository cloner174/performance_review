#
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from evaluations.models import Evaluation

class Command(BaseCommand):
    
    help = 'Create default groups and assign permissions'
    def handle(self, *args, **options):
        # Define groups
        groups = {
            'Employee': [],
            'Manager': [],
            'General Manager': [],
        }
        
        evaluation_content_type = ContentType.objects.get_for_model(Evaluation)
        
        permissions = {
            'view_own_evaluation': Permission.objects.get(codename='view_own_evaluation', content_type=evaluation_content_type),
            'edit_department_evaluation': Permission.objects.get(codename='edit_department_evaluation', content_type=evaluation_content_type),
            'view_all_evaluations': Permission.objects.get(codename='view_all_evaluations', content_type=evaluation_content_type),
        }
        
        groups['Employee'].append(permissions['view_own_evaluation'])
        
        groups['Manager'].extend([
            permissions['view_own_evaluation'],
            permissions['edit_department_evaluation'],
        ])
        
        groups['General Manager'].extend([
            permissions['view_own_evaluation'],
            permissions['edit_department_evaluation'],
            permissions['view_all_evaluations'],
        ])
        
        for group_name, perms in groups.items():
            group, created = Group.objects.get_or_create(name=group_name)
            group.permissions.set(perms)
            group.save()
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created group "{group_name}"'))
            else:
                self.stdout.write(f'Updated group "{group_name}" with permissions.')
        
        self.stdout.write(self.style.SUCCESS('Successfully created/updated groups and permissions'))
    
#cloner174