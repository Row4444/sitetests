from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View


from myaccount.forms import RegistrationForm, UpdateUserForm, LoginForm
from myaccount.models import User
from myaccount.tokens import account_activation_token


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

                current_site = get_current_site(request)
                user = User.objects.get(username=username)
                message = render_to_string('account/activate_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.id)),
                    'token': account_activation_token.make_token(user),
                })
                send_mail('Simple subject', message, 'sitetests1111@gmail.com', [user.email])

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
        if not user.is_verificate and user.email:
            context['email_message'] = 'Check your email: ' + user.email
        context['user'] = user
        context['update_form'] = update_form

        return render(request, 'account/detail.html', context)

    def post(self, request):
        user = get_object_or_404(User, id=request.user.id)
        update_form = UpdateUserForm(request.POST, request.FILES, instance=user)

        if update_form.is_valid():
            new_user_email = update_form.cleaned_data['email']
            if list(new_user_email) == list(user.email):
                current_site = get_current_site(request)
                user.is_verificate = False
                message = render_to_string('account/activate_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.id)),
                    'token': account_activation_token.make_token(user),
                })
                send_mail('Simple subject', message, 'sitetests1111@gmail.com', [new_user_email])

            update_form.save()

        return redirect('update')


def activate(request, idb64, token):
    try:
        id = force_text(urlsafe_base64_decode(idb64))
        user = User.objects.get(id=id)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_verificate = True
        user.save()
    return redirect('tests')


def logout_view(request):
    logout(request)
    return redirect('login')
