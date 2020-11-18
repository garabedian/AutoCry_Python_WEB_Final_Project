from django.contrib.auth import login, authenticate, logout
from django.shortcuts import redirect, render


# Create your views here.
def login_view(request):
    # user = authenticate(username='takvor', password='takvor')
    # user = authenticate(username='user', password='garabedian')
    user = authenticate(username='impotent', password='soft_key')
    if user:
        login(request, user)
        return redirect('landing')

    return render(request, 'users/401_unauthorized.html')


def logout_view(request):
    logout(request)
    return redirect('landing')
