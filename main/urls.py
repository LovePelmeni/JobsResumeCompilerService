from . import views
from django.urls import path
import drf_yasg.views, drf_yasg.openapi
from rest_framework import permissions

urlpatterns = []

resume_urlpatterns = [

    path('resume/list/', views.ResumeGenericViewSet.as_view({'get': 'list'})),
    path('resume/retrieve/', views.ResumeGenericViewSet.as_view({'get': 'retrieve'})),
    path('resume/create/', views.ResumeGenericViewSet.as_view({'post': 'create'})),
    path('resume/delete/', views.ResumeGenericViewSet.as_view({'delete': 'destroy'})),

    path('customer/resumes/list/', views.CustomerResumesAPIView.as_view({'get': 'list'})),
    path('customer/resumes/retrieve/', views.CustomerResumesAPIView.as_view({'get': 'retrieve'}))

]

customer_urlpatterns = [

    path('customer/', views.CustomerAPIView.as_view()),

]


api_schema = drf_yasg.views.get_schema_view(
    info=drf_yasg.openapi.Info(
        title='Jobs Resume Compiler Project',
        description='Service That Allows To Create Custom resumes.',
        default_version='v1',
        license=drf_yasg.openapi.License('BSD License'),
        contact=drf_yasg.openapi.Contact('kirklimushin@gmail.com')
    ), permission_classes = (permissions.IsAuthenticated,),
    public=True
)

openapi_urlpatterns = [
    path('swagger/', api_schema.with_ui(cache_timeout=60 * 5), name='swagger-docs'),
    path('redoc/', api_schema.without_ui(cache_timeout=60 * 5), name='redoc-docs')
]

urlpatterns += resume_urlpatterns
urlpatterns += openapi_urlpatterns




