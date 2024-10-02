from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in

from apps.tech_persons.models import UserEmployee, Employee

@receiver(post_migrate)
def cria_grupos_iniciais(sender, **kwargs):
    grupos = ['Administradores', 'Aprovadores TI', 'Suporte', 'TH', 'Basico', 'Move GPOS']
    
    for grupo in grupos:
        Group.objects.get_or_create(name=grupo)

@receiver(user_logged_in)
def create_or_update_user_employee(sender, user, request, **kwargs):
    employee_id = request.session.get('employeeId', None)
    
    if employee_id and "_" in employee_id:
        matricula = employee_id.split("_", 1)[1]
        
        if Employee.objects.filter(matricula=matricula).exists():
            employee = Employee.objects.get(matricula=matricula)
            
            if employee:
                # Cria ou atualiza o UserEmployee
                user_employee, created = UserEmployee.objects.update_or_create(
                    user=user,
                    defaults={
                        'employee': employee,
                        'emp_id': employee_id
                    }
                )
                
                if created:
                    print(f'DEBUG :: CREATE EMPLOYEE USER {user_employee}')