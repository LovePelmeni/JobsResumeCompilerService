from rest_framework import serializers
from django.utils.translation import gettext_lazy
from . import models
from django.apps.registry import get_models
from django.core.serializers.json import DjangoJSONEncoder
import django.core.exceptions, django.apps


class ModelMultipleChoiceField(serializers.MultipleChoiceField):

    def __init__(self, **kwargs):
        super(ModelMultipleChoiceField, self).__init__(**kwargs)
        self.model = (model for model in django.apps.apps.get_models() if
            model.__class__.__name__ == kwargs.get('model'))[0].__class__.__name__

    def to_representation(self, value):
        return json.loads(value)

    def to_internal_value(self, data):
        converted_query = []
        if not hasattr(data, '__iter__') or not all([isinstance(obj, dict) for obj in data]):
            raise django.core.exceptions.ValidationError(message='Invalid Internal Value.')
        try:
            for element, value in data.items():
                if element.startswith('id') and isinstance(value, int):
                    obj = json.dumps(list(self.model.objects.get(id=value).values()),
                    cls=DjangoJSONEncoder)
                    converted_query.append(obj)

            return json.dumps(converted_query)
        except(json.decoder.JSONDecodeError,):
            raise django.core.exception.ValidationError(
            'Value is not JSON Serializable.')


class ResumeSerializer(serializers.ModelSerializer):

    resume_name = serializers.CharField(label=_("Resume Name"))
    topics = ModelMultipleChoiceField(label=_("Resume Name"), choices=models.Topic.objects.all())
    rate = serializers.CharField(label=_("Resume Name"), choices=getattr(models, 'rate_choices'))

    class Meta:
        model = models.Resume
        fields = ('resume_name', 'topics', 'rate')

class CustomerSerializer(serializers.ModelSerializer):

    username = serializers.CharField(label=_("Username"))
    email = serializers.EmailField(label=_("Email"))
    password = serializers.CharField(label=_("Password"))

    class Meta:
        model = models.Customer
        fields = ('username', 'email', 'password')

class CustomerUpdateSerializer(CustomerSerializer):

    def __init__(self, **kwargs):
        super(CustomerSerializer, self).__init__(**kwargs)
        del self.fields['username']

        for field in self.get_fields():
            if getattr(field, 'required'):
                setattr(field, 'required', False)

    def clean_email(self, value):
        if not value in models.Customer.objects.values_list('email', flat=True):
            return value
        raise django.core.exceptions.ValidationError(message='Invalid Email')