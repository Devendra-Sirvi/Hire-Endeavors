from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30, required=True, help_text='What should we call you?.')
    last_name = forms.CharField(
        max_length=30, required=True, help_text='What should be added at the last of your name?.')
    email = forms.EmailField(
        max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        ]

        def save(self, commit=True):
            user = super(RegistrationForm, self).save(commit=False)

            if commit:
                user.save()
            return user


class OrgRegistrationForm(UserCreationForm):

    email = forms.EmailField(
        max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]
        exclude = ['first_name', 'last_name']

        def save(self, commit=True):
            user = super(RegistrationForm, self).save(commit=False)

            if commit:
                user.save()
            return user


class OrgProfileform(forms.Form):
    Organisation = forms.CharField(
        max_length=50, help_text="Organisation name and Username must be same")
    Manager = forms.CharField(
        max_length=50, help_text="Who is managing the company at this portal?")
    Description = forms.CharField(
        max_length=300, help_text="Describe the people you want to hire.")

    class Meta:
        fields = [
            'Organisation',
            'Manager',
            'Description',
        ]
