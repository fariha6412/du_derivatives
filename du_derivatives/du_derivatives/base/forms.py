from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
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
        fields = ['name', 'csedu_batch', 'profile_picture']


class ProjectForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'placeholder': 'project title'})
        self.fields['github_link'].widget.attrs.update({'placeholder': 'github_link'})
        self.fields['github_link'].widget.attrs.update({'placeholder': 'github project link'})
        self.fields['demo_link'].widget.attrs.update({'placeholder': 'demo video link'})
        self.fields['deployed_link'].widget.attrs.update({'placeholder': 'apk/hosted project link'})
        self.fields['about'].widget.attrs.update({'placeholder': 'write something about the project'})


    class Meta:
        model = Project
        fields = '__all__'
        exclude = ['developer', 'rate', 'tags', 'collaborators', 'date_added', 'date_last_updated']


class UserPasswordResetEmailForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(UserPasswordResetEmailForm, self).__init__(*args, **kwargs)

    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={
        'placeholder': 'email',
        'type': 'email',
        'name': 'email'
        }))