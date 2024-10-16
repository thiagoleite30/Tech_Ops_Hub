from django import template
from user_agents import parse
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
        return "border-danger mb-3"
    elif value == 'aceito':
        return "border-success mb-3"
    else:
        return "border-primary mb-3"


@register.filter
def checa_resposta_aprovacoes(value):
    if value == 'reprovado':
        return "border-danger mb-3"
    elif value == 'aprovado':
        return "border-success mb-3"
    else:
        return "border-primary mb-3"


@register.filter
def _move_gposcheca_status_solicitacoes(value):
    if value:
        return "border-success mb-3"
    else:
        return "border-primary mb-3"


@register.simple_tag(takes_context=True)
def get_cards_per_slide(context):

    request = context['request']
    user_agent = request.META['HTTP_USER_AGENT']
    user_agent_parsed = parse(user_agent)

    if user_agent_parsed.is_mobile:
        return 1
    elif user_agent_parsed.is_tablet:
        return 3
    elif user_agent_parsed.is_pc:
        return 5
