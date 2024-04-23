from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from users.models import Profile, Offense


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["bio", "location", "birth_date"]
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'})
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Offense
        fields = ["title", "content"]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'с307ус 192'}),
            'content': forms.Textarea(attrs={'class': 'form-control'})
        }