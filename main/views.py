import rest_framework.exceptions
from django.shortcuts import render
from rest_framework import views, viewsets, permissions as rest_perms, decorators
from . import permissions, renderers, negotiation, authentication
import django.utils.decorators
from django.views.decorators import csrf
from . import models
from django.db import transaction

# Create your views here.

class ResumeGenericViewSet(viewsets.ModelViewSet):

    permission_classes = (rest_perms.IsAuthenticated,)
    authentication_classes = (authentication.JWTAuthenticationClass,)
    queryset = models.Resume.objects.all()

    @transaction.atomic
    @decorators.action(methods=[], detail=False)
    def create(self, request, **kwargs):
        pass

    @transaction.atomic
    @decorators.action(methods=[], detail=False)
    def update(self, request, **kwargs):
        pass

    @transaction.atomic
    @decorators.action(methods=[], detail=False)
    def destroy(self, request, **kwargs):
        pass

    @decorators.action(methods=[], detail=False)
    def retrieve(self, request, **kwargs):
        pass

    @decorators.action(methods=[], detail=False)
    def list(self, request, **kwargs):
        pass




class UploadedCVAPIView(views.APIView):

    renderer_classes = (renderers.CVRenderer,)
    permission_classes = (rest_perms.IsAuthenticated,)

    def handle_exception(self, exc):
        pass

    def get_renderer_context(self, **kwargs):
        pass

    def get_authenticators(self):
        return (authentication.JWTAuthenticationClass,)

    def get_content_negotiator(self):
        return negotiation.CVNegotiationContentClass()

    @transaction.atomic
    @django.utils.decorators.method_decorator(decorator=csrf.requires_csrf_token)
    def post(self, request):
        try:
            cv_content = cv.CVContent(request.data)
            return django.http.FileResponse(
            request.accepted_renderer.render(cv_content))
        except(rest_framework.exceptions.APIException):
            raise NotImplementedError


class CheckPremiumPermission(views.APIView):

    permission_classes = (rest_perms.IsAuthenticated,)
    authentication_classes = (authentication.JWTAuthenticationClass,)

    def get(self, request):
        customer = models.Customer.objects.get(
        id=request.query_params.get('customer_id'))
        return django.http.HttpResponse(
        status=200, content={'premuim': customer.has_premium})



class CustomerAPIView(views.APIView):
    pass



import django.core.serializers.json
class SuggestionsAPIView(views.APIView):

    permission_classes = (rest_perms.AllowAny,)

    @decorators.action(methods=['get'], detail=True)
    @decorators.permission_classes([rest_perms.IsAuthenticated,])
    @decorators.authentication_classes([authentication.JWTAuthenticationClass,])
    def retrieve(self, request,):
        pass

    @decorators.action(methods=['get'], detail=False)
    def list(self, request):
        from django.db import models as db_models
        customer = models.Customer.objects.get(id=request.query_params.get('customer_id'))
        queryset = models.Resume.objects.filter(premuim=customer.has_premium,
        **db_models.Q(created_at__gte=datetime.datetime.now().days - 7)
        | db_models.Q()).order_by(db_models.F("rate").desc())
        return django.http.HttpResponse(status=200, content=json.dumps(list(queryset),
        cls=django.core.serializers.json.DjangoJSONEncoder))





