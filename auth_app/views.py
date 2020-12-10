from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect, render
from django.contrib.auth.models import Group
from auth_app.forms import LoginForm, RegisterForm, ProfileForm, ProfilePictureForm
from auth_app.models import UserProfile
from autocry_core.decorators import allowed_groups
from main_app.models import Item


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

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }

    return render(request, 'users/register.html', context)


# @login_required
@allowed_groups(allowed_roles=['superusers', 'users'])
def show_profile(request, pk):
    # if request.user.id == pk or request.user.is_superuser:
    if request.user.id == pk:
        user = get_user_model().objects.get(pk=pk)
        current_profile = UserProfile.objects.get(user_id=pk)

        form = ProfilePictureForm(instance=current_profile)

        items = Item.objects.filter(author=pk)
        for item in items:
            item.can_edit = True

        if request.method == 'GET':
            context = {
                'form': form,
                'user': user,
                'items': items,
                'items_empty': Item.objects.all().count() <= 0,
                'filter_included': False,
                'current_access': True,
            }

            return render(request, 'users/user_profile.html', context)

        form = ProfilePictureForm(request.POST, request.FILES)

        if form.is_valid():
            new_image = form.cleaned_data['profile_image']
            if new_image != '/images/users.jpg':
                current_profile.profile_image = new_image
                current_profile.save(update_fields=["profile_image"])

            return redirect('landing')

        context = {
            'form': form,
            'user': user,
            'items': items,
            'items_empty': Item.objects.all().count() <= 0,
            'filter_included': False,
            'current_access': True,
        }

        return render(request, 'users/user_profile.html', context)

    else:
        other = {
            'id': pk,
            'name': get_user_model().objects.get(pk=pk).username,
            'joined': get_user_model().objects.get(pk=pk).date_joined,
        }
        other_image = UserProfile.objects.get(user_id=pk).profile_image

        items = Item.objects.filter(author=pk)
        for item in items:
            item.can_edit = False
            item.creator = other['name']

        context = {
            'other': other,
            'other_image': other_image,
            'items': items,
            'items_empty': Item.objects.all().count() <= 0,
            'filter_included': False,
            'current_access': False,
        }

        return render(request, 'users/user_profile.html', context)

