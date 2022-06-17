from django.contrib import admin
from . import models
# Register your models here.

@admin.register(models.Resume)
class ResumeAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Topic)
class TopicAdmin(admin.ModelAdmin):
    pass




