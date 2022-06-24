import contextlib

import rest_framework.exceptions, typing
from django.shortcuts import render

from rest_framework import views, viewsets, permissions as rest_perms, decorators
from . import permissions, renderers, negotiation, authentication, serializers

import django.utils.decorators, django.http, django.core.exceptions
from django.views.decorators import csrf

from . import models
from django.db import transaction
from django.views.decorators import cache
import logging

logger = logging.getLogger(__name__)
# Create your views here.

class ResumeGenericViewSet(viewsets.ModelViewSet):

    permission_classes = (rest_perms.IsAuthenticated,)
    authentication_classes = (authentication.JWTAuthenticationClass,)
    queryset = models.Resume.objects.all()
    server_exceptions = (NotImplementedError, NotImplemented,)

    def handle_exception(self, exc):
        return django.http.HttpResponse(status=status.HTTP_501_NOT_IMPLEMENTED) \
        if exc in self.server_exceptions else django.http.HttpResponseBadRequest()

    @decorators.action(methods=['get'], detail=False)
    @django.utils.decorators.method_decorator(decorator=cache.never_cache)
    def get_creation_form(self, request):
        """
        // * Allows to add some topics by specifying `extra_topics` query param. Type Integer
        """
        from . import forms
        form = forms.ResumeCreationFormSet()
        formset = forms.modelformset_factory(form=forms.TopicForm,
        extra=request.query_params.get('extra_topics'))
        return django.template.response.TemplateResponse(
        request, 'main/create_resume.html', {'formset': formset(), 'form': form})

    @transaction.atomic
    @decorators.action(methods=['post'], detail=False)
    def create(self, request, **kwargs):
        try:
            customer = models.Customer.objects.get(id=request.query_params.get('customer_id'))
            serializer = serializers.ResumeCreateSerializer(request.data, many=False)
            for topic in request.data.get('topics'):

                topic = serializers.TopicSerializer(topic, many=False)
                if not topic.is_valid(raise_exception=True):
                    raise django.core.exceptions.ValidationError(message='Invalid Data Topic.')

            if serializer.is_valid(raise_exception=True):
                resume = customer.resumes.create(**serializer.validated_data)

                topics = resume.topics.bulk_create([
                topic for topic in request.data.get('topics')])

                assert topics == len(request.data['topics'])
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

class UploadWordCVAPIView(views.APIView):

    content_negotiation_class = (negotiation.CVNegotiationContentClass,)
    renderer_classes = (renderers.CVWordRenderer,)

    def get_permissions(self):
        return (rest_perms.IsAuthenticated,)

    def get_authenticators(self):
        return (authentication.JWTAuthenticationClass,)

    def handle_exception(self, exc):
        if isinstance(exc, django.core.exceptions.BadRequest):
            return django.http.HttpResponse(status=status.HTTP_400_BAD_REQUEST)
        return django.http.HttpResponse(status=status.HTTP_501_NOT_IMPLEMENTED)

    @django.utils.decorators.method_decorator(csrf.requires_csrf_token)
    def post(self, request) -> typing.Union[django.http.FileResponse, django.http.StreamingHttpResponse]:
        try:
            content = cv.CVContent(**request.data)
            return django.http.FileResponse(
            request.accepted_renderer.render(content))
        except(renderers.RendererError, django.core.exceptions.ValidationError):
            raise django.core.exceptions.BadRequest



class UploadPDFCVAPIView(views.APIView):

    renderer_classes = (renderers.CVPDFRenderer,)
    permission_classes = (rest_perms.IsAuthenticated,)
    content_negotiation_class = (negotiation.CVNegotiationContentClass,)

    def handle_exception(self, exc):
        return django.http.HttpResponse(status=500)

    def get_authenticators(self):
        return (authentication.JWTAuthenticationClass,)

    @transaction.atomic
    @csrf.csrf_exempt
    @django.utils.decorators.method_decorator(decorator=csrf.requires_csrf_token)
    def post(self, request):
        try:
            from . import cv
            cv_content = cv.CVContent(**request.data)
            return django.http.FileResponse(
            request.accepted_renderer.render(cv_content))
        except(rest_framework.exceptions.APIException, django.core.exceptions.ValidationError,):
            raise NotImplementedError


