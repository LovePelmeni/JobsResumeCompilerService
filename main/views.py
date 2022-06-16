from django.shortcuts import render
from rest_framework import views
from . import permissions, renderers

# Create your views here.

class ResumeGenericViewSet(viewsets.ModelViewSet):

    def create(self, request, **kwargs):
        pass

    def update(self, request, **kwargs):
        pass

    def destroy(self, request, **kwargs):
        pass

    def retrieve(self, request, **kwargs):
        pass

    def list(self, request, **kwargs):
        pass

class UploadedCVAPIView(views.APIView):

    renderer_classes = (renderers.CVRenderer,)
    permission_classes = (permissions.IsAuthenticated,)


class CheckPremiumPermission(views.APIView):
    pass


class CustomerAPIView(views.APIView):
    pass


