from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm

from myaccount.models import User


class DateInput(forms.DateInput):
    input_type = 'date'


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2')


class LoginForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password')

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        if not authenticate(username=username, password=password):
            raise forms.ValidationError('Invalid login')


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'img', 'name', 's_name', 'date_of_birth', 'about_me')
        widgets = {'date_of_birth': DateInput()}
