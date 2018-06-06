from django.conf import settings
from django.shortcuts import redirect


def is_worker(user):
    if not user.groups.filter(name='Worker').exists() | user.groups.filter(name='Admin').exists():
        return redirect(settings.LOGIN_URL)

class LoginRequiredMiddleware:
    # TODO: Why no work?
    def is_worker(user):
        if not user.groups.filter(name='Worker').exists() | user.groups.filter(name='Admin').exists():
            return redirect(settings.LOGIN_URL)

