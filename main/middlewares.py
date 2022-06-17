from django.utils import deprecation


class SetAuthHeaderMiddleware(deprecation.MiddlewareMixin):

    def process_request(self, request):
        pass