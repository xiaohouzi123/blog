from django.forms import ModelForm

from user.models import User


class RegisterForm(ModelForm):
    class Meta:
        model = User
        fields = ['name','password','email','head','sex','age']


class LoginForm(ModelForm):

    pass