class CustomerAPIView(viewsets.ModelViewSet):

    serializer_class = serializers.CustomerSerializer

    def handle_exception(self, exc):
        from rest_framework import status

        if isinstance(exc, django.core.exceptions.PermissionDenied):
            return django.http.HttpResponse(status=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS)

        if isinstance(exc, django.core.exceptions.ValidationError):
            return django.http.HttpResponseBadRequest()

        if isinstance(exc, django.core.exceptions.ObjectDoesNotExist):
            return django.http.HttpResponseNotFound()

        if isinstance(exc, NotImplementedError):
            return django.http.HttpResponseNotFound()


    def check_permissions(self, request):
        if request.get_signed_cookie('jwt-token') or 'Authorization' in request.META.keys():
            raise django.core.exceptions.PermissionDenied()
        return True

    @decorators.action(methods=['put'], detail=False)
    def update(self, request, *args, **kwargs):
        try:
            customer = models.Customer.objects.get(
            id=request.query_params.get('customer_id'))
            serializer = serializers.CustomerUpdateSerializer(data=request.data, many=False)
            for element, value in serializer.validated_data.items():
                setattr(customer, element, value)

            customer.save()
            return django.http.HttpResponse(status=200)
        except(django.core.exceptions.ObjectDoesNotExist,):
            return django.http.HttpResponseNotFound

    @decorators.action(methods=['delete'], detail=False)
    def destroy(self, request, *args, **kwargs):
        try:
            response = django.http.HttpResponse()
            models.Customer.objects.get(
            id=request.query_params.get('customer_id')).first().delete()
            if 'jwt-token' in request.COOKIES.keys():
                response.delete_cookie('jwt-token')
            return response
        except(django.core.exceptions.ObjectDoesNotExist,):
            return django.http.HttpResponseNotFound()

        except(KeyError, AttributeError, TypeError) as exception:
            logger.error('%s' % exception)


    @transaction.atomic
    @django.utils.decorators.method_decorator(decorator=csrf.requires_csrf_token)
    def create(self, request):
        import jwt
        response = django.http.HttpResponse()
        customer_serializer = serializers.CustomerSerializer(request.data, many=False)
        if customer_serializer.is_valid(raise_exception=True):
            try:
                user = models.Customer.objects.create(**customer_serializer.validated_data)
                response.set_signed_cookie('jwt-token', jwt.encode({'user_id': user.id},
                algorithms='HS256', key=getattr(settings, 'SECRET_KEY')))
            except(django.db.utils.IntegrityError,):
                raise NotImplementedError
        return response

    @cache.cache_page(timeout=60 * 5)
    @decorators.action(methods=['get'], detail=False, description='Returns Creation Customer Form')
    def get_create_form(self, request):
        form = forms.CustomerUpdateForm()
        return django.template.response.TemplateResponse(request,
        'main/create_customer.html', context={'form': form})

    @cache.cache_control(private=True)
    def get_update_form(self, request):
        form = forms.CustomerUpdateForm()
        customer = models.Customer.objects.get(
        id=request.query_params.get('customer_id'))
        form.initial = {element: getattr(customer, element) for
        element in customer._meta.get_fields() if element.lower() in form.get_fields()}
        return django.template.response.TemplateResponse(request,
        'main/customer_update.html', context={'form': form})


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

    @cache.cache_control(timeout=60 * 5, private=True)
    def get_queryset(self, request):
        """
        / * QuerySet is consists of annotation that allows to get users friends that already liked that resumes.
        """
        from django.db import models as db_models
        from .models import RoundValue

        customer = models.Customer.objects.get(id=request.query_params.get('customer_id'))
        return models.Resume.objects.annotate(friends=db_models.Subquery(
        queryset=db_models.QuerySet(query=[customer for customer in
        customer.resumes.exclude(private=True) if
        db_models.F('id') in customer.liked_resumes.values_list('resume_id', flat=True)]))).annotate(
        total_resume_count='over '
        '%s resumes has been published on this platform' % RoundValue(
        db_models.Count(models.Resume.objects.all()))
        )

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


class ReviewResumeAPIView(viewsets.ModelViewSet):

    serializer_class = serializers.ReviewListIssueSerializer
    permission_classes = (permissions.IsResumeOwner,)
    renderer_classes = (renderers.CVPDFRenderer,)

    def __init__(self):
        super(ReviewResumeAPIView, self).__init__()
        from .review import reviewer
        self.reviewer = reviewer.ResumeReviewer

    def get_authenticators(self):
        return (authentication.JWTAuthenticationClass,)

    def get_permissions(self):
        return (rest_perms.IsAuthenticated,)

    @decorators.action(methods=['post'], detail=False, description='Reviews Resume and return '
    'different issues related to correctness logic and consistency of the one.')
    @django.utils.decorators.method_decorator(decorator=cache.never_cache)
    def create(self, request, *args, **kwargs):
        resume = cv.RawResumeContent(request.data)
        issues = self.get_serializer_class()(self.reviewer(resume=resume).review()).data
        return django.http.HttpResponse(status=status.HTTP_200_OK,
        content=issues)



