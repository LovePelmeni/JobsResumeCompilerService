from rest_framework import authentication
import django.core.exceptions, jwt

class JWTAuthenticationClass(authentication.BaseAuthentication):

    def get_authorization_header(self, request):
        return request.META.get('Authorization')

    def authenticate(self, request):
        try:
            if not self.get_authorization_header(request):
                raise django.core.exceptions.PermissionDenied()

            header = self.get_authorization_header(request)
            jwt_token = jwt.decode(header, algorithms='HS256')
            if jwt_token['user_id'] in models.Customer.objects.values_list('id', flat=True):
                return django.core.exceptions.PermissionDenied()
            return True

        except(KeyError, AttributeError, jwt.PyJWTError,):
            return django.core.exceptions.PermissionDenied()



