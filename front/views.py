from django.shortcuts import render, redirect, reverse
from django.views.generic import View
from .forms import RegisterForm, LoginForm
from .models import User
from django.http import HttpResponse
from django.contrib import messages


# Create your views here.
def index(request):
    return render(request, 'index.html')


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('pwd1')
            telephone = form.cleaned_data.get('telephone')
            print(username, password, telephone)
            User.objects.create(username=username, password=password, telephone=telephone)
            return render(request, 'index.html')
        else:
            print(form.errors.get_json_data())
            return HttpResponse('<h3>出错了~</h3>')


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            user = User.objects.filter(username=username).first()
            telephone = user.telephone
            user_id = user.id
            request.session['user_id'] = user_id
            # for sql in connection.queries:
            #     print(sql['sql'])
            context = {'username': username, 'telephone': telephone}
            return render(request, 'index.html', context=context)
        else:
            # messages = form.errors.get_json_data()
            # print(messages)
            errors = form.get_error()
            # print(new_messages)
            for error in errors:
                messages.info(request, error)
            return redirect(reverse('login'))


def blog(request):
    return render(request, 'blog.html')


def video(request):
    return render(request, 'video.html')
