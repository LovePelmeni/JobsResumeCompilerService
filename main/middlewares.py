import django.core.exceptions
from django.utils import deprecation


class SetAuthHeaderMiddleware(deprecation.MiddlewareMixin):

    def process_request(self, request):
        try:
            if not 'Authorization' in request.META.keys():
                request.META['Authorization'] = request.get_signed_cookie('jwt-token')
            return None
        except(KeyError,):
            return None


class BlockedMiddleware(deprecation.MiddlewareMixin):

    def process_request(self, request):
        try:
            if request.user.is_blocked:
                return django.http.HttpResponseForbidden()
        except(django.core.exceptions.RequestAborted,):
            return None

