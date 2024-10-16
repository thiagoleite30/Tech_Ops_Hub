
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
    
    if employee_id and "_" in employee_id:
        matricula = employee_id.split("_", 1)[1]
        
        if Employee.objects.filter(matricula=matricula).exists():
            
            employee = Employee.objects.get(matricula=matricula)

            if employee:
                # Cria ou atualiza o UserEmployee
                user_employee, _ = UserEmployee.objects.update_or_create(
                    user=user,
                    defaults={
                        'employee': employee,
                        'emp_id': employee_id
                    }
                )
