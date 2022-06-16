import django.db.models.manager
from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager


class CustomerQueryset(django.db.models.QuerySet):
    pass

class CustomerManager(models.manager.BaseManager.from_queryset(CustomerQueryset)):
    pass


class ResumeQueryset(django.db.models.QuerySet):
    pass

class ResumeManager(django.db.models.manager.BaseManager.from_queryset(ResumeQueryset)):
    pass

rate_choices = [

]

class Resume(models.Model):

    objects = ResumeManager()

    resume_name = models.CharField(verbose_name=_("Resume Name"), max_length=100, null=False)
    topics = models.ForeignKey(verbose_name=_("Topics"), to=Topic, on_delete=models.PROTECT)
    created_at = models.DateField(verbose_name=_("Created At"), auto_now_add=True, max_length=100)
    rate = models.IntegerField(choices=rate_choices, verbose_name=_("Rate"), null=False)

    def __str__(self):
        return self.resume_name

class Customer(AbstractBaseUser):

    objects = CustomerManager()

    username = models.CharField(verbose_name=_("Username"), null=False, unique=True, max_length=100)
    password = models.CharField(verbose_name=_("Password"), null=False, max_length=100)
    email = models.CharField(verbose_name=_("Email"), null=False, max_length=100)

    balance = models.IntegerField(verbose_name=_("Balance"), null=False)
    resumes = models.ForeignKey(verbose_name=_("Resumes"), null=True, on_delete=models.CASCADE, to=Resume)
    created_at = models.DateField(verbose_name=_("Created At"), null=False, auto_now_add=True)

    def __str__(self):
        return self.username


