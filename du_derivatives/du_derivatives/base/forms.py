from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import User


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'csedu_batch', 'password1', 'password2']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'name', 'profile_picture', 'csedu_batch']
