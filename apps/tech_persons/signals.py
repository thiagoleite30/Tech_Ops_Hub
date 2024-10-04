
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in

from apps.tech_assets.services import get_employedId
from apps.tech_persons.models import UserEmployee, Employee


@receiver(user_logged_in)
def get_emp_id(sender, user, request, **kwargs):
    if request.user.is_authenticated:
        if 'employeeId' not in request.session:
            employeeId = get_employedId(request.user)
            request.session['employeeId'] = employeeId
        else:
            employeeId = request.session['employeeId']
        
    else:
        employeeId = None
    return {'employeeId': employeeId}


@receiver(user_logged_in)
def create_or_update_user_employee(sender, user, request, **kwargs):
    employee_id = request.session['employeeId']

    print(f'DEBUG :: CREATE EMPLOYEE USER :: CHAMOU O SIGNAL :: EMP_ID {employee_id}')
    
    if employee_id and "_" in employee_id:
        matricula = employee_id.split("_", 1)[1]
        print(f'DEBUG :: CREATE EMPLOYEE USER :: TEM MATRICULA {matricula}')
        
        if Employee.objects.filter(matricula=matricula).exists():
            
            employee = Employee.objects.get(matricula=matricula)
            print(f'DEBUG :: CREATE EMPLOYEE USER :: EXISTE EMPLOYEE {employee}')
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