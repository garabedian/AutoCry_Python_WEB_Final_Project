from django.urls import path

from auth_app.views import register_user, login_user, logout_user, show_profile

urlpatterns = (
    path('register/', register_user, name='register user'),
    path('login/', login_user, name='login user'),
    path('logout/', logout_user, name='logout user'),
    path('profile/<int:pk>', show_profile, name='user profile'),
)
