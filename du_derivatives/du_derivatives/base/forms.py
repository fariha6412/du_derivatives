from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Project


class MyUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'username'})
        self.fields['name'].widget.attrs.update({'placeholder': 'name'})
        self.fields['csedu_batch'].widget.attrs.update({'placeholder': 'csedu_batch'})
        self.fields['email'].widget.attrs.update({'placeholder': 'email'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'repeat password'})

    class Meta:
        model = User
        fields = ['username', 'name', 'email', 'csedu_batch', 'password1', 'password2']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'name', 'profile_picture', 'csedu_batch']


class AppForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Project
        fields = '__all__'
        exclude = ['developer', 'rate', 'collaborators', 'date_added', 'date_last_updated']
