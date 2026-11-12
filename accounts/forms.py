from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.contrib.auth import get_user_model

class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Enter your email',
            'class': 'form-input',
        })
    )
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


User = get_user_model()


class EditProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'bio', 'avatar']

        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Enter your username'
            }),
            'bio': forms.Textarea(attrs={
                'placeholder': 'Write something about yourself...',
                'rows': 4
            }),
        }