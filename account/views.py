from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.validators import URLValidator, ValidationError
from django.http.request import HttpRequest
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

from .forms import ProfileForm, SignupForm, UserEditForm
from .models import Profile


def __redirect_url_or_home(request: HttpRequest, home: str = '/'):
    next_url = request.GET.get('next')
    if next_url is None:
        next_url = request.POST.get('next')

    if next_url:
        return HttpResponseRedirect(next_url)
    messages.error(request, f'Could not redirect to {next_url}')
    return HttpResponseRedirect(home)


# @require_GET
# def login_form(request):
#     if request.user.is_authenticated:
#         return __redirect_url_or_home(request)
#     render(request, 'account/login.html')


def signup(request):
    if request.method == 'POST':
        user_form = SignupForm(request.POST)
        if user_form.is_valid():
            try:
                user = User.objects.get(
                    username=user_form.cleaned_data['email'])
                messages.error(
                    request, f'User {user.username} already exists.')
            except User.DoesNotExist:
                user: User = user_form.save(commit=False)
                user.username = user.email
                user.set_password(user_form.cleaned_data['password'])
                user.profile = Profile()
                user.save()
                user.profile.save()
                login(request, user)
                return __redirect_url_or_home(request)
    else:
        user_form = SignupForm()
    return render(request, 'registration/signup.html', {'form': user_form})


@login_required
def edit(request: HttpRequest):

    if request.method == 'POST':
        user_form = UserEditForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)

        if user_form.is_valid():
            user = request.user
            user.first_name = user_form.cleaned_data['first_name']
            user.last_name = user_form.cleaned_data['last_name']
            user.save()
            messages.success(request, 'Successfully Updated User Information.')

            if profile_form.is_valid() and profile_form.cleaned_data['image']:
                image = profile_form.cleaned_data['image']
                user.profile.image = image
                user.profile.save()
                messages.success(request, 'Profile Picture Updated.')

        else:
            messages.error(request, 'Some data was invalid.')

    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    return render(request, 'edit.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })
