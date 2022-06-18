from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from . import models
import typing

from django.apps import apps
from django.core.serializers.json import DjangoJSONEncoder
import django.core.exceptions, django.apps


class HyperLinkedSlugRelatedTopicField(serializers.HyperlinkedModelSerializer):

    def __init__(self, **kwargs):
        super(HyperLinkedSlugRelatedTopicField, self).__init__(**kwargs)

    def validate(self, attrs):
        return super(HyperLinkedSlugRelatedTopicField, self).validate(attrs)

    def prepare_linked_topics(self, topics):
        updated_topics = []
        topic_url = 'http://' + settings.APPLICATION_HOST + 'topic/retrieve/?topic_id=%s'
        for topic in topics:
            topic.id = topic_url % topic.id
            updated_topics.append(topic)
        return updated_topics

    def validated_data(self) -> typing.Dict[str, typing.Any]:
        validated_data = {}
        topics = self.prepare_linked_topics(topics=self.initial_data['topics'])
        validated_data['topics'] = topics
        return validated_data


class ModelMultipleChoiceField(serializers.MultipleChoiceField):

    def __init__(self, model, **kwargs):
        super(ModelMultipleChoiceField, self).__init__(**kwargs)
        self.model = model

    def to_representation(self, value):
        return json.loads(value)

    def to_internal_value(self, data):
        converted_query = []
        if not hasattr(data, '__iter__') or not all([isinstance(obj, dict) for obj in data]):
            raise django.core.exceptions.ValidationError(message='Invalid Internal Value.')
        try:
            for obj in data:
                for element, value in obj.items():
                    if element.startswith('id') and isinstance(value, int):
                        obj = json.dumps(list(self.model.objects.get(id=value).values()),
                        cls=DjangoJSONEncoder)
                        converted_query.append(obj)

            return json.dumps(converted_query)
        except(json.decoder.JSONDecodeError,):
            raise django.core.exception.ValidationError(
            'Value is not JSON Serializable.')


class ResumeCreateSerializer(serializers.ModelSerializer):

    resume_name = serializers.CharField(label=_("Resume Name"), required=True)
    topics = ModelMultipleChoiceField(label=_("Resume Name"), choices=models.Topic.objects.all(), model=models.Topic)
    rate = serializers.ChoiceField(label=_("Resume Name"), choices=getattr(models, 'rate_choices'))

    class Meta:
        model = models.Resume
        fields = ('resume_name', 'topics', 'rate')

class ResumeGetSerializer(serializers.HyperlinkedModelSerializer):

    resume_name = serializers.CharField(label=_("Resume Name"), required=False)
    topics = HyperLinkedSlugRelatedTopicField(label=_("Topics"), required=False)
    rate = serializers.ReadOnlyField(label=_("Rate"), required=False)
    created_at = serializers.ReadOnlyField(label=_("Created At"), required=False)

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
        self.fields.update({'username': serializers.ReadOnlyField(label=_("Username"), required=False)})

        for field in self.get_fields():
            if getattr(field, 'required'):
                setattr(field, 'required', False)

    def clean_email(self, value):
        if not value in models.Customer.objects.values_list('email', flat=True):
            return value
        raise django.core.exceptions.ValidationError(message='Invalid Email')


class TopicSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Topic
        fields = '__all__'