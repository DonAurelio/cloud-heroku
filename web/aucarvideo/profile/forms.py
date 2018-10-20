from django import forms as django_forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm as UserForm
from django.contrib.auth.forms import AuthenticationForm

class UserCreateForm(UserForm):
    email = django_forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("company_name","username", "email", "password1", "password2")
        # fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user