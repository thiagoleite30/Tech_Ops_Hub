from django import template

from setup import settings

register = template.Library()

@register.filter
def subtract(value, arg):
    return value - arg

@register.filter
def pegar_matricula_empId(value):
    if value != None and "_" in value:
        return value.split("_", 1)[1]
    return value

@register.filter
def checa_resposta_termos(value):
    if value == 'recusado':
        return "bg-danger"
    elif value == 'aceito':
        return "bg-success"
    else:
        return "bg-primary"

@register.filter
def checa_resposta_aprovacoes(value):
    if value == 'reprovado':
        return "bg-danger"
    elif value == 'aprovado':
        return "bg-success"
    else:
        return "bg-primary"

@register.filter
def _move_gposcheca_status_solicitacoes(value):
    if value:
        return "bg-success"
    else:
        return "bg-primary"