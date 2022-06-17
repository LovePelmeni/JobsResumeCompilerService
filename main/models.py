import django.db.models.manager
from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.utils.deconstruct import deconstructible



@deconstructible(path='main.models.CreditCardValidator')
class CreditCardValidator(object):

    def __init__(self, value):
        self.value = value

    def __call__(self, *args, **kwargs):
        self.validate()

    def validate(self):
        import re, django.core.exceptions
        if not re.match(pattern=self.match_pattern, string=self.value):
            raise django.core.exceptions.ValidationError(message='Invalid Credit Card Number.')
        return self.value

    def __eq__(self, other):
        return (
        self.validate == other.validate
        and self.value == other.value
        )


class CreditCardField(models.CharField):

    def __init__(self, **kwargs):
        super(CreditCardField, self).__init__(**kwargs)
        self.max_length = 12

    def to_python(self, value):
        return value

    def db_type(self, connection):
        return 'VARCHAR(%s)' % self.max_length

    def clean(self, value, model_instance):
        pass

    def validate(self, value, model_instance):
        pass


class CustomerQueryset(django.db.models.QuerySet):

    def create(self, **kwargs):
        pass

    def update(self, **kwargs):
        pass

    def delete(self):
        pass


class CustomerManager(models.manager.BaseManager.from_queryset(CustomerQueryset)):
    pass


class ResumeQueryset(django.db.models.QuerySet):
    pass


class ResumeManager(django.db.models.manager.BaseManager.from_queryset(ResumeQueryset)):
    pass


rate_choices = [

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
    topics = models.ForeignKey(verbose_name=_("Topics"), to=Topic, on_delete=models.PROTECT)
    created_at = models.DateField(verbose_name=_("Created At"), auto_now_add=True, max_length=100)
    rate = models.IntegerField(choices=rate_choices, verbose_name=_("Rate"), null=False)

    def __str__(self):
        return self.resume_name

    @property
    def get_created_at(self):
        return self.created_at

class Customer(AbstractBaseUser):

    objects = CustomerManager()

    username = models.CharField(verbose_name=_("Username"), null=False, unique=True, max_length=100)
    password = models.CharField(verbose_name=_("Password"), null=False, max_length=100)
    email = models.CharField(verbose_name=_("Email"), null=False, max_length=100)

    balance = models.IntegerField(verbose_name=_("Balance"), null=False)
    credit_card = CreditCardField(verbose_name=_("Credit Card"), null=True, validators=[CreditCardValidator,])
    resumes = models.ForeignKey(verbose_name=_("Resumes"), null=True, on_delete=models.CASCADE, to=Resume)
    created_at = models.DateField(verbose_name=_("Created At"), null=False, auto_now_add=True)
    has_premuim = models.BooleanField(verbose_name=_("Has Premium"), default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'password']

    def __str__(self):
        return self.username

    @property
    def get_created_at(self):
        return self.created_at



