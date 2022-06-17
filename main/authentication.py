from rest_framework import authentication


class JWTAuthenticationClass(authentication.BaseAuthentication):

    def authenticate(self, request):
        pass