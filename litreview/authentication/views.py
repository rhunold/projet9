from django.shortcuts import render, redirect

from django.contrib import messages

from django.db import IntegrityError

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.generic import View


from . import forms
from authentication.models import User, UserFollow


def signup_page(request):
    """Signup page """       
    form = forms.SignupForm()
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # auto-login user
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, 'authentication/signup.html', context={'form': form})



class LoginPageView(View):
    """Login page """       
    template_name = 'authentication/login.html'
    form_class = forms.LoginForm

    def get(self, request):
        form = self.form_class()
        message = ''
        return render(request, self.template_name, context={'form': form, 'message': message})
        
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('home')
        message = 'Identifiants invalides.'
        return render(request, self.template_name, context={'form': form, 'message': message})

 
def logout_user(request):
    """Logout Page """       
    logout(request)
    return redirect('login')




@login_required
def subscription_page(request):
    """ Subscription Page """        
    if request.POST.get('action') == 'search':
        form = forms.SubscribeForm(request.POST)

        if form.is_valid():
            try:
                followed_user = User.objects.get(username=request.POST['followed_user'])
                if request.user == followed_user:
                    messages.error(request, 'Vous ne pouvez pas vous suivre vous-même.')
                else:
                    try:
                        UserFollow.objects.create(user=request.user, followed_user=followed_user)
                        messages.success(request, f'Vous suivez maintenant {followed_user}!')
                    except IntegrityError:
                        messages.error(request, f'Vous suivez déjà {followed_user}!')

            except User.DoesNotExist:
                messages.error(request, f'L\'utilisateur {form.data["followed_user"]} n\'existe pas.')


    else:
        form = forms.SubscribeForm()

    user_follows = UserFollow.objects.filter(user=request.user).order_by('followed_user')
    followed_by = UserFollow.objects.filter(followed_user=request.user).order_by('user')

    context = {
        'form': form,
        'user_follows': user_follows,
        'followed_by': followed_by,
    }

    return render(request, 'authentication/subscription.html', context)


@login_required
def unfollow(request, pk):
    if request.POST.get('action') == 'unfollow':    

        unfollow = UserFollow.objects.get(id=pk)
        followed_user = unfollow.followed_user
        unfollow.delete()
        messages.success(request, f'Vous ne suivez plus {followed_user}')        
        return redirect('subscription')
    