from django.contrib.auth.models import User
from django.db import models


# Create your models here.
from main_app.validators import year_validator


class UserProfile(models.Model):
    birth_year = models.IntegerField(validators=[year_validator])
    profile_image = models.ImageField(blank=True, default='/images/user.png', upload_to="profiles")
    user = models.OneToOneField(User, on_delete=models.CASCADE)
