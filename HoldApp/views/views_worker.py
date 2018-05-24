from django.contrib.auth.decorators import user_passes_test


def is_worker(user):
    return user.groups.filter(name='Worker').exists() | user.groups.filter(name='Admin').exists()
