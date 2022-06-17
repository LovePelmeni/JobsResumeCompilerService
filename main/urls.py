from . import views
from django.urls import path

urlpatterns = []

resume_urlpatterns = [
    path('resume/list/', views.ResumeGenericViewSet.as_view({'get': 'list'})),
    path('resume/retrieve/', views.ResumeGenericViewSet.as_view({'get': 'retrieve'})),
    path('resume/create/', views.ResumeGenericViewSet.as_view({'post': 'create'})),
    path('resume/delete/', views.ResumeGenericViewSet.as_view({'delete': 'destroy'})),
]

customer_urlpatterns = [

]

openapi_urlpatterns = [

]

urlpatterns += resume_urlpatterns
urlpatterns += openapi_urlpatterns




