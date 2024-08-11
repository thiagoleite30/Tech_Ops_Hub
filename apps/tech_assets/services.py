from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE


def register_logentry(instance, action, **kwargs):
    usuario=kwargs.get('user', None)
    content_type = ContentType.objects.get_for_model(instance)
    object_id=instance.pk
    if action == ADDITION:
        details = f"O objeto {content_type.model} ID '{instance.pk}' foi criada pelo usuário {usuario}"
    elif action == CHANGE:
        details = f"O objeto {content_type.model} ID '{instance.pk}' foi modificado pelo usuário {usuario}"
    else:
        object_id=kwargs.get('foto_id', None)
        details = f"O objeto {content_type.model} ID '{instance.pk}' foi deletado pelo usuário {usuario}"

    print(details)
    # Salvar no log 
    LogEntry.objects.create(
        user=usuario,
        content_type=content_type,
        object_id=object_id,
        object_repr=str(instance),
        action_flag=action,
        change_message=details
    )