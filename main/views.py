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
    pass


class CustomerAPIView(views.APIView):
    pass


class SuggestionsAPIView(views.APIView):
    pass