import django.core.exceptions
from django.contrib.auth import backends, login


class UserAuthorizationBackend(backends.BaseBackend):

    def authenticate(self, username=None, password=None):
        try:
            user = models.Customer.objects.get(username=username)
            if user.check_password(raw_password=password) and not user.is_staff:
                login(request, user, backend=getattr(settings, 'AUTHENTICATION_BACKENDS')[0])
                return user
            return None
        except(django.core.exceptions.ObjectDoesNotExist):
            return None

class AdminAuthorizationBackend(backends.BaseBackend):

    def authenticate(self, request, **kwargs):
        try:
            user = models.Customer.objects.get(username=username)
            if not user.check_password(raw_password=password) and user.is_staff:
                login(request, user=user, backend=getattr(settings, 'AUTHENTICATION_BACKENDS')[0])
                return user
            return None
        except(django.core.exceptions.ObjectDoesNotExist):
            return None