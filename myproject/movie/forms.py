from django.contrib.auth.models import User
from django import forms
from .models import *
# from django.core.exceptions import ValidationError


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        labels = {'email': 'Email'}

    def clean(self):

        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            # print("Ayush sucks2")
            raise forms.ValidationError("Username exists")
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            # print("Ayush sucks2")
            raise forms.ValidationError("Email exists")
        return self.cleaned_data
