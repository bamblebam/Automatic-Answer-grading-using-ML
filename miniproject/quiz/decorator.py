from functools import wraps
from django.core.exceptions import PermissionDenied


def is_teacher(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.is_teacher:
            return function(request, *args, **kwargs)
        raise PermissionDenied
    return wrap
