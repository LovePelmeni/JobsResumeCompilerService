import contextlib

import rest_framework.exceptions
from django.shortcuts import render

from rest_framework import views, viewsets, permissions as rest_perms, decorators
from . import permissions, renderers, negotiation, authentication, serializers

import django.utils.decorators, django.http, django.core.exceptions
from django.views.decorators import csrf

from . import models
from django.db import transaction
from django.views.decorators import cache


# Create your views here.


class ResumeGenericViewSet(viewsets.ModelViewSet):

    permission_classes = (rest_perms.IsAuthenticated,)
    authentication_classes = (authentication.JWTAuthenticationClass,)
    queryset = models.Resume.objects.all()
    serializer_class = serializers.ResumeCreateSerializer

    @transaction.atomic
    @decorators.action(methods=['post'], detail=False)
    def create(self, request, **kwargs):
        try:
            customer = models.Customer.objects.get(id=request.query_params.get('customer_id'))
            serializer = serializers.ResumeCreateSerializer(request.data, many=False)
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


class UploadedCVAPIView(views.APIView):

    renderer_classes = (renderers.CVPDFRenderer,)
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
    permission_classes = (rest_perms.IsAuthenticated,)
    authentication_classes = (authentication.JWTAuthenticationClass,)
    serializer_class = serializers.ResumeGetSerializer


    def filter_queryset(self, queryset):
        return queryset.filter(owner=self.request.query_params.get('customer'))


    def get_queryset(self):
        return self.filter_queryset(queryset=self.queryset)


    @decorators.action(methods=['get'], detail=True)
    def retrieve(self, request, *args, **kwargs):
        try:
            resume = self.get_queryset().get(id=request.query_params.get('resume_id')).values()
            return django.http.HttpResponse(status=200, content=json.dumps({'resume': list(resume)},
            cls=django.core.serializers.json.DjangoJSONEncoder
            ))
        except(django.core.exceptions.ObjectDoesNotExist,):
            return django.http.HttpResponseNotFound()


    @decorators.action(methods=['get'], detail=False)
    def list(self, request, *args, **kwargs):
        queryset = self.serializer_class(self.get_queryset(), many=True)
        return django.http.HttpResponse(status=200,
        content=json.dumps({'resumes': queryset.validated_data}))


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


class TopicViewSet(viewsets.ModelViewSet):

    queryset = models.Topic.objects.all()
    serializer_class = serializers.TopicSerializer
    permission_classes = (rest_perms.IsAuthenticated,)

    def filter_queryset(self, queryset):
        resume = models.Resume.objects.get(id=self.request.query_params.get('resume_id'))
        return queryset.filter(resume=resume).select_related('topic')

    def get_queryset(self):
        return self.filter_queryset(self.queryset)

    @decorators.action(methods=['get'], detail=False)
    def retrieve(self, request, *args, **kwargs):
        topic = self.serializer_class(self.get_queryset().get(
        id=request.query_params.get('topic_id')), many=False)
        return django.http.HttpResponse(json.dumps({'topic': topic.data}))

    @decorators.action(methods=['get'], detail=False)
    def list(self, request, *args, **kwargs):
        queryset = self.serializer_class(self.get_queryset(), many=True)
        return django.http.HttpResponse(json.dumps({'queryset': queryset.data}))



class ResumesCatalogSuggestionsAPIView(viewsets.ModelViewSet):

    permission_classes = (rest_perms.IsAuthenticated,)
    queryset = models.Resume.objects.filter(private=False)

    @cache.cache_control(timeout=60 * 5)
    def get_queryset(self, request):
        """
        / * QuerySet is consists of annotation that allows to get users friends that already liked that resumes.
        """
        from django.db import models as db_models

        customer = models.Customer.objects.get(id=request.query_params.get('customer_id'))
        return models.Place.objects.annotate(friends=db_models.Subquery(
        queryset=db_models.QuerySet(query=[customer for customer in
        customer.resumes.exclude(private=True) if
        db_models.F('id') in customer.liked_resumes.values_list('resume_id', flat=True)])))


    @decorators.action(methods=['get'], detail=False)
    def retrieve(self, request, *args, **kwargs):
        query = self.get_queryset(request).filter(id=request.query_params.get('resume_id')).values()
        return django.http.HttpResponse(json.dumps({'resume': list(query.values())}))

    @decorators.action(methods=['get'], detail=False)
    def list(self, request, *args, **kwargs):
        query = self.get_queryset(request)
        return django.http.HttpResponse(status=status.HTTP_200_OK,
        content=json.dumps({'queryset': list(query.values())},
        cls=django.core.serializers.json.DjangoJSONEncoder))




