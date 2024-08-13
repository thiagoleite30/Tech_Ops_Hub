from django.core.exceptions import PermissionDenied
from functools import wraps

from django.shortcuts import redirect

def group_required(group_name, redirect_url=None):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated and request.user.groups.filter(name=group_name).exists():
                return view_func(request, *args, **kwargs)
            if redirect_url:
                return redirect(redirect_url)
            raise PermissionDenied  # ou redirecione para outra página
        return _wrapped_view
    return decorator