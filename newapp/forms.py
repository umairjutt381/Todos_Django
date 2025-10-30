from django import forms
from django.contrib.auth.models import User
from .models import Profile, Todo


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_pic', 'location']

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['task_name', 'description','text']