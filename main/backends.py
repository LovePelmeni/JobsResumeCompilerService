from django.contrib.auth import backends


class UserAuthorizationBackend(backends.BaseBackend):

    def authenticate(self, username=None, password=None):
        pass


