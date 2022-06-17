import django.core.serializers.json
from rest_framework import permissions


class HasPremuimAccount(permissions.BasePermission):

    def has_permission(self, request, view):
        if not models.Customer.objects.filter(id=request.query_params.get('customer_id')).first().has_premuim:
            return django.core.exceptions.PermissionDenied()
        return True

    def has_object_permission(self, request, view, obj):
        request.query_params.update({'customer_id': obj.id})
        return self.has_permission(request, view)


class IsResumeOwner(permissions.BasePermission):

    def has_permission(self, request, view):
        customer = models.Customer.objects.get(id=request.query_params.get('customer_id'))
        if not request.query_params.get('resume_id') in customer.resumes.values_list('id', flat=True):
            return django.core.exceptions.PermissionDenied()

    def has_object_permission(self, request, view, obj):
        request.query_params.update({'customer_id': obj.id})
        return self.has_permission(request, view)



