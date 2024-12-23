from django.core.exceptions import PermissionDenied
from functools import wraps

from django.shortcuts import redirect

from apps.tech_persons.models import UserEmployee

def group_required(group_name, redirect_url=None):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated and request.user.groups.filter(name__in=group_name).exists():
                return view_func(request, *args, **kwargs)
            if redirect_url:
                print(f'OS GRUPOS QUE VOCE ESTA SAO: {group_name}')
                return redirect(redirect_url)
            raise PermissionDenied  # ou redirecione para outra página
        return _wrapped_view
    return decorator


def employee_required(redirect_url=None):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user = request.user
            if not UserEmployee.objects.filter(user=user).exists():
                return redirect(redirect_url)
            else:
                return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator