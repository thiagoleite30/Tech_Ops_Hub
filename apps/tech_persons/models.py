from django.db import models
from django.contrib.auth.models import User

from apps.tech_assets.models import CostCenter

    
class Employee(models.Model):
    setor = models.CharField(max_length=255, blank=True, null=True)
    filial = models.CharField(max_length=100)
    matricula = models.CharField(max_length=100)
    nome = models.CharField(max_length=255)
    cpf = models.CharField(max_length=100, unique=True)
    cargo = models.CharField(max_length=255, blank=True, null=True)
    centro_custo = models.ForeignKey(
        CostCenter, on_delete=models.SET_NULL, null=True)
    situacao = models.CharField(max_length=100)
    situacao_data_fim = models.DateField(null=True, blank=True)
    data_registro = models.DateField(auto_now_add=True, null=True, blank=True)
    ultima_alteracao = models.DateField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f'{self.matricula}'

class UserEmployee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    emp_id = models.CharField(
        max_length=100, blank=True, null=True)  # Campo para employeeId

    def __str__(self):
        return self.user.username
