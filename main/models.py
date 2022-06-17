import django.db.models.manager
from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.utils.deconstruct import deconstructible


class HTMLContentValidator(django.core.validators.BaseValidator):

    def __call__(self, value) -> typing.Union[str, Exception]:
        pass


class HTMLField(models.CharField):

    def __init__(self, **kwargs):
        super(HTMLField, self).__init__(**kwargs)
        self.max_length = kwargs.get('max_length')

    def validate(self, value, model_instance):
        return super().validate(value, model_instance)


import django.core.validators

class CreditCardValidator(django.core.validators.BaseValidator):

    def __call__(self, value):
        import re, django.core.exceptions
        if not re.match(pattern=self.match_pattern, string=value):
            raise django.core.exceptions.ValidationError(message='Invalid Credit Card Number.')
        return value

class CreditCardField(models.CharField):

    def __init__(self, **kwargs):
        super(CreditCardField, self).__init__(**kwargs)
        self.max_length = 12
        self.validators.append(CreditCardValidator)

    def to_python(self, value):
        return value

    def db_type(self, connection):
        return 'VARCHAR(%s)' % self.max_length

    def validate(self, value, model_instance):
        return super().validate(value, model_instance)


class ResumeQueryset(django.db.models.QuerySet):
    pass

class ResumeManager(django.db.models.manager.BaseManager.from_queryset(ResumeQueryset)):
    pass

rate_choices = [
    (str(number), '%s' % number) for number in range(1, 6)
]

class Topic(models.Model):

    objects = models.Manager()
    name = models.CharField(verbose_name=_("Topic's Name"), null=False, max_length=100)
    description = models.TextField(verbose_name=_("Description"), null=False, max_length=300)

    def __str__(self):
        return self.name

class Resume(models.Model):

    objects = ResumeManager()

    resume_name = models.CharField(verbose_name=_("Resume Name"), max_length=100, null=False)
    content = HTMLField(verbose_name=_("Image PDF Content Of the Resume"), max_length=10000, null=False)
    topics = models.ForeignKey(verbose_name=_("Topics"), to=Topic, on_delete=models.PROTECT)
    created_at = models.DateField(verbose_name=_("Created At"), auto_now_add=True, max_length=100)
    rate = models.IntegerField(choices=rate_choices, verbose_name=_("Rate"), null=False)
    private = models.BooleanField(verbose_name=_("Private."), default=True)

    class Meta:
        indexes = [
            models.Index(fields='created_at', name='created_at')
        ]

    def __str__(self):
        return self.resume_name

    @property
    def get_created_at(self):
        return self.created_at

class Customer(AbstractBaseUser):

    objects = BaseUserManager()

    username = models.CharField(verbose_name=_("Username"), null=False, unique=True, editable=False, max_length=100)
    password = models.CharField(verbose_name=_("Password"), null=False, max_length=100)
    email = models.CharField(verbose_name=_("Email"), null=False, max_length=100)

    balance = models.IntegerField(verbose_name=_("Balance"), null=False)
    credit_card = CreditCardField(verbose_name=_("Credit Card"), null=True, validators=[CreditCardValidator,])

    resumes = models.ForeignKey(verbose_name=_("Resumes"), null=True, on_delete=models.CASCADE, to=Resume)
    created_at = models.DateField(verbose_name=_("Created At"), null=False, auto_now_add=True)
    has_premuim = models.BooleanField(verbose_name=_("Has Premium"), default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'password']

    class Meta:
        indexes = [
            models.Index(fields=('created_at'), name='created_at_pkey'),
            models.Index(fields=('username'), name='username_pkey')
        ]

    def __str__(self):
        return self.username

    @property
    def get_created_at(self):
        return self.created_at





