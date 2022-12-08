from django import forms

# from authentication.models import User

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class SignupForm(UserCreationForm):
    required_css_class = 'required-field'
    error_css_class = 'error-field'

    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Votre nom d'utilisateur"}))
    password1 = forms.CharField(label=("Password"), widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Votre mot de passe"}))
    password2 = forms.CharField(label=("Password"), help_text=("Entrez le même mot de passe pour vérification."),
                                widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Confirmation du mot de passe"}))

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username',)
        # help_texts = {
        #     'username': None,
        # }


# class LoginForm(forms.Form):
class LoginForm(AuthenticationForm):

    required_css_class = 'required-field'
    error_css_class = 'error-field'

    username = forms.CharField(label='', max_length=63,
                               widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Nom d'utilisateur"}))
    password = forms.CharField(label=(""), max_length=63,
                               widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Mot de passe"}))


class SubscribeForm(forms.Form):
    followed_user = forms.CharField(label=False, widget=forms.TextInput())
