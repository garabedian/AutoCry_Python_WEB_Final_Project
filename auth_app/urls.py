from django.urls import path

from auth_app.views import login_view, logout_view

urlpatterns = (
    path('login/', login_view, name='login user'),
    path('logout/', logout_view, name='logout user'),
)
