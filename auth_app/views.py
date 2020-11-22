import os
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect, render
from django.contrib.auth.models import Group
from auth_app.forms import LoginForm, RegisterForm, ProfileForm
from django.core.files.storage import default_storage
from django.conf import settings


@transaction.atomic
def register_user(request):
    if request.method == 'GET':
        context = {
            'user_form': RegisterForm(),
            'profile_form': ProfileForm(),
        }

        return render(request, 'users/register.html', context)

    user_form = RegisterForm(request.POST)
    profile_form = ProfileForm(request.POST, request.FILES)


    if user_form.is_valid() and profile_form.is_valid():
        user = user_form.save()
        user.save()
        profile = profile_form.save(commit=False)
        profile.user = user
        profile.save()

        # Adding new user to a predefined common group
        common_group = Group.objects.get(name='users')
        common_group.user_set.add(user)

        login(request, user)
        return redirect('landing')

    # #  Saving POSTed file to storage
    # file = request.FILES['profile_image']
    # file_name = default_storage.save(file.name, file)
    #
    # # Reading file from storage. Opening the file prevents from deleting.
    # # file = default_storage.open(file_name)
    # # file_url = default_storage.url(file_name)
    #
    # # Cleaning the temporary storage, used to make image "default
    # project_root = settings.MEDIA_ROOT
    # path_to_file = os.path.join(project_root, file_name)
    # if os.path.isfile(path_to_file):
    #     os.remove(path_to_file)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }

    return render(request, 'users/register.html', context)


def get_redirect_url(params):
    redirect_url = params.get('return_url')
    return redirect_url if redirect_url else 'landing'


def login_user(request):
    # # user = authenticate(username='takvor', password='takvor')
    # # user = authenticate(username='user', password='garabedian')
    # user = authenticate(username='impotent', password='soft_key')
    # if user:
    #     login(request, user)
    #     return redirect('landing')
    #
    # return render(request, 'users/401_unauthorized.html')

    if request.method == 'GET':
        context = {
            'login_form': LoginForm(),
        }

        return render(request, 'users/login.html', context)

    login_form = LoginForm(request.POST)

    return_url = get_redirect_url(request.POST)
    if login_form.is_valid():
        username = login_form.cleaned_data['username']
        password = login_form.cleaned_data['password']
        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return redirect(return_url)

    context = {
        'login_form': login_form,
    }

    return render(request, 'users/login.html', context)


@login_required
def logout_user(request):
    logout(request)
    return redirect('landing')
