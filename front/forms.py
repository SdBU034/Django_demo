# encoding = utf-8

from django import forms
from .models import User
from django.core import validators


class RegisterForm(forms.Form):
    username = forms.CharField(min_length=4, max_length=20)
    pwd1 = forms.CharField(max_length=16, min_length=6)
    pwd2 = forms.CharField(max_length=16, min_length=6)
    telephone = forms.CharField(max_length=11, validators=[validators.RegexValidator(r'1[3456778]\d{9}', message='电话号码格式错误！')])

    def clean(self):
        cleaned_data = super().clean()
        pwd1 = cleaned_data.get('pwd1')
        pwd2 = cleaned_data.get('pwd2')
        if pwd1 != pwd2:
            raise validators.ValidationError(message='两次输入密码不一致')
        return cleaned_data

    def clean_telephone(self):
        telephone = self.cleaned_data.get('telephone')
        if User.objects.filter(telephone=telephone).exists():
            raise validators.ValidationError(message='%s已经被注册了。' % telephone)
        return telephone


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['password', 'username']
        error_messages = {
            'username': {
                'min_length': 'username最小长度不能少于4位',
            },
            'password': {
                'min_length': 'password最小长度不能少于6位',
            }
        }

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        if not User.objects.filter(username=username, password=password).exists():
            raise validators.ValidationError(message='用户名或者密码错误')
        return cleaned_data

    def get_error(self):
        new_errors = []
        errors = self.errors.get_json_data()
        for messages in errors.values():
            for message_dicts in messages:
                for key, message in message_dicts.items():
                    if key == 'message':
                        new_errors.append(message)
        return new_errors
