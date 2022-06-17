import rest_framework.exceptions
from django.shortcuts import render

from rest_framework import views, viewsets, permissions as rest_perms, decorators
from . import permissions, renderers, negotiation, authentication, serializers

import django.utils.decorators, django.http, django.core.exceptions
from django.views.decorators import csrf

from . import models
from django.db import transaction


# Create your views here.


class ResumeGenericViewSet(viewsets.ModelViewSet):

    permission_classes = (rest_perms.IsAuthenticated,)
    authentication_classes = (authentication.JWTAuthenticationClass,)
    queryset = models.Resume.objects.all()
    serializer_class = serializers.ResumeSerializer

    @transaction.atomic
    @decorators.action(methods=['post'], detail=False)
    def create(self, request, **kwargs):
        try:
            customer = models.Customer.objects.get(id=request.query_params.get('customer_id'))
            serializer = serializers.ResumeSerializer(request.data, many=False)
            if serializer.is_valid(raise_exception=True):
                customer.resumes.create(**serializer.validated_data)
            return django.http.HttpResponse(status=200)
        except(django.db.utils.IntegrityError, django.core.exceptions.ObjectDoesNotExist,):
            raise NotImplementedError


    @transaction.atomic
    @decorators.action(methods=['delete'], detail=False)
    @decorators.permission_classes([permissions.IsResumeOwner,])
    def destroy(self, request, **kwargs):
        try:
            resume = self.get_queryset().objects.get(id=request.query_params.get('resume_id'))
            resume.delete()
            return django.http.HttpResponse(status=200)
        except(django.db.utils.IntegrityError, django.db.utils.DataError):
            raise NotImplementedError


    @decorators.action(methods=['get'], detail=False)
    def retrieve(self, request, **kwargs):
        pass

    @decorators.action(methods=['get'], detail=False)
    def list(self, request, **kwargs):
        pass




class UploadedCVAPIView(views.APIView):

    renderer_classes = (renderers.CVRenderer,)
    permission_classes = (rest_perms.IsAuthenticated,)
    content_negotiation_class = (negotiation.CVNegotiationContentClass,)

    def handle_exception(self, exc):
        return django.http.HttpResponse(status=500)

    def get_authenticators(self):
        return (authentication.JWTAuthenticationClass,)

    @transaction.atomic
    @django.utils.decorators.method_decorator(decorator=csrf.requires_csrf_token)
    def post(self, request):
        try:
            from . import cv
            cv_content = cv.CVContent(**request.data)
            return django.http.FileResponse(
            request.accepted_renderer.render(cv_content))
        except(rest_framework.exceptions.APIException, django.core.exceptions.ValidationError,):
            raise NotImplementedError


class CustomerAPIView(views.APIView):
    pass



class CustomerResumesAPIView(viewsets.ModelViewSet):

    queryset = models.Resume.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.JWTAuthenticationClass,)


    def filter_queryset(self, queryset):
        return queryset.filter(owner=self.request.query_params.get('customer'))


    def get_queryset(self):
        return self.filter_queryset(queryset=self.queryset)


    @decorators.action(methods=['get'], detail=True)
    def retrieve(self, request, *args, **kwargs):
        try:
            resume = self.get_queryset().get(id=request.query_params.get('resume_id')).values()
            return django.http.HttpResponse(status=200, content=json.dumps({'resume': list(resume)}))
        except(django.core.exceptions.ObjectDoesNotExist,):
            return django.http.HttpResponseNotFound()


    @decorators.action(methods=['get'], detail=False)
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().values()
        return django.http.HttpResponse(status=200,
        content=json.dumps({'resumes': list(queryset)}))


import django.core.serializers.json
class ResumePublicSuggestionsAPIView(viewsets.ReadOnlyModelViewSet):

    permission_classes = (rest_perms.IsAuthenticated,)
    queryset = models.Resume.objects.filter(private=False)


    def get_authenticators(self):
        return (authentication.JWTAuthenticationClass,)


    @decorators.action(methods=['get'], detail=True)
    def retrieve(self, request,):
        try:
            obj = self.get_queryset().get(id=request.query_params.get('resume_id'))
            return django.http.HttpResponse(status=status.HTTP_200_OK, content=json.dumps({'obj': list(obj)},
            cls=django.core.serializers.json.DjangoJSONEncoder))
        except(django.core.exceptions.ObjectDoesNotExist,):
            return django.http.HttpResponseNotFound()


    @decorators.action(methods=['get'], detail=False)
    def list(self, request):
        from django.db import models as db_models
        customer = models.Customer.objects.get(id=request.query_params.get('customer_id'))
        queryset = self.get_queryset().filter(
        has_premuim=customer.has_premuim).order_by(db_models.F("rate").desc())
        return django.http.HttpResponse(status=200, content=json.dumps({'resumes': list(queryset)},
        cls=django.core.serializers.json.DjangoJSONEncoder))




