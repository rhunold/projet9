from django import forms

# from authentication.models import User

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username',)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=63, label='Nom d\'utilisateur')
    password = forms.CharField(max_length=63, widget=forms.PasswordInput, label='Mot de passe')

# class LoginForm(forms.ModelForm):
#    class Meta:
#      model = User
#      fields = '__all__'
#     #  exclude = ('time_created',)  # pour ne pas afficher certains champs du model dans le formulaire


class SubscribeForm(forms.Form):
    followed_user = forms.CharField(label=False, widget=forms.TextInput())