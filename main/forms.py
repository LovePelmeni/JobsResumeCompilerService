from django import forms
from django.utils.translation import gettext_lazy as _
from . import models


class CustomerForm(forms.ModelForm):

    username = forms.CharField(label=_("Username"), max_length=100, required=True)
    email = forms.EmailField(label=_("Email"), max_length=100, required=True, widget=forms.EmailInput)
    password = forms.CharField(label=_("Password"), max_length=100, required=True)

    class Meta:
        model = models.Customer
        fields = ('username', 'email', 'password')

class CustomerUpdateForm(CustomerForm):

    def __init__(self, **kwargs):
        super(CustomerUpdateForm, self).__init__(**kwargs)

class ResumeCreationFormSet(forms.BaseModelFormSet):

    resume = forms.CharField(label='Resume Name',
    widget=forms.TextInput, required=True)

class TopicForm(forms.ModelForm):

    name = forms.CharField(label='Topic Name', required=True)
    description = forms.CharField(label='Description', required=True, widget=forms.Textarea)

    class Meta:
        model = models.Topic
        fields = ('name', 'description',)

