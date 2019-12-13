from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.views import View

from myaccount.forms import RegistrationForm, UpdateUserForm, LoginForm
from myaccount.models import User


class Registration(View):
    def get(self, request):
        context = {}
        form = RegistrationForm()
        context['registration_form'] = form
        return render(request, 'account/register.html', context)

    def post(self, request):
        context = {}
        if request.POST:
            form = RegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                password1 = form.cleaned_data.get('password1')

                account = authenticate(
                    username=username,
                    password=password1,
                )
                login(request, account)

                return redirect('update')
            else:
                context['registration_form'] = form

        return render(request, 'account/register.html', context)


class Login(View):
    def get(self, request):
        context = {}
        login_form = LoginForm()
        context['login_form'] = login_form
        return render(request, 'account/login.html', context)

    def post(self, request):
        context = {}
        if request.user.is_authenticated:
            return redirect('update')
        if request.POST:
            print(request.POST)
            form = LoginForm(request.POST)

            print(form.errors)
            if form.is_valid():
                print('------')
                username = request.POST['username']
                password = request.POST['password']
                user = authenticate(username=username, password=password)

                if user:
                    login(request, user)
                    return redirect('update')
            context['login_form'] = form
            return render(request, 'account/login.html', context)


class UpdateAccount(View):
    def get(self, request):
        context = {}
        user = get_object_or_404(User, id=request.user.id)
        update_form = UpdateUserForm(instance=user)
        context['user'] = user
        context['update_form'] = update_form

        return render(request, 'account/detail.html', context)

    def post(self, request):
        context = {}
        user = get_object_or_404(User, id=request.user.id)
        print(request.FILES)
        update_form = UpdateUserForm(request.POST, request.FILES, instance=user)
        if update_form.is_valid():
            update_form.save()

        context['user'] = user
        context['update_form'] = update_form

        return render(request, 'account/detail.html', context)


def logout_view(request):
    logout(request)
    return redirect('login')